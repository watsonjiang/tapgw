#! /usr/bin/env python

import os, sys
import socket
from fcntl import ioctl
from select import select
import dpkt
import struct
import binascii

TUNSETIFF = 0x400454ca
TUNSETPERSIST = TUNSETIFF + 1
TUNSETOWNER   = TUNSETIFF + 2
TUNSETGROUP   = TUNSETIFF + 4

SIOCSIFHWADDR = 0x8924
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI  = 0x1000

TUNMODE = IFF_TAP|IFF_NO_PI
TUN_FD = None
GW_MAC = "52:7b:34:64:00:00"
GW_IP = "192.0.1.1"
TUN_DEV_NAME = "tap0"
ID_COUNT = 0

arp_cache = {}

def mac_ntoa(mac):
   """Print out hunman readable MAC address 
   """
   return '%.2x:%.2x:%.2x:%.2x:%.2x:%.2x' % tuple(map(ord, list(mac)))

def mac_aton(str):
   """ Convert a string representation of a mac address into a network address
   """
   macbytes = [int(i, 16) for i in str.split(':')]
   return struct.pack('6B', *macbytes)

def handle_arp(arp):
   if arp.op == dpkt.arp.ARP_OP_REQUEST:
      print "Arp %s(%s) -> %s(%s)" % (mac_ntoa(arp.sha), socket.inet_ntoa(arp.spa),
                                    mac_ntoa(arp.tha), socket.inet_ntoa(arp.tpa))
      arp_cache[arp.spa] = arp.sha
      if socket.inet_ntoa(arp.tpa) == GW_IP:
         #build arp response
         arp_p = dpkt.arp.ARP()
         arp_p.op = dpkt.arp.ARP_OP_REPLY
         arp_p.sha = mac_aton(GW_MAC)
         arp_p.spa = socket.inet_aton(GW_IP)
         arp_p.tha = arp.sha
         arp_p.tpa = arp.spa
         packet = dpkt.ethernet.Ethernet()
         packet.src = mac_aton(GW_MAC)
         packet.dst = arp.sha
         packet.data = arp_p
         packet.type = dpkt.ethernet.ETH_TYPE_ARP

         #raw = struct.pack("!HH", 0, packet.type) + str(packet)
         raw = str(packet)
         os.write(TUN_FD, raw) 

         return arp_p
      
def handle_gw_icmp(icmp):
   if icmp.type == dpkt.icmp.ICMP_ECHO:
      echo_req = icmp.data
      print "icmp echo: id %d, seq %d " % (echo_req.id, echo_req.seq)
      echo_rpl = dpkt.icmp.ICMP.Echo()
      echo_rpl.id = echo_req.id
      echo_rpl.seq = echo_req.seq
      echo_rpl.data = echo_req.data
      icmp_rpl = dpkt.icmp.ICMP()
      icmp_rpl.type = dpkt.icmp.ICMP_ECHOREPLY
      icmp_rpl.code = 0
      icmp_rpl.data = echo_rpl
      return icmp_rpl
      
def handle_gw_ip(ip):
   if ip.p == dpkt.ip.IP_PROTO_ICMP:
      icmp_rpl = handle_gw_icmp(ip.data) 
      if icmp_rpl != None:
         ip_rpl = dpkt.ip.IP()
         ip_rpl.src = ip.dst
         ip_rpl.dst = ip.src
         ip_rpl.id = ID_COUNT++ 
         ip_rpl.p = dpkt.ip.IP_PROTO_ICMP
         ip_rpl.off = dpkt.ip.IP_DF
         ip_rpl.data = icmp_rpl
         ip_rpl.len += len(icmp_rpl)
         return ip_rpl
      return
   print "Ip: unknow ip proto(%s), ignore." % ip.data.__class__.__name__

def route_ip(ip):
   pass

def handle_ip(ip):
   print "Ip: %s -> %s" % (socket.inet_ntoa(ip.src), socket.inet_ntoa(ip.dst))
   if socket.inet_ntoa(ip.dst) == GW_IP:
      return handle_gw_ip(ip)
   return route_ip(ip)

def handle_frame(eth):
   print "Eth frame: %s -> %s" % (mac_ntoa(eth.src), mac_ntoa(eth.dst))
   if mac_ntoa(eth.dst) != GW_MAC and mac_ntoa(eth.dst) != "ff:ff:ff:ff:ff:ff":
      print "WARNING!!, Got frame not target to gateway, ignore." 
      return
   if eth.type == dpkt.ethernet.ETH_TYPE_ARP:
      handle_arp(eth.data)
      return
   if eth.type != dpkt.ethernet.ETH_TYPE_IP:
      print "Non IP packet type(%s) not supported. ignore" % eth.data.__class__.__name__
      return
   ip_rpl = handle_ip(eth.data)
   if ip_rpl != None:
      print "!!!!!!!!!!send rpl"
      packet = dpkt.ethernet.Ethernet()
      packet.src = mac_aton(GW_MAC)
      packet.dst = eth.src
      packet.data = ip_rpl
      packet.type = dpkt.ethernet.ETH_TYPE_IP
      #raw = struct.pack("!HH", 0, packet.type) + str(packet)
      raw = str(packet)
      os.write(TUN_FD, raw) 

   return 

if __name__ == "__main__":
   TUN_FD = os.open("/dev/net/tun", os.O_RDWR)
   ifs = ioctl(TUN_FD, TUNSETIFF, struct.pack("16sH", TUN_DEV_NAME, TUNMODE))
   ifname = ifs[:16].strip("\x00")

   #set mac addr
   #macbytes = [int(i, 16) for i in MAC.split(':')]
   #ifs = ioctl(TUN_FD, SIOCSIFHWADDR, struct.pack("16sH6B8x", 
   #            ifname, socket.AF_UNIX, *macbytes))

   #persist tap device
   ifs = ioctl(TUN_FD, TUNSETOWNER, 0)
   ifs = ioctl(TUN_FD, TUNSETGROUP, 0) 
   ifs = ioctl(TUN_FD, TUNSETPERSIST, 1)

   print "Allocated interface %s. Configure it and use it" % ifname

   try:
      while 1:
         r = select([TUN_FD],[],[])[0][0]
         if r == TUN_FD:
            print "-------------"
            raw = os.read(TUN_FD, 1500)
            #flag, proto = struct.unpack("!HH", raw[:4]) #Not needed due to NOPI
            frame = dpkt.ethernet.Ethernet(raw)
            handle_frame(frame)  
   except KeyboardInterrupt:
      print "Stopped by user."


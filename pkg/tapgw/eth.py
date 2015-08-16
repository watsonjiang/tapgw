#! /usr/bin/env python
import logging
from tapgw.utils import *
import dpkt

logger = logging.getLogger('tapgw.eth_stack')
class EthStack:
   MAC_BCAST = str(bytearray([0xff, 0xff, 0xff, 0xff, 0xff, 0xff]))
   def __init__(self, mac):
      self._mac = mac

   def set_ip_stack(self, ipstack):
      self._ip_stack = ipstack

   def set_arp_stack(self, arpstack):
      self._arp_stack = arpstack

   def set_tap(self, tap):
      self._tap = tap

   def handle_south_inco(self, eth):
      '''
      handle eth frame from tap device (south incoming)
      '''
      logger.debug("eth south incoming: %s -> %s", mac_ntoa(eth.src), mac_ntoa(eth.dst))
      if eth.dst != self.MAC_BCAST and eth.dst != self._mac:
         logger.debug("Got frame not target to gateway, ignore.")
         return
      if eth.type == dpkt.ethernet.ETH_TYPE_ARP:
         self._arp_stack.handle_south_inco(eth.data)
         return
      if eth.type != dpkt.ethernet.ETH_TYPE_IP:
         logger.debug("Non IP packet type(%s) not supported. ignore", 
                      eth.data.__class__.__name__)
         return
      self._ip_stack.handle_south_inco(eth.data)

   def _handle_north_ip_inco(self, ip):
      p = dpkt.ethernet.Ethernet()
      p.src = self._mac
      dst_mac = self._arp_stack.get_mac_addr(ip.dst)
      if dst_mac == None: #don't know the peer
         self._arp_stack.try_find_peer(ip.dst)
         return 
      p.dst = dst_mac
      p.data = ip
      p.type = dpkt.ethernet.ETH_TYPE_IP
      self._tap.write_frame(p)

   def _handle_north_arp_inco(self, arp):
      p = dpkt.ethernet.Ethernet()
      p.src = self._mac
      p.dst = arp.tha
      p.data = arp
      p.type = dpkt.ethernet.ETH_TYPE_ARP
      self._tap.write_frame(p)

   def _handle_north_inco(self, pkg):
      '''
      handle pkg from ip/arp stack (north incoming)
      '''
      if pkg isinstance dpkt.ip.IP:
         self._handle_north_ip_inco(pkg)
      elif pkg isinstance dpkt.arp.ARP:
         self._handle_north_arp_inco(pkg) 
      else:
         logger.info("unknow north income! %s", pkg.__class__.__name__) 

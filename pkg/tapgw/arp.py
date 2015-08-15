#! /usr/bin/env python
import logging
import threading
import dpkt
import socket
from tapgw.utils import mac_aton, mac_ntoa
logger = logging.getLogger('tapgw.arp_stack')

class ArpStack:
   def __init__(self, gw_ip, gw_mac):
      self._arp_cache = {}
      self._arp_cache_lock = threading.Lock()
      self._gw_ip = socket.inet_aton(gw_ip)
      self._gw_mac = mac_aton(gw_mac)
      self._eth_stack = None

   def set_eth_stack(self, eth_stack):
      self._eth_stack = eth_stack

   def _add_arp_entry(self, ip, mac):
      with self._arp_cache_lock:
         self._arp_cache[ip] = mac

   def get_mac_addr(self, ip):
      with self._arp_cache_lock:
         if ip not in self._arp_cache:
            return None
         return self._arp_cache[ip] 

   def handle_south_inco(self, arp):
      if arp.op == dpkt.arp.ARP_OP_REQUEST:
         logger.debug("Arp %s(%s) -> %s(%s)"
                       ,mac_ntoa(arp.sha), socket.inet_ntoa(arp.spa)
                       ,mac_ntoa(arp.tha), socket.inet_ntoa(arp.tpa))
         self._add_arp_entry(arp.spa, arp.sha)
         if arp.tpa == self._gw_ip:
            #build arp response
            arp_p = dpkt.arp.ARP()
            arp_p.op = dpkt.arp.ARP_OP_REPLY
            arp_p.sha = self._gw_mac
            arp_p.spa = self._gw_ip
            arp_p.tha = arp.sha
            arp_p.tpa = arp.spa
            self._eth_stack.handle_north_inco(arp_p)

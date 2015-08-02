#! /usr/bin/env python
import logging

logger = logging.getLogger('tapgw.arp_stack')

class ArpStack:
   def __init__(self, gw_ip):
      self.arp_cache = {}
      self._gw_ip = gw_ip
      self._eth_stack = None

   def set_eth_stack(self, eth_stack):
      self._eth_stack = eth_stack

   def handle_south_inco(self, arp):
      if arp.op == dpkt.arp.ARP_OP_REQUEST:
         logger.debug("Arp %s(%s) -> %s(%s)", mac_ntoa(arp.sha), socket.inet_ntoa(arp.spa)
                       ,mac_ntoa(arp.tha), socket.inet_ntoa(arp.tpa))
         self.arp_cache[arp.spa] = arp.sha
         if socket.inet_ntoa(arp.tpa) == self._gw_ip:
            #build arp response
            arp_p = dpkt.arp.ARP()
            arp_p.op = dpkt.arp.ARP_OP_REPLY
            arp_p.sha = mac_aton(GW_MAC)
            arp_p.spa = socket.inet_aton(GW_IP)
            arp_p.tha = arp.sha
            arp_p.tpa = arp.spa
            self._eth_stack.handle_north_inco(arp_p)

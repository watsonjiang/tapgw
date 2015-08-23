#! /usr/bin/env python
import dpkt
import logging

logger = logging.getLogger('tapgw.ip_stack')

class IpStack:
   def __init__(self):
      pass

   def set_router(self, rt):
      self._router = rt

   def set_eth_stack(self, eth_stack):
      self._eth_stack = eth_stack
 
   def set_icmp_stack(self, icmp_stack):
      self._icmp_stack = icmp_stack

   def handle_south_inco(self, ip):
      if ip.p == dpkt.ip.IP_PROTO_ICMP:
         self._icmp_stack.handle_south_inco(ip.data)
      self._router.handle_south_inco(ip) 

   def handle_north_inco(self, pkg):
      '''handle pkg from icmp/router
      '''
      if isinstance(pkg, dpkt.icmp.ICMP):
         self._handle_north_icmp_inco(pkg)
      elif isinstance(pkg, dpkt.ip.IP): 
         self._handle_north_ip_inco(ip)


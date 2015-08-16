#! /usr/bin/env python
import dpkt
import logging

logger = logging.getLogger('tapgw.icmp_stack')

class IcmpStack:
   def __init__(self):
      self._ip_stack = None

   def set_ip_stack(self, ip_stack):
      self._ip_stack = ip_stack

   def handle_south_inco(self, icmp):
      if icmp.type == dpkt.icmp.ICMP_ECHO:
         req = icmp.data
         logger.debug("icmp echo: id %d, seq %d", req.id, req.seq)
         rpl = dpkt.icmp.ICMP.Echo()
         rpl.id = req.id
         rpl.seq = req.seq
         rpl.data = req.data
         icmp_rpl = dpkt.icmp.ICMP()
         icmp_rpl.type = dpkt.icmp.ICMP_ECHOREPLY
         icmp_rpl.code = 0
         icmp_rpl.data = rpl
         self._ip_stack.handle_north_inco(icmp_rpl)
         

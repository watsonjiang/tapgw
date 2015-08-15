#! /usr/bin/env python
import logging
from tapgw.utils import *
import dpkt

logger = logging.getLogger('tapgw.eth_stack')
class EthStack:
   MAC_BCAST = str(bytearray([0xff, 0xff, 0xff, 0xff, 0xff, 0xff]))
   def __init__(self, mac):
      self._mac = mac
      self._ip_stack = None

   def set_ip_stack(self, ipstack):
      self._ip_stack = ipstack

   def set_arp_stack(self, arpstack):
      self._arp_stack = arpstack

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

   def handle_north_inco(self, ip):
      '''
      handle ip pkg from ip stack (north incoming)
      '''
      pass

#! /usr/bin/env python
import logging

logger = logging.getLogger('tapgw.eth_stack')
MAC_BCAST = 0xffffffffffff
class EthStack:
   def __init__(self, mac):
      self._mac = mac
      self._ipstack = None

   def set_ip_stack(self, ipstack):
      self._ipstack = ipstack

   def set_arp_stack(self, arpstack):
      self._arpstack = arpstack

   def handle_south_inco(self, eth):
      '''
      handle eth frame from tap device (south incoming)
      '''
      logger.debug("eth south incoming: %s -> %s", mac_ntoa(eth.src), mac_ntoa(eth.dst))
      if eth.dst != MAC_BCASE and eth.dst != self._mac:
         logger.debug("Got frame not target to gateway, ignore.")
         return
      if eth.type == dpkt.ethernet.ETH_TYPE_ARP:
         self._arpstack.handle_south_inco(eth.data)
         return
      if eth.type != dpkt.ethernet.ETH_TYPE_IP:
         logger.debug("Non IP packet type(%s) not supported. ignore", 
                      eth.data.__class__.__name__)
         return
      self._ipstack.handle_south_inco(eth.data)

   def handle_north_inco(self, ip):
      '''
      handle ip pkg from ip stack (north incoming)
      '''
      pass

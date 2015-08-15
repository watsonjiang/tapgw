#! /usr/bin/env python
import unittest
import dpkt
from tapgw.arp import ArpStack
from tapgw.utils import mac_aton
import socket

import logging
logging.basicConfig(level=logging.DEBUG)

class MockEthStack:
   def __init__(self):
      self.eth_pkg = None
   def handle_north_inco(self, eth_pkg):
      self.eth_pkg = eth_pkg

class EthTest(unittest.TestCase):
   def setUp(self):
      self._GW_IP = "192.0.0.1"
      self._GW_MAC = "51:00:00:00:00:01"
      self.arp_stack = ArpStack(self._GW_IP, self._GW_MAC)
      self.eth_stack = MockEthStack()
      self.arp_stack.set_eth_stack(self.eth_stack)
      return

   def tearDown(self):
      return

   def testGetSetArpCache(self):
      self.arp_stack._add_arp_entry(socket.inet_aton("127.0.0.1"),
                                    mac_aton("50:00:00:00:00:01"))
      nmac = self.arp_stack.get_mac_addr(socket.inet_aton("127.0.0.1"))
      self.assertEqual(nmac, mac_aton("50:00:00:00:00:01"))
   
   def testGetSetArpCacheNotFound(self):
      nmac = self.arp_stack.get_mac_addr("127.0.0.1")
      self.assertEqual(nmac, None) 

   def testHandleSouthInco1(self):
      '''
      test handle arp request
      '''
      req = dpkt.arp.ARP()
      req.op = dpkt.arp.ARP_OP_REQUEST
      req.sha = mac_aton("00:00:00:00:00:01")
      req.spa = socket.inet_aton("192.0.1.11")
      req.tha = mac_aton("ff:ff:ff:ff:ff:ff")  #don't care
      req.tpa = socket.inet_aton("192.0.0.1")  #where is 192.0.0.1 
      self.arp_stack.handle_south_inco(req)
      rsp = self.eth_stack.eth_pkg
      self.assertEqual(rsp.op, dpkt.arp.ARP_OP_REPLY)
      self.assertEqual(rsp.sha, mac_aton(self._GW_MAC))
      self.assertEqual(rsp.spa, socket.inet_aton(self._GW_IP))
      self.assertEqual(rsp.tha, mac_aton("00:00:00:00:00:01"))
      self.assertEqual(rsp.tpa, socket.inet_aton("192.0.1.11"))
      nmac = self.arp_stack.get_mac_addr(socket.inet_aton("192.0.1.11"))
      self.assertEqual(nmac, mac_aton("00:00:00:00:00:01"))
      return 

   def testHandleSouthInco2(self):
      '''
      test handle arp request, not query gw, should be ignored
      '''
      req = dpkt.arp.ARP()
      req.op = dpkt.arp.ARP_OP_REQUEST
      req.sha = mac_aton("00:00:00:00:00:01")
      req.spa = socket.inet_aton("192.0.1.11")
      req.tha = mac_aton("ff:ff:ff:ff:ff:ff")  #don't care
      req.tpa = socket.inet_aton("192.0.0.2")  #where is 192.0.0.2 
      self.arp_stack.handle_south_inco(req)
      rsp = self.eth_stack.eth_pkg
      self.assertEqual(rsp, None)
      nmac = self.arp_stack.get_mac_addr(socket.inet_aton("192.0.1.11"))
      self.assertEqual(nmac, mac_aton("00:00:00:00:00:01"))
      return 



if __name__ == "__main__":
   unittest.main() 

#! /usr/bin/env python
import unittest
import dpkt
from tapgw.eth import EthStack
from tapgw.utils import mac_aton

import logging
logging.basicConfig(level=logging.DEBUG)

class MockIpStack:
   def __init__(self):
      self.ip_pkg = None
   def handle_south_inco(self, ip_pkg):
      self.ip_pkg = ip_pkg

class MockArpStack:
   def __init__(self):
      self.arp_pkg = None
   def handle_south_inco(self, arp_pkg):
      self.arp_pkg = arp_pkg

MAC=mac_aton("50:00:00:00:00:01")

class EthTest(unittest.TestCase):
   def setUp(self):
      self.eth_stack = EthStack(MAC)
      self.ip_stack = MockIpStack()
      self.arp_stack = MockArpStack()
      self.eth_stack.set_ip_stack(self.ip_stack)
      self.eth_stack.set_arp_stack(self.arp_stack)
      return

   def tearDown(self):
      return


   def testHandleSouthInco1(self):
      '''
      test arp broadcast pkg
      '''
      raw = bytearray(
                  [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 
                   0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
                   0x08, 0x06, 0x00, 0x01, 0x08, 0x00,
                   0x06, 0x04, 0x00, 0x01, 0x02, 0x02,
                   0x02, 0x02, 0x02, 0x02, 0xc0, 0xa8,
                   0x01, 0x01, 0xff, 0xff, 0xff, 0xff,
                   0xff, 0xff, 0xc0, 0xa8, 0x01, 0x01,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
         
      eth = dpkt.ethernet.Ethernet(raw)
      self.eth_stack.handle_south_inco(eth)
      self.assertEqual(self.arp_stack.arp_pkg, eth.data)
      self.assertEqual(self.ip_stack.ip_pkg, None)
      return 

   def testHandleSouthInco2(self):
      '''
      test gw specific arp package
      '''
      raw = bytearray(
                  [0x50, 0x00, 0x00, 0x00, 0x00, 0x01, 
                   0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
                   0x08, 0x06, 0x00, 0x01, 0x08, 0x00,
                   0x06, 0x04, 0x00, 0x01, 0x02, 0x02,
                   0x02, 0x02, 0x02, 0x02, 0xc0, 0xa8,
                   0x01, 0x01, 0x50, 0x00, 0x00, 0x00,
                   0x00, 0x01, 0xc0, 0xa8, 0x01, 0x01,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
         
      eth = dpkt.ethernet.Ethernet(raw)
      self.eth_stack.handle_south_inco(eth)
      self.assertEqual(self.arp_stack.arp_pkg, eth.data)
      self.assertEqual(self.ip_stack.ip_pkg, None)
      return 


   def testHandleSouthInco3(self):
      '''
      test eth frame not target to gw
      '''
      raw = bytearray(
                  [0xff, 0xff, 0xff, 0xff, 0xff, 0xf1, 
                   0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
                   0x08, 0x06, 0x00, 0x01, 0x08, 0x00,
                   0x06, 0x04, 0x00, 0x01, 0x02, 0x02,
                   0x02, 0x02, 0x02, 0x02, 0xc0, 0xa8,
                   0x01, 0x01, 0xff, 0xff, 0xff, 0xff,
                   0xff, 0xf1, 0xc0, 0xa8, 0x01, 0x01,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
         
      eth = dpkt.ethernet.Ethernet(raw)
      self.eth_stack.handle_south_inco(eth)
      self.assertEqual(self.arp_stack.arp_pkg, None)
      self.assertEqual(self.ip_stack.ip_pkg, None)
      return 


if __name__ == "__main__":
   unittest.main() 

#! /usr/bin/env python
import unittest
import dpkt
from tapgw.eth import EthStack

class MockIpStack:
   def handle_south_inco(self, ip_pkg):
      self.ip_pkg = ip_pkg

class MockArpStack:
   def handle_south_inco(self, arp_pkg):
      self.arp_pkg = arp_pkg

MAC=0x500000000001

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

   def testHandleSouthInco(self):
      
      self.eth_stack.handle
      return 

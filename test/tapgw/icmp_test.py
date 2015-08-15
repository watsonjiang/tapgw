#! /usr/bin/env python
import unittest
import dpkt
from tapgw.icmp import IcmpStack
from tapgw.utils import mac_aton
import socket

import logging
logging.basicConfig(level=logging.DEBUG)

class MockEthStack:
   def __init__(self):
      self.eth_pkg = None
   def handle_north_inco(self, eth_pkg):
      self.eth_pkg = eth_pkg

class IcmpTest(unittest.TestCase):
   def setUp(self):
      self.icmp_stack = IcmpStack()
      self.eth_stack = MockEthStack()
      self.icmp_stack.set_eth_stack(self.eth_stack)
      return

   def tearDown(self):
      return

   def testHandleSouthInco1(self):
      '''
      test handle icmp ping
      '''
      req = dpkt.icmp.ICMP.Echo()
      req.data = "hello"
      req.id = 1
      req.seq = 1
      req_icmp = dpkt.icmp.ICMP()
      req_icmp.type = dpkt.icmp.ICMP_ECHO
      req_icmp.code = 0
      req_icmp.data = req
      self.icmp_stack.handle_south_inco(req_icmp)
      rsp = self.eth_stack.eth_pkg
      self.assertEqual(rsp.type, dpkt.icmp.ICMP_ECHOREPLY)
      return 


if __name__ == "__main__":
   unittest.main() 

#! /usr/bin/env python
import unittest
from tapgw import utils

class EthTest(unittest.TestCase):

   def testMacNtoa(self):
      nmac = str(bytearray([0x50, 0x00, 0x00, 0x00, 0x00, 0x01]))
      amac = utils.mac_ntoa(nmac)
      self.assertEqual(amac, "50:00:00:00:00:01") 
     
   def testMacAton(self):
      amac = "50:00:00:00:00:01"
      nmac = utils.mac_aton(amac)
      self.assertEqual(nmac, str(bytearray([0x50, 0x00, 0x00, 0x00, 0x00, 0x01])))

if __name__ == "__main__":
   unittest.main() 

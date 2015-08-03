#! /usr/bin/env python

from tapgw.gateway import Gateway
from tapgw.router import Router
from tapgw.ip import IpStack
from tapgw.arp import ArpStack
from tapgw.icmp import IcmpStack
from tapgw.eth import EthStack
from tapgw.utils import *

import logging

logger = logging.getLogger('tapgw')

def _monkey_patch():
   import gevent.monkey
   gevent.monkey.patch_all()

def run_forever(**conf):
   tap_dev_name = conf['tap_dev_name']
   gw_mac = mac_aton(conf['gw_mac'])
   gw_ip = conf['gw_ip']
   gw = Gateway(tap_dev_name, gw_mac, gw_ip)
   rt_ip = conf['router_ip']
   rt_port = conf['router_port']
   rt_tbl = eval(conf['router_tbl']) 
   rt = Router(rt_ip, rt_port, rt_tbl)
   logger.debug("apply gevent monkey patch.")
   _monkey_patch()

   eth_stack = EthStack()
   arp_stack = ArpStack()
   icmp_stack = IcmpStack()
   ip_stack = IpStack()
   
   gw.set_ip_stack(ip_stack)
   rt.set_eth_stack(eth_stack) 
   gw.start()
   rt.start()
   #loop for ever
   while True:
      time.sleep(1)  

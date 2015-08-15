#! /usr/bin/env python

from tapgw.gateway import Gateway
from tapgw.router import Router
from tapgw.ip import IpStack
from tapgw.arp import ArpStack
from tapgw.icmp import IcmpStack
from tapgw.eth import EthStack

import logging

logger = logging.getLogger('tapgw')

def run_gw_forever(**conf):
   logger.info("run gateway with conf %s" % conf)
   tap_dev_name = conf['tap_dev_name']
   gw_mac = mac_aton(conf['gw_mac'])
   gw_ip = conf['gw_ip']
   gw = Gateway(tap_dev_name, gw_mac, gw_ip)
   rt_ip = conf['router_ip']
   rt_port = conf['router_port']
   rt_tbl = eval(conf['router_tbl']) 
   rt = Router(rt_ip, rt_port, rt_tbl)

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
      import time
      time.sleep(1)  

def run_lb_forever(**conf):
   pass

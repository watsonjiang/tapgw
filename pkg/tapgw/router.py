#! /usr/bin/env python

import logging
import threading
logger = logging.getLogger('tapgw.router')

class Router(threading.Thread):
   def __init__(self, rt_ip, rt_port, rt_tbl):
      self._rt_ip = rt_ip
      self._rt_port = rt_port
      self._rt_tbl_path = rt_tbl
      self._ip_stack = None 

   def set_ip_stack(self, ip_stack):
      self._ip_stack = ip_stack

   def read_pkg():
      return 

   def write_pkg():
      pass

   def router_loop(self):
      logger.debug("start router loop")
      while True:
         try:
            req = self.read_pkg()
            self._ip_stack.handle_north_inco(req)
         except:
            logging.exception("router loop error!")

     

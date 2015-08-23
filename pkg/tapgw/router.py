#! /usr/bin/env python

import logging
import threading
import socket
logger = logging.getLogger('tapgw.router')

class Router(threading.Thread):
   def __init__(self, rt_ip, rt_port, rt_tbl):
      self._rt_ip = rt_ip
      self._rt_port = rt_port
      self._rt_tbl_path = rt_tbl
      self._ip_stack = None 

   def _open_socket(self):
      self._svrsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self._svrsock.setsockopt(socekt.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self._svrsock.bind('', 9999)
      self._clisock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self._clisock.connect('127.0.0.4') 

   def set_ip_stack(self, ip_stack):
      self._ip_stack = ip_stack

   def read_pkg(self):
      try:
         msg, addr = self._svrscok.recvfrom(1500)
         logger.debug("Got data from %s" % addr)
         return msg
      except: 
         logger.exception("fail to recv message")
      

   def write_pkg(self, ip):
      self._clisock.sendall(ip)

   def run(self):
      logger.debug("start router loop")
      while True:
         try:
            req = self.read_pkg()
            self._ip_stack.handle_north_inco(req)
         except:
            logger.exception("router loop error!")

     

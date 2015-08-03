from tapgw.tap import Tap
import logging
import sys
import threading
import time

logger = logging.getLogger('tapgw.gateway')


class Gateway(threading.Thread):
   def __int__(self, tap_dev_name):
      self._tap_dev_name = tap_dev_name

   def set_eth_stack(self, eth_stack):
      self._eth_stack = eth_stack

   def run(self):
      logger.debug("create tap device [%s]", self._tap_dev_name)
      try:
         tap = Tap(self._tap_dev_name)
      except:
         logging.exception("fail to init tap device.")
         sys.exit(1)
      logger.debug("start gateway loop")
      while True:
         try:
            req = tap.read_frame()
            self._eth_stack.handle_south_inco(req)
         except:
            logging.exception("gateway loop error!")


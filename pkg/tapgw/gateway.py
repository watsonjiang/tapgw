from tapgw.tap import Tap
import logging
import sys
import threading
import time

logger = logging.getLogger('tapgw.gateway')

def monkey_patch():
   import gevent.monkey
   gevent.monkey.patch_all()


class Gateway:
   def __int__(self):
      pass

   def tap_loop(self):
      logger.debug("start tap loop")
      while True:
         try:
            req = self.tap.read_frame()
            self.eth_stack.handle_south_inco(req)
         except:
            logging.exception("tap loop error!")

   def router_loop(self):
      logger.debug("start router loop")
      while True:
         try:
            req = self.router.read_pkg()
            self.ip_stack.handle_north_inco(req)
         except:
            logging.exception("router loop error!")

   def run_forever(self):
      logger.debug("apply gevent monkey patch.")
      monkey_patch()
      logger.debug("create tap device [%s]", self.tap_dev_name)
      try:
         self.tap = Tap(self.tap_dev_name)
      except:
         logging.exception("fail to init tap device.")
         sys.exit(1)
      try:
         self.router = Router()
      except:
         logging.exception("fail to init router.")
         sys.exit(1)
      self.ip_stack = IpStack()
      self.eth_stack = EthStack(self.ip_stack)
      self.ip_stack.set_eth_stack(self.eth_stack)
      threading.Thread(target=self.tap_loop).start()
      threading.Trhead(target=self.router_loop).start()
      #loop forever 
      while True:
         time.sleep(1)

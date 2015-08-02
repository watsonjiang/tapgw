from tapgw.tap import Tap
import logging
import sys
import threading

logger = logging.getLogger('tapgw.gateway')

def monkey_patch():
   import gevent.monkey
   gevent.monkey.patch_all()

def handle_req(req_frame):
   pass


      
def tap_loop(self):
   logger.debug("open tap device")
   try:
      tap = Tap(tap_dev_name)
   except:
      logging.exception("fail to init tap device.")
      sys.exit(1)
 
   while True:
      try:
         req_frame = tap.read_frame()
         rsp_frame = handle_req(req_frame)
         tap.write_frame(rsp_frame)
      except:
         logging.exception("gateway loop error!")

def udp_loop():
   pass

def run(tap_dev_name):
   logger.debug("apply gevent monkey patch.")
   monkey_patch()
   t = threading.Thread(target=tap_loop)
   t.start()       
    

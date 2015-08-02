import os
from fcntl import ioctl
import dpkt
import struct

TUNSETIFF = 0x400454ca
TUNSETPERSIST = TUNSETIFF + 1
TUNSETOWNER   = TUNSETIFF + 2
TUNSETGROUP   = TUNSETIFF + 4

SIOCSIFHWADDR = 0x8924
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI  = 0x1000

TUNMODE = IFF_TAP|IFF_NO_PI

class Tap:
   '''
   class to abstract tap device
   '''
   def __init__(self, name):
      self._tun_fd = None
      self._dev_name = name
      self.open_dev()

   def open_dev(self):
      self._tun_fd = os.open('/dev/net/run', os.O_RDWR)
      ifs = ioctl(self._tun_fd, TUNSETIFF, 
                  struct.pack('16sH', self._dev_name, TUNMODE))
      ifname = ifs[:16].strip('\x00')
      #persist tap device
      ioctl(self._tun_fd, TUNSETOWNER, 0)
      ioctl(self._tun_fd, TUNSETGROUP, 0)
      ioctl(self._tun_fd, TUNSETPERSIST, 1)
   
   def read_frame(self):
      raw = os.read(self._tun_fd, 1500)
      return dpkt.ethernet.Ethernet(raw)      

   def write_frame(self, frame):
      os.write(self._tun_fd, str(frame)) 

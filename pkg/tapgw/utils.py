def mac_ntoa(mac):
   """Print out hunman readable MAC address 
   """
   return '%.2x:%.2x:%.2x:%.2x:%.2x:%.2x' % tuple(map(ord, list(mac)))

def mac_aton(str):
   """ Convert a string representation of a mac address into a network address
   """
   macbytes = [int(i, 16) for i in str.split(':')]
   return struct.pack('6B', *macbytes)



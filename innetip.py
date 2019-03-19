import socket
import fcntl
import struct
  
def getpubip():
    with open('/etc/myshell/new_baseinfo', 'r') as f:
        for line in f:
            if line.startswith('nodeip'):
                ip = line.strip('\n').split('=')
                pubip = ip[1].strip()
    return pubip

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

print "{},{},{}".format(getpubip(), get_ip_address('eth0'),get_ip_address('eth1'))

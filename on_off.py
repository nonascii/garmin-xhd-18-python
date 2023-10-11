#!/usr/bin/env python

import socket
import struct

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    cmd_on  = struct.pack("<iib", 0x919, 1, 1)
    cmd_off = struct.pack("<iib", 0x919, 1, 0)
    while True:
        cmd = input("Type 1 or 0 to On/Off:")
        if   cmd == '0':
            print('sending off')
            sock.sendto(cmd_off, ('172.16.2.0', 50101))
        elif cmd == '1':
            print('sending on')
            sock.sendto(cmd_on,  ('172.16.2.0', 50101))


if __name__ == '__main__':
  main()

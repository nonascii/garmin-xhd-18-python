#!/usr/bin/python3

import _thread, time, socket, binascii
from struct import unpack
from collections import namedtuple
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from threading import Lock

lock = Lock()

host       = '172.16.1.1'
MCAST_GRP  = '239.254.2.0'
MCAST_PORT = 50102

data = []
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#sock.settimeout(0.2)
try:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except AttributeError as e:
    print(e)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

sock.bind((MCAST_GRP, MCAST_PORT))

sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF,   socket.inet_aton(host))
sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))


def listening_thread():
    global data
    while True:
        with lock:
            while len(data) < 1440:
                try:
                    data_raw, addr = sock.recvfrom(1024)
                  #data = data_raw
                except socket.error as e:
                    print ('Exception {}'.format(e))
                data.append(data_raw)


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)


def drawSpokes(radar):
    img = Image.new('RGB', (5500, 5500))
    for line_data, angle in radar:
        for r, strength in enumerate(line_data):
            x, y = pol2cart(r, angle)
            #print (x,y,r,angle,strength)
            img.putpixel((1500+int(x),1500+int(y)), (0,0,strength))
    img.save('sqr2.png')
    #return img


def drawSpokesNP(radar):
    w, h = 5500, 5500
    n = 256
    x = np.linspace(-3., 3., n)
    y = np.linspace(-3., 3., n)
    data = np.zeros((h,w,3),dtype=np.uint8)

    for line_data, angle in radar:
        for r, strength in enumerate(line_data):
            if strength != 0:
#                x, y = pol2cart(r, angle/4)
#                ix, iy = np.round(x,1)*10,np.round(y,1)*10
#                data[1500+int(ix),1500+int(iy)]= [strength,0,0]

                qx, wy = pol2cart(r, np.deg2rad(angle))
                zx, zy = np.round(qx,1)*10,np.round(wy,1)*10
                data[1500+int(zx),1500+int(zy)]= [0,0,strength]

#                ax, by = pol2cart(r, angle) #np.rad2deg(angle))
#                jx, jy = np.round(ax,1)*10,np.round(by,1)*10
#                print (np.round(x,1)*10, np.round(y,1)*10, r, angle, strength)
#                data[1500+ int(jx),1500+int(jy)]= [0,strength,0]

    img = Image.fromarray(data, 'RGB')
    img.save('sqr.png')
    #return img


def drawMPL(radar):
    # setting the axes projection as polar
    plt.axes(projection = 'polar')

    #for rad in rads:
    #    plt.polar(rad, r, 'g.') 

    for line_data, angle in radar:
        for r, strength in enumerate(line_data):
            plt.scatter(angle, r, c=strength)
            print (angle,r,strength)

    # display the Polar plot
    plt.savefig('plot.png', format='png')


def main():
    global data
    try:
        _thread.start_new_thread(listening_thread, ())
    except:
        print ("Error: unable to start thread")
        quit()

    radar = []
    debug = False
    while 1:
        with lock:
            if data:
                for spoke in data:
                    data_raw = spoke
                    data_len = len(data_raw)
                    print ("")
                    if data_len == 558:
                        packet_type, len1, fill_1, scan_length, angle, fill_2, range_meters, display_meters, fill_3, scan_length_bytes_s, fills_4, scan_length_bytes_i, fills_5, line_data = unpack('<iihhhhiihhhih522s', data_raw)
                        if debug:
                            print ("packet_type {}".format(hex(packet_type)))
                            print ("len1 {}".format(len1))
                            print ("fill_1 {}".format(fill_1))
                            print ("scan_length {}".format(scan_length))
                            print ("angle {} angle_raw {}".format(angle, angle/8))
                            print ("fill_2 {}".format(fill_2))
                            print ("range_meters {}".format(range_meters))
                            print ("display_meters {}".format(display_meters))
                            print ("fill_3 {}".format(fill_3))
                            print ("scan_s {}".format(scan_length_bytes_s))
                            print ("fills_4 {}".format(fills_4))
                            print ("scan_i {}".format(scan_length_bytes_i))
                            print ("fills_5 {}\n".format(fills_5))
                        radar.append((line_data, angle/8))
                drawSpokesNP(radar)
               # drawSpokes(radar)
                        #drawMPL(radar)
                exit()
                data = []   # Empty the variable ready for the next one
    #        time.sleep(1)

if __name__ == '__main__':
  main()


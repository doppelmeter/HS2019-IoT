#!/usr/bin/python

from sense_hat import SenseHat

import time
import socket

sense = SenseHat()


def get_ip_adress():
    ip_address = '';
    connected = False
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not connected:
        connected = True
        try:
            s.connect(("8.8.8.8", 80))
        except:
            connected = False

    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


# while True:
sense.show_message(get_ip_adress(), scroll_speed=0.2)

#!/usr/bin/python

# ToDo: Refactoring
import subprocess
import time

import paho.mqtt.client as mqtt
from sense_hat import SenseHat

from utils.display import triangel, piano, guitar, attention
from utils.functions import get_ip_adress
from utils.settings import *

# get IP-adress for identification
# ======================================================================================================================
ip_adress = get_ip_adress()

# connection to the broker
# ======================================================================================================================
client = mqtt.Client()
client.connect(settings.broker, settings.broker_port, 60)

client.loop_start()

# choose scale and synthesizer
# ======================================================================================================================
sense = SenseHat()

scale = ["C", "D", "E", "F", "G", "A", "B"]
synt = [('tri',triangel),
        ('piano', piano),
        ('guitar', guitar)]

current_synt = 0
current_note = 0
current_octave = 5

def choose_note(current_note, current_octave):
    if event.direction == "up":
        current_note += 1
        if current_note >= len(scale):
            current_note = 0
            current_octave += 1
            if current_octave > 8:
                current_octave = 0

        sense.clear()
        sense.show_letter(scale[current_note])
        for i in range(current_octave):
            sense.set_pixel(7, 7-i, (255,0,0))

    elif event.direction == "down":
        current_note -= 1
        if current_note < 0:
            current_note = len(scale) - 1
            current_octave -= 1
            if current_octave < 0:
                current_octave = 8

        sense.clear()
        sense.show_letter(scale[current_note])
        for i in range(current_octave):
            sense.set_pixel(7, 7-i, (255, 0, 0))

    return current_note, current_octave

def choose_synt(current_synt):
    if event.direction == "right":
        current_synt += 1
        if current_synt >= len(synt):
            current_synt = 0
        sense.set_pixels(synt[current_synt][1])

    elif event.direction == "left":
        current_synt -= 1
        if current_synt < 0:
            current_synt = len(synt) - 1
        sense.set_pixels(synt[current_synt][1])

    return current_synt

def check_hit(threshold):
    acceleration = sense.get_accelerometer_raw()
    # x = acceleration['x']
    # y = acceleration['y']
    z = acceleration['z']

    if abs(z) > threshold:
        return True
    else:
        return False

def send_messeage():
    sense.show_letter("X")
    send = f"{ip_adress};{scale[current_note]}{current_octave};{synt[current_synt][0]}"
    client.publish(settings.topic_sound_msg, payload=send, qos=0, retain=False)
    time.sleep(0.1)
    sense.clear()

def check_temp(max_temp):
    temp = sense.get_temperature()

    if temp > max_temp:
        return True
    else:
        return False

def shutdown_pi(sec):
    for i in reversed(range(0, sec)):
        sense.show_letter(str(i))
        time.sleep(0.5)
        sense.set_pixels(attention)
        time.sleep(0.5)

    subprocess.Popen(['shutdown', '-h', f'-t {sec}'])

sense.clear()
while True:
    for event in sense.stick.get_events():
        if event.action == "pressed":
            current_note, current_octave = choose_note(current_note, current_octave)
            current_synt = choose_synt(current_synt)

    if check_hit(threshold=1.2):
        send_messeage()

    if check_temp(max_temp=55):
        shutdown_pi(sec=10)
        break

    time.sleep(0.08)

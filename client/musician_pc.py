#!/usr/bin/python

# ToDo: Refactoring
# ToDo: Mapping a tiny piano-keyboard to the keyboard

import time

import keyboard
import paho.mqtt.client as mqtt

from utils.display import triangel, piano, guitar
from utils.functions import get_ip_adress
from utils.settings import *

client = mqtt.Client()
client.connect(settings.broker, settings.broker_port, 60)

client.loop_start()

ip_adress = get_ip_adress()

# Tonleiter und Instrument auswählen
# ======================================================================================================================

# Tonleiter
scale = ["C", "D", "E", "F", "G", "A", "H"]

# ToDo: Was ist der Unterschied zwischen B und H, weil H gibt es in Sonic Pi nicht!!!
scale[-1] = "B"
# Instrumente


synt = [triangel, piano, guitar]

current_synt = 0
current_tones = 0
octave = 5


while True:  # making a loop
    if keyboard.is_pressed('up'):  # iy 'q' is pressed
        current_tones += 1
        if current_tones >= len(scale):
            current_tones = 0
            octave += 1
            if octave > 8:
                octave = 0
        print(str(scale[current_tones]))
    elif keyboard.is_pressed('down'):  # iy 'q' is pressed
        current_tones -= 1
        if current_tones < 0:
            current_tones = len(scale) - 1
            octave -= 1
            if octave < 0:
                octave = 8
        print(str(scale[current_tones]))
    elif keyboard.is_pressed('right'):  # iy 'q' is pressed
        current_synt += 1
        if current_synt >= len(synt):
            current_synt = 0
        print(current_synt)
    elif keyboard.is_pressed('left'):  # iy 'q' is pressed
        current_synt -= 1
        if current_synt < 0:
            current_synt = len(synt) - 1
        print(current_synt)
    if keyboard.is_pressed('space'):  # if key 'space' is pressed
        send = f"{ip_adress};{scale[current_tones]}{octave};{current_synt}"
        client.publish(settings.topic_sound_msg, payload=send, qos=0, retain=False)
        print("space ")
    else:
        pass
    time.sleep(0.08)

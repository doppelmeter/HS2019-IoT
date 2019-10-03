# MQTT Settings
# ======================================================================================================================
class settings:
    pass


settings.broker = "test.mosquitto.org"
settings.broker_port = 1883
settings.topic = "FHNW2019"
settings.topic_sound_msg = settings.topic + "/sound-msg"
settings.topic_control_orchestra = settings.topic + "/ctl-orchestra"

settings.sound_param = {
    'attack': None,
    'decay': None,
    'sustain_level': None,
    'sustain': None,
    'release': None,
    'cutoff': None,
    'cutoff_attack': None,
    'amp': None,
    'pan': None
}

import socket


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

import time
import random
import keyboard
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect(settings.broker, settings.broker_port, 60)

client.loop_start()

ip_adress = get_ip_adress()

octave = 2
current_synt = "piano"
intervall = 1.2

real_live = True
anti_skills = 400

def send(tone, octave=octave, synt=current_synt, ip_adress=ip_adress):
    send = f"{ip_adress};{tone}{octave};{synt}"
    print(send)
    client.publish(settings.topic_sound_msg, payload=send, qos=0, retain=False)
    sleep(0.01)
    send = f"{ip_adress};{tone}5;{synt}"
    print(send)
    client.publish(settings.topic_sound_msg, payload=send, qos=0, retain=False)



def sleep(s):
    if real_live:
        r = random.randint(1000-anti_skills,1000+anti_skills)/1000
    else:
        r = 1
    time.sleep(s*intervall*r)

while True:
    send("C")
    sleep(0.25)
    send("D")
    sleep(0.25)
    send("E")
    sleep(0.25)
    send("F")
    sleep(0.25)
    send("G")
    sleep(0.5)
    send("G")
    sleep(0.5)
    send("A")
    sleep(0.25)
    send("A")
    sleep(0.25)
    send("A")
    sleep(0.25)
    send("A")
    sleep(0.25)
    send("G")
    sleep(0.5)
    send("A")
    sleep(0.25)
    send("A")
    sleep(0.25)
    send("A")
    sleep(0.25)
    send("A")
    sleep(0.25)
    send("G")
    sleep(0.5)
    send("F")
    sleep(0.25)
    send("F")
    sleep(0.25)
    send("F")
    sleep(0.25)
    send("F")
    sleep(0.25)
    send("E")
    sleep(0.5)
    send("E")
    sleep(0.5)
    send("D")
    sleep(0.25)
    send("D")
    sleep(0.25)
    send("D")
    sleep(0.25)
    send("D")
    sleep(0.25)
    send("C")
    sleep(0.5)
    sleep(1.5)
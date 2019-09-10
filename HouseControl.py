#!/usr/bin/python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

pin = 12;

def on_connect(client, userdata, rc, x):
    print("Connected with result code "+str(rc))
    client.subscribe("HouseControl/comando/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if(msg.payload=="liga"):
        GPIO.output(pin, 1)
    elif(msg.payload=="desliga"):
        GPIO.output(pin, 0)
    elif(msg.payload=="verifica"):
        client.publish("HouseControl/verifica", payload="Pino 7: " + str(GPIO.input(pin)), qos=1)

def on_publish(mqttc, obj, mid, x):
    print("on_publish: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos, x):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_disconnect(client, userdata, rc, x):
    print("Disconnect: " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect

client.connect("127.0.0.1", 1883, 60)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, 0)

client.loop_forever()
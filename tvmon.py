#!/usr/bin/python3

import paho.mqtt.client as mqtt #import the client1
import time,datetime
import sys
import requests
############

"""
IMPORTANT: TVs REQUIRE IP addresses, not DNS names to be used!

tv-laser.lan.makeitlabs.com has address 10.25.6.28
bkg@cgimisc:~/tvmon$ host tv-shopbot.lan.makeitlabs.com
tv-shopbot.lan.makeitlabs.com has address 10.25.9.124
"""
SHOPBOT="10.25.9.124"
LASER=="10.25.6.28"

def on_connect(client, userdata, message,data):
    print ("CONNECTED",datetime.datetime.now())
    client.subscribe("#")
    sys.stdout.flush()
def on_disconnect(client, test,data):
    print ("DICONECCTED",data,test,datetime.datetime.now())
    client.subscribe("#")
    sys.stdout.flush()
def tv_onoff(on=True):
    print ("Turn TV ",on,datetime.datetime.now())
    if on:
        r = requests.post(f"http://{LASER}:8060/keypress/PowerOn","")
        r = requests.post(f"http://{SHOPBOT}:8060/keypress/PowerOn","")
    else:
        r = requests.post(f"http://{LASER}:8060/keypress/PowerOff","")
        r = requests.post(f"http://{SHOPBOT}:8060/keypress/PowerOff","")
    print ("TV RETUREND",r.status_code,r.reason)
    sys.stdout.flush()
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    """
    print("message time " ,str(datetime.datetime.now()))
    print("message payload " ,msg)
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    """
    if (message.topic == "facility/alarm/system"):
        if msg == "armed":
            print ("ARMED")
            tv_onoff(False)
        elif msg == "disarmed":
            print ("DISARMED")
            tv_onoff(True)
        else:
            print (f"Misunderstood message \"{msg}\"")
    sys.stdout.flush()
########################################
broker_address="mqtt"
print("creating new instance")
client = mqtt.Client("tvmon") #create new instance
client.on_message=on_message #attach function to callback
client.on_connect=on_connect #attach function to callback
client.on_disconnect=on_disconnect #attach function to callback
print("connecting to broker")
client.connect(broker_address,port=2889) #connect to broker
client.subscribe("#")
#client.loop_start() #start the loop
#while True:
#	time.sleep(36000) # wait
#print ("Staring TV on")
#tv_onoff(True)
client.loop_forever(retry_first_connection=True) #stop the loop
print ("EXITED")

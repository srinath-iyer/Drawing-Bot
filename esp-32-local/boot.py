# Import Python's socket API to create the web server
try:
  import usocket as socket
except:
  import socket

# Pins for ESP-32
from machine import Pin
# enable wifi connections with ESP 32
import network
import json

# Turn off debugging messages
import esp
esp.osdebug(None)

# Garbage collector - we want to manage memory carefully as we have very little on the ESP32
import gc
gc.collect()

# Import the Bot class and create a new bot instance
import bot
robot=bot.Bot()

import os
f=open("network.txt","r") # You will need to edit the contents of network.txt for your own network.
network_info=json.loads(f.read())
print(network_info)
# Network information, change as necessary
ssid = network_info["SSID"]
password = network_info["Password"]

station = network.WLAN(network.STA_IF)

station.active(True)
if password is not "None":
    station.connect(ssid, password)
else:
    station.connect(ssid)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)


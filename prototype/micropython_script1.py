from machine import Pin
import utime
DIRECTION_X_PIN = 9
direction_x = Pin(DIRECTION_X_PIN, Pin.OUT)
step = Pin(13, Pin.OUT)
enable = Pin(10, Pin.OUT)

enable.value(0)

direction_x.value(1)

def stepOne():
  step.value(1)
  utime.sleep(0.001)
  step.value(0)


while True:
    stepOne()
    utime.sleep(0.1)

#Monitors GPIO pin 12 for input. A sound module is set up on physical pin 12.
#https://pinout.xyz/pinout/wiringpi#
import cayenne.client
import time
import datetime
import os
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SOUND_PIN = 18
GPIO.setup(SOUND_PIN, GPIO.IN)

count = 0

#Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "9b7f0060-be8c-11e7-be81-7712fc6df8b0"
MQTT_PASSWORD  = "8b69c615aaefd24a33ddcdeeeed50093724751cb"
MQTT_CLIENT_ID = "31467fb0-d477-11e7-9768-2143f8645011"

# The callback for when a message is received from Cayenne.
def on_message(message):
  print("message received: " + str(message))
  # If there is an error processing the message return an error string, otherwise return nothing.

client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

def DETECTED(SOUND_PIN):
   global count
   nowtime = datetime.datetime.now()
   count += 1

   print "Sound Detected! " + str(nowtime) + " " + str(count)
   #os.system("/home/pi/scripts/playfile.py")

   return nowtime
print "Sound Module Test (CTRL+C to exit)"
time.sleep(2)
print "Ready"

try:
   GPIO.add_event_detect(SOUND_PIN, GPIO.RISING, callback=DETECTED)
   while 1:
      time.sleep(100)
except KeyboardInterrupt:
   print " Quit"
   GPIO.cleanup()



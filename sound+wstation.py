#!/usr/bin/env python
import cayenne.client
import time
#Sound - Monitors GPIO pin 12 for input. A sound module is set up on physical pin 12.
#Sound - https://pinout.xyz/pinout/wiringpi#
import datetime
import os
import Adafruit_DHT
from RPLCD import CharLCD
#from RPLCD import CursorMode

import RPi.GPIO as GPIO
import time

# Define GPIO to LCD mapping
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13 
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11
LED_ON = 15

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

SENSOR = Adafruit_DHT.DHT22; 
PIN = 2

GPIO.setmode(GPIO.BCM)
SOUND_PIN = 18
GPIO.setup(SOUND_PIN, GPIO.IN)

count = 0

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "9b7f0060-be8c-11e7-be81-7712fc6df8b0"
MQTT_PASSWORD  = "8b69c615aaefd24a33ddcdeeeed50093724751cb"
MQTT_CLIENT_ID = "778729f0-be99-11e7-bdc0-ad7c93d4b0e5"

# The callback for when a message is received from Cayenne.
def on_message(message):
  print("message received: " + str(message))
  # If there is an error processing the message return an error string, otherwise return nothing.

#def print_data(temp, hum):
#    lcd.cursor_pos = (0, 0)
#    lcd.write_string("Temp: " + temp + unichr(223) + "C")
#    lcd.cursor_pos = (1, 0)
#    lcd.write_string("Temp: " + hum + unichr(223) + "F")

def lcd_init():
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable  
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)  
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)  


def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)      

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)   

def lcd_string(message,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified

  if style==1:
    message = message.ljust(LCD_WIDTH," ")  
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)


lcd_init();
client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

i=0
timestamp = 0

while True:
  client.loop()

  if (time.time() > timestamp + 1):

    

    # Read data from Sensor
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    #print_data(temperature, humidity)

    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Temp : " + str(round(temperature, 3))+" "+chr(223)+"C",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("Hum : " + str(round(humidity,3)) + " %",2) 
   
    #client.virtualWrite(1, temperature, "UNIT_CELSIUS", "TYPE_TEMPERATURE")
    #client.virtualWrite(2, humidity, "rel_hum", "p")
    #client.luxWrite(2, i*10)
    #client.hectoPascalWrite(3, i+800)
    #timestamp = time.time()
    #i = i+1
	
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







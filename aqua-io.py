#!/usr/bin/env python3
import Adafruit_DHT as dht  
import Adafruit_CharLCD as LCD
import time
from datetime import datetime
from time import sleep
import os
import threading
import glob
from Adafruit_IO import Client


# Import library and create instance of REST client.
from Adafruit_IO import Client, Data
aio = Client('YOUR ADAFRUIT IO USERNAME', 'YOUR ADAFRUIT IO KEY')




# Raspberry Pi pin configuration:
lcd_rs        = 27  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
#lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2
# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'



def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#CELSIUS CALCULATION
def read_temp_c():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = int(temp_string) / 1000.0 # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
        temp_c = str(round(temp_c, 1)) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL, THEN CONVERT IT TO A STRING
        return temp_c

def send_aio():
        air = aio.feeds('test1')
        aio.send_data('test.key1', temp)

        humid = aio.feeds('test2')
        aio.send_data('test2.key', humi)

        water = aio.feeds('test3')
        aio.send_data('test3.key', read_temp_c())



try:    
   while True:
        humi, temp = dht.read_retry(dht.DHT22, 4)  # Reading Humidity and Temperature
        lcd.cursor_pos = (0, 0)
        lcd.message("Tank:" + read_temp_c() + "%" + "C")
        lcd.set_cursor(0, 1)
        lcd.message(datetime.now().strftime('%H:%M'))
        lcd.set_cursor(9,1)                         # Set cursor to first line
        lcd.message('%dC' % temp)            # Print temperature on LCD
        lcd.set_cursor(13,1)                         # Set cursor on second line
        lcd.message('%d%%' % humi)           # Print Humidity on LCD
        lcd.set_cursor(0,0)
        send_aio()
        time.sleep(30)



   
  
 
except KeyboardInterrupt:
        lcd.clear()
        lcd.message("Adeus!")
        time.sleep(3)
        sys.exit()


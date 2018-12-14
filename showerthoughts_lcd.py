
import Adafruit_DHT as dht  
import Adafruit_CharLCD as LCD
import praw
import time
from datetime import datetime
from time import sleep
import os
import threading




reddit = praw.Reddit(client_id='xxxxxxxxxxx', \
                     client_secret='xxxxxxxxxx', \
                     user_agent='xxxxxxxxxxx' \
                     )


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

interval = 6000
framebuffer = [
    '',
    ]

                
                
def write_to_lcd(lcd, framebuffer, num_cols):
    lcd.home()
    for row in framebuffer:
        lcd.message(row.ljust(num_cols)[:num_cols])
        lcd.message('r\n')

#store thought to txt to limit connections to reddit
def myPeriodicFunction():
    for submission in reddit.subreddit('Showerthoughts').top(limit=1, time_filter='hour'):
        with open('showerthoughts.txt', 'w') as file:
            file.write(submission.title)
            print(submission.title, datetime.now().strftime('%H:%M'))
                
        
        
def startTimer():
    threading.Timer(interval, startTimer).start()
    myPeriodicFunction()





def loop_string(string, lcd, framebuffer, row, num_cols, delay=0.525):
    padding = ' ' * num_cols
    s = padding + string +padding
    for i in range(len(s) - num_cols + 1):
        framebuffer[row] = s[i:i+num_cols]
        write_to_lcd(lcd, framebuffer, num_cols)
        time.sleep(delay)


startTimer()


try:    
   while True:
       # Loop will run forever
       #lcd.clear()     # Clear the LCD
       long_string = open('showerthoughts.txt').read()
       humi, temp = dht.read_retry(dht.DHT22, 4)  # Reading Humidity and Temperature
       lcd.set_cursor(0, 1)
       lcd.message(datetime.now().strftime('%H:%M'))
       lcd.set_cursor(9,1)                         # Set cursor to first line
       lcd.message('%dC' % temp)            # Print temperature on LCD
       lcd.set_cursor(13,1)                         # Set cursor on second line
       lcd.message('%d%%' % humi)           # Print Humidity on LCD
       lcd.set_cursor(0,0)
       lcd.message('%s' % ( loop_string(long_string, lcd, framebuffer, 0, 16) ) )

       
# If keyboard Interrupt is pressed
except KeyboardInterrupt:
    pass         # Go to next line
lcd.clear()



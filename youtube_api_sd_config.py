"""
This program was inspired by Arduino YouTube API Library, in order to get Google Apps API key
see this link https://github.com/witnessmenow/arduino-youtube-api

Program read API Key and other configuration file from SD card
and use them to connect google API to get your Youtube channel statistics
then refresh every specific period of time as you configured it.

Written by Pongrut Palarpong


"""
from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
import urequests
import utime


# Define variable for reading data from SD card
API_KEY = None      # API_KEY
CHANNEL_ID = None   # CHANNEL_ID
REFESH_MIN = 5      # Refresh period in minutes
SOUND = 'OFF'       # Not yet use in this program

# Read config.txt from root directory of SD card
with open('/sd/config.txt', 'r') as fs:
  CHANNEL_ID = fs.readline().split('=')[1].rstrip()
  API_KEY   = fs.readline().split('=')[1].rstrip()
  REFESH_MIN = fs.readline().split('=')[1].rstrip()
  SOUND = fs.readline().split('=')[1].rstrip()


"""
# This section for test reading file from SD card and display on screen
setScreenColor(0x222222)
label0 = M5TextBox(10, 20, "API_KEY: ", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label1 = M5TextBox(10, 60, "CHANNEL_ID : ", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label2 = M5TextBox(10, 100, "REFESH_MIN: ", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label3 = M5TextBox(10, 140, "SOUND: ", lcd.FONT_Default, 0xFFFFFF, rotate=0)

label0.setText("API_KEY   : " + API_KEY)
label1.setText("CHANNEL_ID: " + CHANNEL_ID)
label2.setText("REFESH_MIN: "+REFESH_MIN)
label3.setText("SOUND     : "+SOUND)

"""


# Set background color
setScreenColor(0xFFFFFF)

# Define youtube logo image file to display
image0 = M5Img(0, 0, "res/youtube.jpg", True)
# Define text elements to show values on screen
title0 = M5Title(title="Title", x=3 , fgcolor=0xFFFFFF, bgcolor=0x0000FF)
label_youtube = M5TextBox(10, 24, "YouTube", lcd.FONT_DejaVu56, 0x000000, rotate=0)
label0 = M5TextBox(10, 100, "Subscribers:", lcd.FONT_DejaVu24, 0x000000, rotate=0)
label1 = M5TextBox(10, 171, "Views:", lcd.FONT_DejaVu24, 0x000000, rotate=0)
label_time = M5TextBox(216, 90, "000", lcd.FONT_DejaVu40, 0x000000, rotate=0)
label_subscriber = M5TextBox(10, 126, "", lcd.FONT_DejaVu40, 0xf30505, rotate=0)
label_view = M5TextBox(10, 200, "", lcd.FONT_DejaVu40, 0xf30505, rotate=0)

# Disable title which saved for display error message
title0.hide()

# Auto connecting wifi and show on screen
wifiCfg.screenShow()
wifiCfg.autoConnect(lcdShow = True)


# Function for connect google API and return statistics data
def get_current_stat():
  # Declare CHANNEL_ID & API_KEY is global variables
  global CHANNEL_ID
  global API_KEY
  # Define variables to store statistics data
  subscriber_count = 0
  video_count = 0
  view_count = 0

  # Generate google API url which contains Channel ID & API key that read from config.txt
  googleapis_url ='https://www.googleapis.com/youtube/v3/channels?part=statistics&id=' + CHANNEL_ID + '&key=' + API_KEY
  try:
    # Connect google API
    req = urequests.request(method='GET', url=googleapis_url, headers={})

    # Get response data
    res_data = req.json()['items']
    # Read viewCount, subscriberCount, videoCount
    view_count = res_data[0]['statistics']['viewCount']
    subscriber_count = res_data[0]['statistics']['subscriberCount']
    video_count = res_data[0]['statistics']['videoCount']
  except:
    # If error turn on Title and display error
    title0.show()
    title0.setTitle('Request failed.')

  # Return statistics data
  return subscriber_count, video_count, view_count

# Set timer in milisecond unit from REFESH_MIN
timer_ms = int(REFESH_MIN)*60*1000
# Read current time in milisecond
current_time = utime.ticks_ms()
# Initial first end time in milisecond
target_time = 0
# Calculate next 1 second time in milisecond
second_timer =  current_time + 1000
# Countdown counter in second
counter = int(timer_ms/1000)


while True:
  # Read current time in milisecond
  current_time = utime.ticks_ms()
  # Process every second
  if second_timer < current_time:
    # Process if time reached target end time
    if target_time < current_time:
      # Get channel statistics
      subscriber_count, video_count, view_count = get_current_stat()
      # Display youtube logo
      image0.show()
      # Display labels with data
      label0.setText("Subscribers: ")
      label_subscriber.setText('{:,}'.format(int(subscriber_count)))
      label1.setText("Views: ")
      label_view.setText('{:,}'.format(int(view_count)))
      # Calculate next end time in milisecond
      target_time = current_time + timer_ms
      # Reset counter
      counter = int(timer_ms/1000)

    # Reset second timer
    second_timer = current_time + 1000
    # Display countdown timer
    label_time.setText('{:03d}'.format(counter))
    # Decrease counter -1
    counter -= 1

# M5Stack-YouTube-Sub-Counter
YouTube Channel Subscribers on M5Stack Display.
The Program read API Key and other configuration file from SD card
and use them to connect google API to get your Youtube channel statistics
then refresh every specific period of time as you configured it.

## Find your channel's user ID & channel ID
1. Sign in to YouTube.
2. In the top right, click your profile picture and then Settings Settings.
3. From the left Menu, select Advanced settings https://www.youtube.com/account_advanced
4. You’ll see your channel’s user and channel IDs.


## Find your Google API Key
1. Go to Google Cloud Console and create a new project if you don't have one https://console.developers.google.com/
2. Type "API & Services" in the search box and then select API & Services, and go to menu Credentials https://console.developers.google.com/apis/credentials
3. Click + CREATE CREDENTIALS at the top, then select API Key.
4. Type "YouTube Data API v3" in the search box, then select API YouTube Data API v3, and "Enable" it. https://console.developers.google.com/apis/library/youtube.googleapis.com
5. Test by replacing URL with your YOUR_CHANNEL_ID and YOUR_API_KEY. You should get Channel Statistics in JSON format
https://www.googleapis.com/youtube/v3/channels?part=statistics&id=YOUR_CHANNEL_ID&key=YOUR_API_KEY


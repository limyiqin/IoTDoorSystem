from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from rpi_lcd import LCD
from picamera import PiCamera
import RPi.GPIO as GPIO
import MFRC522
import signal
import MySQLdb
from time import sleep
from datetime import datetime
import telepot
import json
import tinys3



uid = None
continue_reading = True
lcd = LCD()
unlocked = False
btn = 13
buzzer = 22
red_led = 18
green_led = 21
cardID = [47,254,122,29,182]
camera = PiCamera()
pictureURL = None

lcd.text('Launching...',1)

#Telegram
my_bot_token = 'telegram token'
bot = telepot.Bot(my_bot_token)
response = bot.getUpdates()
print(response)
#chat_ID = response[0]['message']['chat']['id']

#AWS
host="AWS Host endpoint"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"
conn = tinys3.Connection('AWS Key')

try:	
    my_rpi = AWSIoTMQTTClient("basicPubSub")
    my_rpi.configureEndpoint(host,8883)
    my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
    
    # Connect and subscribe to AWS IoT
    my_rpi.connect()
    print("Connection Succesful")	
except:	
 print("Error connecting to AWS")	

def end_read(signal,frame):
 global continue_reading
 continue_reading = False
 GPIO.cleanup()

def doorbellBuzzer():
    print("button is pressed.Sending to MQTT")
    MQTT_MSG=json.dumps({"message": "button_pressed","ImageURL":"aws s3 url"+pictureURL, "doorStatus": unlocked});
    print(MQTT_MSG)
    my_rpi.publish("sensors/Button", MQTT_MSG, 1)
    print("Message Published!")
    sleep(1)

def card(status, uid):
    print("sounding buzzer...")
    MQTT_MSG=json.dumps({"card_status": status,"cardID":str(uid),"doorStatus": unlocked});
    print(MQTT_MSG)
    my_rpi.publish("sensors/Button", MQTT_MSG, 1)
    print("Message Published!")
    sleep(1)


signal.signal(signal.SIGINT, end_read)

mfrc522 = MFRC522.MFRC522()
GPIO.output(buzzer,0)
GPIO.output(red_led,0)
GPIO.output(green_led,0)

sleep(1)

lcd.text('Getting ready',1)
lcd.text('......',2)
sleep(1)
lcd.text('Smart Doorbell',1)
lcd.text('',2)

while continue_reading:
 (status,TagType) = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)
 if status is mfrc522.MI_OK:
  (status,uid) = mfrc522.MFRC522_Anticoll()
  print ("UID of card is{}".format(uid))
  if uid == cardID: 
   if unlocked is False:
    GPIO.output(green_led,1)
    lcd.text('Door Unlocked', 1)
    lcd.text('Welcome Back!', 2)
    unlocked = True
    card("success", uid)
    sleep(0.3)
    GPIO.output(green_led,0)
    lcd.clear()   
    #add to db
    
   else:
    GPIO.output(green_led,1)
    lcd.text('Door Locked', 1)
    lcd.text('Bye Bye!', 2)
    unlocked = False
    card("success", uid)
    sleep(0.3)
    GPIO.output(green_led,0)
    lcd.clear()    
    #add to db
    
  else:
    GPIO.output(red_led,1)
    lcd.text('Wrong Card', 1)
    lcd.text('Detected!', 2)
    card("fail", uid)
    sleep(1.2)
    GPIO.output(red_led, 0) 
    lcd.clear()
    #add to db

 
 if GPIO.input(btn) == True:
  pictureURL = 'CapturedPics/photo_'+str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+'.jpg'
  if unlocked is True:
   GPIO.output(green_led, 1)
   lcd.text('Ding Dong!', 1)
   lcd.text('Wait for answer.', 2)
   doorbellBuzzer()
   camera.capture(pictureURL)
   f = open(pictureURL,'rb')
   conn.upload(pictureURL,f,'dmitiotdoorbell')
   print("Upload Done")
   GPIO.output(green_led, 0)
   lcd.clear()

  else:
   GPIO.output(red_led, 1)
   lcd.text('No One at Home', 1)
   lcd.text('Try again later', 2)
   doorbellBuzzer()
   camera.capture(pictureURL)
   f = open(pictureURL,'rb')
   conn.upload(pictureURL,f,'dmitiotdoorbell')
   print("Upload Done")
   GPIO.output(red_led, 0)
   lcd.clear()
   try:
    print("Test")
    for i in range(len(response)):
     chat_ID = response[i]['message']['chat']['id']
     bot.sendPhoto(chat_ID ,open(pictureURL,'rb'),'Someone was at your doorstep at '+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
   except e: 
    print e

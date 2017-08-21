# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from gpiozero import Buzzer,LED
from rpi_lcd import LCD
import random
import sys
import pyrebase
from datetime import datetime
import json

lcd = LCD() 
lcd.text('Launching...', 1)
sleep(1)
lcd.text('Getting ready', 1)
lcd.text('......', 2)

bz = Buzzer(22)
led = LED(18)

config = {
#Firebase API Key
    
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

#Firebase login (username, password)
user = auth.sign_in_with_email_and_password("","")
db = firebase.database()

lcd.text('Smart Doorbell', 1)
lcd.text('', 2)

# Custom MQTT message callback
def customCallback(client, userdata, message):

    print(message.payload)

    try:
        payload = json.loads(message.payload)


        if payload['card_status'] == 'success':
            timestring=str(datetime.now())
            bz.on()
            sleep(0.2)
            bz.off()
            data = {
            "type": "Card detected",
            "time": timestring,
            "status": "Success",
            "card_uid": payload['cardID'],
            "doorstatus": payload['doorStatus']
            }
            db.child('Card_Log').push(data, user['idToken'])

            if payload['doorStatus'] == False:
                db.child('Door_Status/Status').set("Locked", user['idToken'])
            else:
                db.child('Door_Status/Status').set("Unlocked", user['idToken'])
            

        if payload['card_status'] == 'fail':
            timestring=str(datetime.now())
            bz.on()
            sleep(1)
            bz.off()
            data = {
            "type": "Card detected",
            "time": timestring,
            "status": "Fail",
            "card_uid": payload['cardID'],
            "doorstatus": payload['doorStatus']
            }
            db.child('Card_Log').push(data, user['idToken'])

    except:
        payload = json.loads(message.payload)
        if payload['message'] == 'button_pressed':         
            timestring=str(datetime.now())
            if payload['doorStatus'] == True:
                bz.on()
                lcd.text('Doorbell ringing', 1)
                lcd.text('......', 2)
                led.blink()
                sleep(1)
                bz.off()
                led.off()
            sleep(3)
            data = {
            "type": "Doorbell pressed",
            "time": timestring,
            "doorstatus": payload['doorStatus'],
            "imageURL": payload['ImageURL']
            }
            print("Storing data")
            db.child('Button_Log').push(data, user['idToken'])
            sleep(2)
            lcd.text('Smart Doorbell', 1)
            lcd.text('', 2)


#host="arc9ek78m9yut.iot.us-west-2.amazonaws.com"
host="AWS Key"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

try:
    my_rpi = AWSIoTMQTTClient("indoor")
    my_rpi.configureEndpoint(host, 8883)
    my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
    my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
    my_rpi.configureMQTTOperationTimeout(5)  # 5 sec
    
    # Connect and subscribe to AWS IoT
    my_rpi.connect()
except:
    print("Unexpected error:", sys.exc_info()[0])

while True:
 my_rpi.subscribe("sensors/Button", 1, customCallback)
 buzzerStatus = db.child("Sound_Buzzer").child("Status").get(user['idToken']).val()
 if buzzerStatus == True:
    timestring=str(datetime.now())
    bz.on()
    lcd.text('Doorbell ringing', 1)
    lcd.text('......', 2)
    led.blink()
    sleep(1)
    bz.off()
    led.off()
    sleep(2)
    lcd.text('Smart Doorbell', 1)
    lcd.text('', 2)
 sleep(2)

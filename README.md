# IoTDoorSystem
The Repository for IoT Module project on Door System

## :exclamation: Introduction
The Iot-Door System is an application whereby it helps both strangers on the Door to notify
the user that someone is at the door and at the same time notify the stranger if someone is
at home. Basically how this application works is that if the user is at home and someone is 
outside the door pressing the door bell, the door bell will ring to notify the user. Then the 
system will notify the user to wait for the user to check the door.  If a situation like when 
if the stranger pressed the bell and no one is present at home. The door bell will not ring, 
but the stranger will be notified by the Displaying of message that no one is at home.
Whenever the door bell is pressed a picture and the necessary details will be recorded down 
every time someone presed the doorbell and will be stored in the database for reference and 
allows the user to check who was at the door previously. Also a telegram message will also be 
sent to the user to to notify who came and what time they came, if no one is at home. The user 
will need to tap in/tap out the card on the NFC/RFID reader to tell the system if somone is at 
home or not.

## :exclamation: Hardware Requirements:

1. 2 Raspberry Pi with Raspberry Pi Camera
2. 2 Main GPIO BreadBoard and 1 Mini BreadBoard
3. A lot of Jumper Wires(8 inside and 18 outside)[May need more wires for extension if you plan to do like what we did]
4. 2 Red LED light and 1 Green LED Light
5. 1 Buzzer
6. 1 Button
7. 3 Resistors (2 220K and 1 10K Resistors will be used)
8. 1 NFC/RFID Card Reader
9. 2 of 12C LCD Display

## :exclamation: Fritzing Diagram
Inside Raspberry Pi

 ![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/DI.png)

Outside Raspberry Pi

 ![](http://i.imgur.com/oKlq3vN.png)
 

## :exclamation: Installing Libraries

To start off please make sure you have the following items installed and enabled.

For Telegram Bot
```
sudo pip install telepot
```

For 12C LCD Display Library
```
sudo pip install rpi-lcd
```

For SPI-Py Library
```
git clone https://github.com/lthiery/SPI-Py.git
cd /home/pi/SPI-Py
sudo python setup.py install
```

For Pyrebase(Firebase SDK for Python)
```
pip install pyrebase
```

For Python Dev Libraries
```
sudo apt-get install python-dev
```

For AWS SDK
```
sudo pip install AWSIoTPythonSDK
```

For AWS s3 image uploader
```
pip install tinys3

Note: If you encounter an error saying errno13 Permission Denined, please run this code:
chmod 777 /path/of/directory/error/is/saying
```

For MQTT Subscribing and Publishing
```
sudo pip install paho‐mqtt 
```

Make sure you have also enabled Device Tree in config.txt
```
sudo nano /boot/config.txt
```
Ensure these lines are included in config.txt
```
device_tree_param=spi=on
dtoverlay=spi-bcm2835
```
**Make sure you have also enabled SPI and also Camera in sudo raspi-config**


## :exclamation: Firebase Setup


**Create a Firebase account**
Creating a Firebase account is simple. You can register using an existing Google account at https://firebase.google.com/


**Add project**
Go to https://console.firebase.google.com/, add a new project and named it “Smart Doorbell”
 ![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/1.png)

**Copy config script**
On the console, click on “Add Firebase to your web app” and take note of the scripts, you will need it later.
 ![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/2.png)
 
**Create service account**
Go to Project Settings, click on the Service Account tab > Manage all service accounts (top right), you will be directed to the page shown below, click Create Service Account.
 ![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/x.png)
The project service account json file will be downloaded. (You will have to place this file next to the python file which we will be coding later)

**Authentication**
On the console, go to Authentication>Sign-in Method, enable Email/Password.
 ![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/y.png)
 
Go to User>Add user, add a user, this will be used for self-authentication purposes later in the code.
 ![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/z.png)

## :exclamation: Amazon Web Services(AWS) S3 Bucket Setup
If you have not created an account for AWS, create one. Once you have an account, follow the steps below:

On the AWS Console, search for 's3' Click on the first one you see

![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/s3_1.JPG)

Once done, click on Create a Bucket on the left side. 

![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/s3_2.JPG)

Give a name for your bucket. I gave it as 'iotdoorbell', then click on next

![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/s3_3.JPG)

Click on next again

![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/s3_4.JPG)

On the permission page, change the 'Manage Read Permission' to 'Grant public read access to this bucket', then click on next and then finish.

![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/s3_5.JPG)


On that bucket, click on Permission Tab, then Bucket Policy.

![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/s3_6.JPG)

Paste the following json
```
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "AllowPublicRead",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::iotdoorbell/*"
        }
    ]
}
```
**Note on the Resource, i put mine as 'iotdoorbell'. Change the name to the bucket of your name**

Once done, you can create a folder called 'CapturedPics' to save all the images taken by the RPi Camera

![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/s3_7.JPG)

###### Getting Private Key
On the top, click on your account name, follow by My Security Credentials.

![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/s3_8.JPG)

On your Security Credentials Page, click on :heavy_plus_sign: next to Access Key. Once done, click on Create New Access Key. This will prompt you to download a .csv file. You **must download** it to get your secret key. Store the Access Key and Secret Key carefully

![](https://s3-ap-southeast-1.amazonaws.com/dmitiotdoorbell/Github+image+hosting/test)

## Preparing Telegram Bot

Create a Telegram Bot using BotFather. Give it a name and a username. For mine I name it
iotdoorbell_bot. Follow the steps i did below.

![](http://i.imgur.com/yZnVnxc.jpg)

Once done save the API Key in a notepad. The key will be used in the main python Start talking to your new bot by saying /start.

## :exclamation: Amazon Web Services(AWS) Message Broker Setup


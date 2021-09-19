import requests
import smtplib
import cv2
import numpy as np
import os 
import urllib.request
import RPi.GPIO as GPIO
import time
from gpiozero import Servo
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


#GPIO.setmode(GPIO.BCM)
#GPIO.setup(4,GPIO.OUT)
#GPIO.setup(18,GPIO.OUT)
#p = GPIO.PWM(4,50)
#p.start(7.5)
#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'vkwatra1703@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = '######'  #change this to match your gmail password

class Emailer:
    def sendmail(self, recipient, subject, content, image):
          
        #Create Headers
        emailData = MIMEMultipart()
        emailData['Subject'] = subject
        emailData['To'] = recipient
        emailData['From'] = GMAIL_USERNAME
 
        #Attach our text data  
        emailData.attach(MIMEText(content))
 
        #Create our Image Data from the defined image
        imageData = MIMEImage(open(image, 'rb').read(), 'jpg') 
        imageData.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
        emailData.attach(imageData)
  
        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
  
        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
  
        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, emailData.as_string())
        session.quit
  
sender = Emailer()
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['Unknown','Vansh','vansh'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:

    ret, img =cam.read()
    img = cv2.flip(img, 1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    #time.sleep(1)

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        cv2.imwrite("Storingfaces/Users."+time.ctime()+".jpg",gray[y:y+h,x:x+w])
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            cv2.imwrite("denied/Denied.Unknown" + ".jpg", gray[y:y+h,x:x+w])
            image = 'denied/Denied.Unknown.jpg'
            sendTo = 'vansh.kwatra17@gmail.com'
            emailSubject = "Unknown Person Detected!"
            emailContent = "Person detected at: " + time.ctime()
            sender.sendmail(sendTo, emailSubject, emailContent, image)
            confidence = "  {0}%".format(round(100 - confidence))
            r= requests.post('https://maker.ifttt.com/trigger/DETECT/with/key/dmOJvcQyMfI3pSU-cNBvv0')
        
        
        
      
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    #if k == 27:
    #break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()


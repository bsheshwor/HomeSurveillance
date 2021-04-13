import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage

path = 'Resources1'
images = []
Names = []
myList = os.listdir(path)
print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    Names.append(os.path.splitext(cl)[0])
print(Names)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markPerson(className):
    with open ('RecordFile.csv','r+') as f:
        myDatalist = f.readlines()
        nameList = []
        for line in myDatalist:
            entry = line.split(',')
            nameList.append(entry[0])
        if className not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{className},{dtString}')
            email_alert("System Alert!!", "Someone just trespassed your property!! ", "shresthanaruto97@gmail.com") 

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = 'gaurabstha001@gmail.com'
    msg['from'] = user
    password = 'pgvrykietyiugmxf'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()



encodeListknown = findEncodings(images)
print("Encoding Complete")


cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceLocationCurImg = face_recognition.face_locations(imgS)
    encodeCurImg = face_recognition.face_encodings(imgS, faceLocationCurImg)

    for encodeFace, faceLoc in zip(encodeCurImg, faceLocationCurImg):
        matches = face_recognition.compare_faces(encodeListknown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListknown, encodeFace)
        #print(faceDis)
        macthIndex = np.argmin(faceDis)

        if matches[macthIndex]:
            className = Names[macthIndex].upper()
            #print(className)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1,y1),(x2,y2),(0,0,255),3)
            cv2.putText(img,className,(x1+12,y2-12),cv2.FONT_ITALIC,1,(0,255,0),3)
            markPerson(className)

        else:
            className = 'Unknown Person'
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1,y1),(x2,y2),(0,0,255),3)
            cv2.putText(img,className,(x1+12,y2-12),cv2.FONT_ITALIC,1,(0,255,0),3)
            markPerson(className)
            


    cv2.imshow('Webcam', img)
    cv2.waitKey(1)

   
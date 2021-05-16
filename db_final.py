import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd
import numpy as np
from pymongo import MongoClient

# database connect
client = MongoClient(port=27017)
db= client.home_surveillance #database new
appData= db.appData


def memberentry_record(name):
    with open('data.csv', 'r+') as f:
        myDataList = f.readlines()
        namelist = []
        for line in myDataList:
            entry = line.split(',')
            namelist.append(entry[0])
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            #f.writelines(f'\n{name},{dtstring}')
        if name not in namelist:
            now = datetime.now()
            dtstring = now.strftime('%y:%m:%d:%H:%M:%S')
            f.writelines(f'\n{name},{dtstring}')



faceData=[]   #contains the entire face data dict with name, relation and the corresponding enocdings
for x in appData.find({},{ "_id": 0 }):
  faceData.append(x)
face = []  #it contains the list of arrays that are encodings of the face
# print((faceData[0]['encodings']))

# appending face encodings in list face
for i in range(len(faceData)):
    face_arr = np.zeros(128)
    for j in range(128):
        face_arr[j]=faceData[i]['encodings'][j]
    face.append(face_arr)


print('Data Extraction Complete')
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(face, encodeFace)
        faceDist = face_recognition.face_distance(face, encodeFace)
        # print(matches)
        matchIndex = np.argmin(faceDist)

        if matches[matchIndex]:
            name = faceData[matchIndex]['name'].upper()
            relation = faceData[matchIndex]['relation'].upper()
            # print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0),2)
            cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
            cv2.putText(img, relation, (x1+50,y2+50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
            memberentry_record(name)
        else:
            name = 'Unknown'
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            memberentry_record(name)
            print("Unknown member detected, Alert!!")


    cv2.imshow('webcam', img)
    cv2.waitKey(1)

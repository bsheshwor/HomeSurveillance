import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'source'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markDetect(name):
    with open('data.csv','r+') as f:
        myDataList = f.readlines()
        nameList=[]
        for line in myDataList:
            entry= line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dateStr= now.strftime("%H:%M:%S")
            f.writelines(f'\n{name},{dateStr }')

        print(myDataList)



encodeListknown = findEncodings(images)
print("Encoding Complete")
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListknown, encodeFace)
        faceDist = face_recognition.face_distance(encodeListknown, encodeFace)
        # print(faceDist)

        matchIndex = np.argmin(faceDist)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            # print(name)
            y1,x2,y2,x1= faceLoc
            y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6, y2-6),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
            markDetect(name)


    cv2.imshow('webCam', img)
    cv2.waitKey(1)


# img1 = face_recognition.load_image_file("source/elon musk.jpeg")
# img2 = face_recognition.load_image_file("source/bill gates.jpg")
# img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
# img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
#
# faceLocation = face_recognition.face_locations(img1)[0]
# faceEncoding = face_recognition.face_encodings(img1)[0]
# cv2.rectangle(img1, (faceLocation[3],faceLocation[0]), (faceLocation[1],faceLocation[2]), (255,0,255), 2)
#
# faceLocation1 = face_recognition.face_locations(img2)[0]
# faceEncoding1 = face_recognition.face_encodings(img2)[0]
# cv2.rectangle(img2, (faceLocation1[3],faceLocation1[0]), (faceLocation1[1],faceLocation1[2]), (255,255,0), 4)
#
#
# results = face_recognition.compare_faces([faceEncoding],faceEncoding1)
# faceDistance = face_recognition.face_distance([faceEncoding],faceEncoding1)
# print(results, faceDistance)
# cv2.putText(img2, f'{results} {round(faceDistance[0], 2)}',(100, 50), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0,255,0), 3)
#
# cv2.imshow('Bill Gates', img1)
# cv2.imshow('Bill Gates1', img2)
# cv2.waitKey(0)

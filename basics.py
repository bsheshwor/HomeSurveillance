import cv2
import numpy as np
import face_recognition

imgBishesh = face_recognition.load_image_file('images/bishesh.jpg')
imgBishesh = cv2.cvtColor(imgBishesh, cv2.COLOR_BGR2RGB)

imgBisheshtest = face_recognition.load_image_file('images/bishesh_test.jpg')
imgBisheshtest = cv2.cvtColor(imgBisheshtest, cv2.COLOR_BGR2RGB)

faceLoc = face_recognition.face_locations(imgBishesh)[0]
encodeBishesh = face_recognition.face_encodings(imgBishesh)[0]
cv2.rectangle(imgBishesh,(faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255,0,255), 2)

faceLocTest = face_recognition.face_locations(imgBisheshtest)[0]
encodeBisheshTest = face_recognition.face_encodings(imgBisheshtest)[0]
cv2.rectangle(imgBisheshtest,(faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255,0,255), 2)

results = face_recognition.compare_faces([encodeBishesh], encodeBisheshTest)
faceDis = face_recognition.face_distance([encodeBishesh], encodeBisheshTest)
print(results, faceDis)
cv2.putText(imgBisheshtest, f'{results}{round(faceDis[0],2)}',(50,50), cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255),2)

cv2.imshow('Bishesh', imgBishesh)
cv2.imshow('Bishesh Test', imgBisheshtest)

cv2.waitKey(0)


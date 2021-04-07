import cv2
import numpy as np
import face_recognition
import os

from pymongo import MongoClient
client = MongoClient(port=27017)

db= client.home_surveillance #database new
appData= db.appData




img1 = face_recognition.load_image_file("source/bill gates.jpg")
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

faceLocation = face_recognition.face_locations(img1)[0]
faceEncoding = face_recognition.face_encodings(img1)[0]
cv2.rectangle(img1, (faceLocation[3],faceLocation[0]), (faceLocation[1],faceLocation[2]), (255,0,255), 2)




mylist=[]

for i in range(len(faceEncoding)):
    mylist.append(faceEncoding[i])
data = {
    'name':'Bill Gates',
    'encodings':mylist
}
# appData.insert_one(data)
faceData=[]
for x in appData.find({},{ "_id": 0 }):
  faceData.append(x)

# print((faceData[0]['encodings']))
face1= np.zeros(128)
for i in range(len(faceEncoding)):
    face1[i]=faceData[0]['encodings'][i]

# print(face1.ndim)

# print(type(faceEncoding))
# print(type(face1))
# print(faceEncoding.ndim)
results = face_recognition.compare_faces([faceEncoding],face1)
faceDistance = face_recognition.face_distance([faceEncoding],face1)
print(results, faceDistance)
# cv2.waitKey(0)
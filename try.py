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




faceData=[]
for x in appData.find({},{ "_id": 0 }):
  faceData.append(x)
face = []
# print((faceData[0]['encodings']))

face1= np.zeros(128)
for i in range(128):
    face1[i]=faceData[0]['encodings'][i]

for i in range(len(faceData)):
    face_arr = np.zeros(128)
    for j in range(128):
        face_arr[j]=faceData[i]['encodings'][j]
    face.append(face_arr)



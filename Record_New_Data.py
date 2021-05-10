import cv2
from pymongo import MongoClient
import numpy as np
from datetime import datetime
import os
import face_recognition

face_cascade = cv2.CascadeClassifier('models/cascade.xml')
cam = cv2.VideoCapture(0)
cv2.namedWindow('Record New Face Data')


def insertDataToDb(name,relation,encodings):
    client = MongoClient(port=27017)
    db = client.home_surveillance  # database new

    data = {
        'name': name,
        'relation': relation,
        'encodings': encodings

    }
    appData = db.appData
    appData.insert_one(data)


while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

    cv2.rectangle(frame, ((0, frame.shape[0] - 25)), (270, frame.shape[0]), (255, 255, 255), -1)
    if(len(faces)==0):
        cv2.putText(frame, "NO Face DETECTED", (50,50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

    if (len(faces) >1):
        cv2.putText(frame, "Multiple Faces Detected!! ", (50,50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
    if not ret:
        print('Failed to grab Frame')
        break
    else:
        cv2.imshow("Record", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

        elif (k % 256 == 32) and len(faces)==0: #space key
            cv2.putText(frame, "NO Face DETECTED", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

        elif (k % 256 == 32) and len(faces) >1:  # space key
            cv2.putText(frame, "Multiple Faces Detected", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)



        elif (k % 256 == 32) and len(faces)==1: #space key
            now = datetime.now()
            dtstring = now.strftime('%y%m%d%H%M%S')
            name = input("Enter your name:")
            relation = input("Enter the relation to the person:")
            img_name = "{}_{}.png".format(name,dtstring)
            path = 'source'
            cv2.imwrite(os.path.join(path, img_name), frame)
            print("{} written!".format(img_name))

    #        compute the encodings of the facedata
            img = face_recognition.load_image_file(f"source/{img_name}")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            faceLocation = face_recognition.face_locations(img)[0]
            faceEncoding = face_recognition.face_encodings(img)[0]
            cv2.rectangle(img, (faceLocation[3], faceLocation[0]), (faceLocation[1], faceLocation[2]), (255, 0, 255), 2)

            encodingList = []

            for i in range(len(faceEncoding)):
                encodingList.append(faceEncoding[i])

            insertDataToDb(name=name, relation=relation, encodings=encodingList)
            break

cam.release()

cv2.destroyAllWindows()
import cv2
import face_recognition
import numpy as np
import smtplib
from email.message import EmailMessage
import time
import imghdr
from pymongo import MongoClient
import pygame
pygame.mixer.init()


# importing cascading model to detect face
face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')

# initializing database
client = MongoClient(port=27017)
db= client.home_surveillance #database new
appData= db.appData
imageRel= db.imageRel

# function to play sound
def play():
    pygame.mixer.music.load('static/ALert.wav')
    pygame.mixer.music.play(loops= 3)

# class to record new data
class recordData(object):
    def __init__(self):
        self.address = "http://192.168.1.9:8080/video"

        self.video = cv2.VideoCapture(self.address)


        self.no_of_faces = 0

    def __del__(self):
        self.video.release()

    def getFaces(self):
        return self.no_of_faces

    def get_frame(self):
        success, img = self.video.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.rectangle(img, ((0, img.shape[0] - 25)), (270, img.shape[0]), (255, 255, 255), -1)
        self.no_of_faces = len(faces)
        # if faces detected
        if (self.no_of_faces==1):
            cv2.imwrite('t.jpeg', img)
        # if no face detect
        if (self.no_of_faces==0):
            cv2.putText(img, "NO Face DETECTED", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
        # if detected multiple faces
        if (self.no_of_faces > 1):
            cv2.putText(img, "Multiple Faces Detected!! ", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

        cv2.waitKey(1)




        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()



# class for surveillance camera
class VideoCamera(object):
    def __init__(self):
        # self.video = cv2.VideoCapture(1)
        # self.address = "http://192.168.43.1:8080/video"
        self.address = "http://10.42.0.144:8080/video"
        self.video = cv2.VideoCapture(0)

        self.faceData = []
        for x in imageRel.find({}, {"_id": 0}):
            self.faceData.append(x)

        print("faceData")
        self.face = []
        self.namelist = []
        for i in range(len(self.faceData)):
            self.namelist.append(self.faceData[i]['name'])

        # print((faceData[0]['encodings']))

        print(self.namelist)

        for i in range(len(self.faceData)):
            face_arr = np.zeros(128)
            for j in range(128):
                face_arr[j] = self.faceData[i]['encodings'][j]
            self.face.append(face_arr)

        # self.vide.set(3, 640)
        # self.vide.set(4, 480)


    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, img = self.video.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(self.face, encodeFace)
            faceDist = face_recognition.face_distance(self.face, encodeFace)
            # print(matches)
            matchIndex = np.argmin(faceDist)

            if matches[matchIndex]:
                name = self.faceData[matchIndex]['name'].upper()
                relation = self.faceData[matchIndex]['relation'].upper()
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(img, relation, (x1 + 50, y2 + 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                self.memberentry_record(name)
            else:
                name = 'unknown'
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.imwrite('intruder.jpg', img)
                play()

                # self.memberentry_record(name)
                t = time.strftime("%Y-%m-%d_%H-%M-%S")
                print("Unknown member detected, Alert!!")

               

        cv2.waitKey(1)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()


    def memberentry_record(self, name):
        name = name.lower()
        with open('static/data.csv', 'r+') as f:
            myDataList = f.readlines()
            entryList=[]
            for line in myDataList:
                entry = line.split(',')
                entryList.append(entry[0])


            if name in self.namelist:
                if name not in entryList:
                    t = time.strftime("%Y-%m-%d_%H-%M-%S")
                    f.writelines(f'\n{name},{t}')


            elif name not in self.namelist:
                t = time.strftime("%Y-%m-%d_%H-%M-%S")
                f.writelines(f'\n{name},{t}')
                print("unknown persion recorded")

                self.email_alert("Security Alert!!","Someone just trespassed your property at " +t +"!!","shresthaumesh2056@gmail.com")




    def email_alert(self, subject, body, to):
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to

        user = 'BugDevelopers55@gmail.com'
        msg['from'] = user
        password = 'ppejebvyyyipczby'

        with open('intruder.jpg', 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name
        
        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)

        server.quit()

        print("email success")


       


        

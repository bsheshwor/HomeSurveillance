from flask import Flask, render_template, Response, request
from camera import recordData,VideoCamera
import cv2
from pymongo import MongoClient
from datetime import datetime
import numpy as np
import face_recognition
import os

app = Flask(__name__)

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

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/new')
def index():
    return render_template('index.html')


@app.route('/new/record')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/newnew')
def indexindex():
    return render_template('record.html')


@app.route('/newnew/record')
def recordrecord():
    return Response(gen(recordData()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/takeimage', methods = ['POST'])
def takeimage():
    name = request.form['name']
    relation = request.form['relation']
    print(type(name))
    imgToSave = cv2.imread('t.jpeg')
    now = datetime.now()
    dtstring = now.strftime('%y%m%d%H%M%S')

    img_name = "{}_{}.png".format(name, dtstring)
    path = 'source'
    cv2.imwrite(os.path.join(path, img_name), imgToSave)
    print("{} written!".format(img_name))

    #        compute the encodings of the facedata
    img = face_recognition.load_image_file('t.jpeg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceLocation = face_recognition.face_locations(img)[0]
    faceEncoding = face_recognition.face_encodings(img)[0]
    cv2.rectangle(img, (faceLocation[3], faceLocation[0]), (faceLocation[1], faceLocation[2]), (255, 0, 255), 2)

    encodingList = []

    for i in range(len(faceEncoding)):
        encodingList.append(faceEncoding[i])

    insertDataToDb(name=name, relation=relation, encodings=encodingList)


    return Response(status=200)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

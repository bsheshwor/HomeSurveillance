from flask import Flask, render_template, Response
from camera import recordData,VideoCamera

app = Flask(__name__)


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



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

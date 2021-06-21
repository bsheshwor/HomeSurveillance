from flask import Flask, render_template, Response, request, redirect, session, url_for
from camera import recordData,VideoCamera
import cv2
from pymongo import MongoClient
from datetime import datetime
import face_recognition
import os
import bcrypt
from flask_bcrypt import Bcrypt
import pandas as pd
import flask_admin as admin
from wtforms import form, fields, validators
from flask_admin.contrib.pymongo import ModelView, filters
from latestclass import Images



app = Flask(__name__)
KEY = os.urandom(24)
app.config["SECRET_KEY"] = KEY
client = MongoClient(port=27017)
db = client.home_surveillance  # database new
records = db.records
bcrypt = Bcrypt(app)

# forms
class UserForm(form.Form):
    user = fields.StringField("Name")
    email = fields.StringField("Email")
    password = fields.PasswordField(
        "Password",
        validators=[validators.DataRequired()],
        filters=[lambda x: bcrypt.generate_password_hash(x).decode("utf-8")],
    )
    relation = fields.StringField("Relation")




def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/video')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/record')
def indexindex():
    return render_template('record.html')


@app.route('/record/new')
def recordrecord():
    return Response(gen(recordData()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/takeimage', methods = ['POST'])
def takeimage():
    name = request.form['name']
    relation = request.form['relation']
    address = request.form['address']
    phone = request.form['phone']
    print(type(name))
    imgToSave = cv2.imread('t.jpeg')
    now = datetime.now()
    dtstring = now.strftime('%y%m%d%H%M%S')
    # clearing directory
    
    img_name = "{}_{}.png".format(name, dtstring)
    path = 'source/'
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
    
    new = Images()

    new.insertDataToDb(name=name,path=path,tempfile= img_name,relation=relation,address=address,phone=phone,filename="t.jpeg", encodings=encodingList)
    dir = 'source'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    os.remove('t.jpeg')


    return Response(status=200)

@app.route("/", methods=["post", "get"])
def base():
    if "email" in session:
        email = session["email"]
        relation = session["relation"]

        return render_template("base.html", email=email, relation=relation)
    else:
        return redirect(url_for("login"))


@app.route("/index", methods=["post", "get"])
def index():
    if "email" in session:
        email = session["email"]
        relation = session["relation"]

        return render_template("index.html", email=email, relation= relation)


@app.route("/register", methods=["post", "get"])
def reg():
    message = ""
    myform = UserForm
    if "email" in session:
        return redirect(url_for("base"))

    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        relation = "member"
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"user": user})
        email_found = records.find_one({"email": email})
        relation_found = records.find_one({"relation": relation})

        if user_found:
            message = "There already is a user by that name"
            return render_template("register.html", message=message)
        if email_found:
            message = "This email already exists in database"
            return render_template("register.html", message=message)
        if password1 != password2:
            message = "Passwords should match!"
            return render_template("register.html", message=message)
        else:
            hashed = bcrypt.generate_password_hash(password2).decode("utf-8")
            user_input = {
                "user": user,
                "relation": relation,
                "email": email,
                "password": hashed,
            }
            records.insert_one(user_input)

            user_data = records.find_one({"email": email})
            new_email = user_data["email"]

            return render_template("base.html", email=new_email)
    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    message = ""
    if "email" in session:
        return redirect(url_for("base"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # pass_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        # print(pass_hash)
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found["email"]
            passwordcheck = email_found["password"]
            relation = email_found["relation"]

            if bcrypt.check_password_hash(passwordcheck, password):
                session["email"] = email_val
                session["relation"] = relation
                return redirect(url_for("index"))
            else:
                if "email" in session:
                    return redirect(url_for("index.html"))
                message = "Wrong password"
                return render_template("login.html", message=message)
        else:
            message = "Email not found"
            return render_template("login.html", message=message)
    return render_template("login.html")


@app.route("/signout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("base.html")
    else:
        return render_template("register.html")


@app.route("/newentry", methods=["post", "get"])
def newent():
    if "email" in session:
        email = session["email"]
        realtion = session["relation"]
        return render_template("newentry.html", email=email, relation = realtion)

@app.route('/csv', methods=['GET', 'POST'])
def csvfile():
    if "email" in session:
        email = session["email"]
        relation = session["relation"]
        dict_from_csv = pd.read_csv('static/data.csv', header=None, index_col=0, squeeze=True).to_dict()
        #df = pd.read_csv('static/data.csv')
        #db.csvdata.insert_one(dict_from_csv)
        return render_template('csv.html', email=email,relation=relation, data=dict_from_csv)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if "email" in session:
        email = session["email"]
        relation = session["relation"]
        if request.method == "POST":
            query = request.form.get("search")
            img = Images()
            details=img.queryData(query)
            print(query)
            file = "images/"+query+".jpeg"
            print(file)
            if details:
                return render_template('search.html',file= file, email=email, relation = relation, details = details)
    return render_template('search.html',email=email, relation = relation)



# Flask views
@app.route("/admin")
def adminPanel():
    return '<a href="/admin/">Click me to get to Admin!</a>'

class UserView(ModelView):
    column_list = ("user", "email", "relation", "password")
    column_sortable_list = ("user", "email", "relation", "password")
    # column_exclude_list = ['password']

    form = UserForm



if __name__ == '__main__':
    admin = admin.Admin(app, name="Home_Surveillance")
    admin.add_view(UserView(records, "User"))

    app.run(host='0.0.0.0', debug=True)
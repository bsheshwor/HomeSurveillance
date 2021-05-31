from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt
from flask_bcrypt import Bcrypt

from pymongo import MongoClient
from datetime import datetime
import os
from bson.objectid import ObjectId
import flask_admin as admin
from wtforms import form, fields, validators
from flask_admin.form import Select2Widget
from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.model import BaseModelView
from flask_admin.model.fields import InlineFormField, InlineFieldList

app = Flask(__name__)
KEY= os.urandom(24)
app.config['SECRET_KEY'] = KEY
client = MongoClient(port=27017)
db = client.home_surveillance
records = db.records
bcrypt = Bcrypt(app)


class UserForm(form.Form):
    user = fields.StringField('Name')
    email = fields.StringField('Email')
    password = fields.PasswordField('Password',validators=[validators.DataRequired()],filters=[lambda x: bcrypt.generate_password_hash(x).decode('utf-8')])
    relation = fields.StringField('Relation')

@app.route("/", methods=['post', 'get'])
def base():
    if "email" in session:
        email = session["email"]
        return render_template('base.html', email=email)
    else:
        return redirect(url_for("login"))

@app.route("/index", methods=['post', 'get'])
def index():
    if "email" in session:
        email = session["email"]
        return render_template('index.html', email=email)

@app.route("/register", methods=['post', 'get'])
def reg():
    message = ''
    myform = UserForm
    if "email" in session:
        return redirect(url_for("base"))

    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        relation = request.form.get("relation")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"user": user})
        email_found = records.find_one({"email": email})
        relation_found = records.find_one({"relation": relation})

        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)
        else:
            hashed = bcrypt.generate_password_hash(password2).decode('utf-8')
            user_input = {'user': user,'relation':relation,'email': email, 'password': hashed}
            records.insert_one(user_input)

            user_data = records.find_one({"email": email})
            new_email = user_data['email']


            return render_template('base.html', email=new_email)
    return render_template('register.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    message = ''
    if "email" in session:
        return redirect(url_for("base"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        #pass_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        #print(pass_hash)
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            print(passwordcheck)
            if bcrypt.check_password_hash(passwordcheck,password):
                session["email"] = email_val
                return redirect(url_for('base'))
            else:
                if "email" in session:
                    return redirect(url_for("base.html"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html')

@app.route("/signout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("base.html")
    else:
        return render_template('register.html')


@app.route("/newentry", methods=['post', 'get'])
def newent():
    if "email" in session:
        email = session["email"]
        return render_template('newentry.html', email=email)


@app.route('/csv', methods=['GET', 'POST'])
def csvfile():
    if "email" in session:
        email = session["email"]
        return render_template('csv.html', email=email)

class UserView(ModelView):
    column_list = ('user', 'email', 'relation','password')
    column_sortable_list = ('user', 'email','relation','password')
    #column_exclude_list = ['password']

    form = UserForm

# Flask views
@app.route('/admin')
def adminPanel():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ == '__main__':
    admin = admin.Admin(app, name='Home_Surveillance')
    admin.add_view(UserView(records, 'User'))

    # Start app
    app.run(host='0.0.0.0',port='3030',debug=True)

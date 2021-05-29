from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt
import csv


app = Flask(__name__)
# database connect
client = pymongo.MongoClient(port=27017)
db= client.home_surveillance #database new
records = db.records


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
    if "email" in session:
        return redirect(url_for("base"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
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
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
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

       
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
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
    


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
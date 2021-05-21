from flask import render_template, url_for, flash, redirect, request, abort
from forms import RegistrationForm, LoginForm, MemberDataForm
from models import User, Members
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask
from flask_mongoengine.wtf import model_form
from flask_bcrypt import Bcrypt
from flaskApp import login_manager
from flask_sqlalchemy import SQLAlchemy
from . import admin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'd34ff4afb6567b186258533d28956412'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#TODO: CONNECT THE MONGODB
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

def check_admin():
    """
    Prevent non-admins from accessing the page
    :return:
    """
    if not current_user.is_admin:
        abort(403)

# Members' Data Views


@admin.route('/members', methods=['GET', 'POST'])
@login_required
def list_members():
    """
    List all members
    """
    check_admin()

    members = Members.query.all()

    return render_template('members.html',
                           members=members, title="Members")


@app.route('/members/add', methods=['GET', 'POST'])
@login_required
def add_members():
    """
    Add a member to the database
    """
    check_admin()

    add_member = True

    form = MemberDataForm()
    if form.validate_on_submit():
        members = Members(name=form.name.data,
                             relation=form.relation.data,
                             image = form.image.data)
        try:
            # add department to the database
            db.session.add(members)
            db.session.commit()
            flash('You have successfully added a new members.')
        except:
            # in case members' name already exists
            flash('Error: Member name already exists.')

        # redirect to departments page
        return redirect(url_for('list_members'))

    # load members template
    return render_template('member.html', action="Add",
                           add_member=add_member, form=form,
                           title="Add Member")


@app.route('/members/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_members(id):
    """
    Edit a member
    """
    check_admin()

    add_member = False

    member = Members.query.get_or_404(id)
    form = MemberDataForm(obj=member)
    if form.validate_on_submit():
        member.name = form.name.data
        member.relation = form.relation.data
        db.session.commit()
        flash('You have successfully edited the member data.')

        # redirect to the departments page
        return redirect(url_for('list_members'))

    form.relation.data = member.relation
    form.name.data = member.name
    return render_template('member.html', action="Edit",
                           add_member=add_member, form=form,
                           member=member, title="Edit Member")


@app.route('/members/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_member(id):
    """
    Delete a member from the database
    """
    check_admin()

    member = Members.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash('You have successfully deleted a member.')

    # redirect to the departments page
    return redirect(url_for('list_members'))

    return render_template(title="Delete Member")

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} is created! You can now login', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form = form)

@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.is_admin:
            return redirect(url_for('admin_dashboard'))
        elif user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title = 'Account')

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    #prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('admin_dashboard.html', title="Dashboard")



if __name__=="__main__":
    app.run(debug=True)
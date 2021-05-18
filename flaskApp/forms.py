from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    """Registration Form"""
    username = StringField('Username',
                           validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators =[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data)
        if user:
            raise ValidationError('Username Already Exists. Please choose another username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data)
        if user:
            raise ValidationError('That email is taken. Please choose another email address.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=username.email)
    #     if user:
    #         raise ValidationError('That email is taken. Please choose another email address.')


class LoginForm(FlaskForm):
    """Login Form"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
from flask_uploads import IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, EqualTo, DataRequired, Email


class RegisterForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired('A full name is required.'),
                                                Length(max=100,
                                                       message='Your name can\'t be more than 100 characters.')])
    email = EmailField('Email', validators=[InputRequired('Email is required.'),
                                            Length(max=30, message='Your username is too many characters.')])

    password = PasswordField('Password',
                             validators=[InputRequired('A password is required.'),
                                         EqualTo('confirm_password', message='Password must match')])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired()])

    image = FileField(validators=[FileAllowed(IMAGES, 'Only images are accepted.')])


class LoginForm(FlaskForm):
    email = EmailField('Email',
                       validators=[InputRequired('A password is required.'),
                                   Email()])
    password = PasswordField('Password',
                             validators=[InputRequired('A password is required.')])
    remember = BooleanField('Remember me')

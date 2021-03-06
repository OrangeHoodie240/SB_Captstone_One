from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SelectField, FieldList, FormField
from wtforms.validators import InputRequired, Optional, Length, Email
import re

class RegisterForm(FlaskForm):

    username = StringField("Username: ", validators=[InputRequired(message='Must specify username'), Length(min=9, max=30, message='Must be between 9 and 30 characters')])
    password = PasswordField('Password: ', validators=[InputRequired(message="Must specify password"), Length(min=9, max=30, message='Must be between 9 and 30 characters')])
    email = StringField('Email: ', validators=[Email(message='Must be valid email'), Length(min=3, message='Email too short'), InputRequired(message='Must specify email')])

class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[InputRequired(message='Must specify username'), Length(min=9, max=30, message='Must be between 9 and 30 characters')])
    password = PasswordField('Password: ', validators=[InputRequired(message="Must specify password"), Length(min=9, max=30, message='Must be between 9 and 30 characters')])


class WorkoutForm(FlaskForm):
    name = StringField("Name: ", validators=[InputRequired(message='Must specify name'), Length(max=30, message='Max of 30 characters')])

class DayForm(FlaskForm):
    weekday = SelectField('Day Of Week', validators=[InputRequired(message='Must specify day')])


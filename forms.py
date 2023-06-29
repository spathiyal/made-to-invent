from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email, Length,Optional,InputRequired

class UserForm(FlaskForm):
    """Form to add new user"""

    firstname = StringField('First Name',validators=[InputRequired(message="First Name is required")])
    middlename = StringField('Middle Name',validators=[Optional()])
    lastname = StringField('Last Name',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8)])

class LoginForm(FlaskForm):
    """Login form """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
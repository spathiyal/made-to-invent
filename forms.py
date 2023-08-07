from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email, Length,Optional,InputRequired

class UserForm(FlaskForm):
    """Form to add new user"""

    firstname = StringField('First Name',validators=[InputRequired(message="First Name is required")],description="Required Field")
    middlename = StringField('Middle Name',validators=[Optional()],description="Optional")
    lastname = StringField('Last Name',validators=[DataRequired()],description="Required Field" )
    email = StringField('Email', validators=[DataRequired(), Email()]  ,description="Enter valid email. Required Field" )
    username = StringField('Username', validators=[DataRequired()],description="Required Field" )
    password = PasswordField('Password', validators=[Length(min=6)],description="Minimum 6 characters required")

class LoginForm(FlaskForm):
    """Login form """

    username = StringField('Username', validators=[DataRequired()],description="Required Field" )
    password = PasswordField('Password', validators=[DataRequired()],description="Required Field" )


class PatentForm(FlaskForm):
    """Form to add new patent"""

    patent_number = StringField('Patent Number',validators=[InputRequired(message="Patent Number is required")])

class InventorForm(FlaskForm):
    """Form to add new inventor"""

    firstname = StringField('First Name',validators=[InputRequired(message="First name is required")])
    lastname = StringField('Last Name',validators=[InputRequired(message="Last name is required")])


from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import text
from datetime import datetime


db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)



    with app.app_context():
        db.drop_all()
        db.create_all()


class User(db.Model):
    """user table model"""
    __tablename__ = "users"
    username = db.Column(db.String(20), primary_key=True,  unique=True)
    password = db.Column(db.Text, nullable=False)

    firstname = db.Column(db.String(30), nullable=False)
    middlename = db.Column(db.String(30), nullable=True)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(30), nullable=True)

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.firstname} {self.lastname}"

    @classmethod
    def newUserSignUp(cls, firstname, middlename, lastname, email, username, password):
        """Create new user."""
        # https://flask-bcrypt.readthedocs.io/en/1.0.1/ - for reference
        pwhash = Bcrypt().generate_password_hash(password).decode("utf-8")

        # return user info, username and password
        return cls(firstname=firstname, middlename=middlename, lastname=lastname, email=email, username=username, password=pwhash)

    @classmethod
    def login(cls, username, password):
        """Validate if the login user exists & password is correct.  Return user if valid; else return False. """

        user = User.query.filter_by(username=username).first()

        if user and Bcrypt().check_password_hash(user.password, password):
            # return user instance

            return user
        else:

            return False


class Patent(db.Model):
    """user table model"""
    __tablename__ = "patents"
    patent_number = db.Column(db.Text, primary_key=True,  unique=True)
    patent_title = db.Column(db.Text,
                          nullable=False)
    issued_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )
    username = db.Column(db.String(20) )
    iventions = db.relationship('InventorPatent',backref='patent')
    @classmethod
    def addPatentToList(cls, patent_number):
        """add new patent info."""

        # return patent info
        return cls(patent_number=patent_number)



class Inventor(db.Model):
    """Project. Employees can be assigned to this."""
    __tablename__ = "inventors"
    inventor_id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    inventor_name = db.Column(db.Text,
                          nullable=False)
    username = db.Column(db.String(20) )

    patents = db.relationship('Patent',secondary = 'inventors_patents',backref = 'inventors')
    iventions = db.relationship('InventorPatent',backref='inventorß')


class InventorPatent(db.Model):
    """Mapping of an employee to a project."""
    __tablename__ = "inventors_patents"

    inventor_id = db.Column(db.Integer,
                       db.ForeignKey("inventors.inventor_id"),
                       primary_key=True)
    patent_number = db.Column(db.Text,
                          db.ForeignKey("patents.patent_number"),
                          primary_key=True)

    username = db.Column(db.Text,
                          db.ForeignKey("users.username"),
                          primary_key=True)




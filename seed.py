"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
new_user = User(firstname="Shyla", middlename=None, lastname="Pathiyal", email="spathiyal@gmail.com" ,username="username", password="password")


db.session.commit()

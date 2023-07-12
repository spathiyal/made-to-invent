from flask import Flask, request, redirect, render_template, flash, g, session
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from email_validator import validate_email
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from models import db, connect_db, User,Patent,Inventor, InventorPatent
from forms import UserForm, LoginForm,PatentForm,InventorForm
from secrets_1 import API_SECRET_KEY
import requests

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///made_to_invent_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
bcrypt = Bcrypt(app)
connect_db(app)

API_BASE_URL = 'https://api.patentsview.org/patents'

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True


# toolbar = DebugToolbarExtension(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.username


def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    return redirect('/')


@app.route('/')
def home_page():
    return render_template("home.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserForm()
    if form.validate_on_submit():
        # is this post request and valid?
        try:
            new_user = User.newUserSignUp(
                firstname=form.firstname.data,
                middlename=form.middlename.data,
                lastname=form.lastname.data,
                email=form.email.data,
                username=form.username.data,
                password=form.password.data
            )

            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:

            flash(f"User {new_user.username} already exists.")
            return render_template('signup.html', form=form)
        do_login(new_user)
        return redirect('/dashboard')

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        auth_user = User.login(form.username.data,
                               form.password.data)

        if auth_user:
            do_login(auth_user)
            flash(f"Hello, {auth_user.username}!", "success")
            return redirect('/dashboard')
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash("Invalid password.")
        if not user:
            flash("Invalid username.")

    return render_template('/login.html', form=form)

@app.route('/inventor')
def inventor_list():
    return render_template("/inventor-list.html")

@app.route('/<int:id>/edit', methods=["GET", "POST"])
def edit(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        firstname = form.firstname.data,
        middlename = form.middlename.data,
        lastname = form.lastname.data,
        email = form.email.data
        db.session.commit()
        return redirect("/")
    else:
        return render_template("edit.html", form=form)


# test from https://python-adv-web-apps.readthedocs.io/en/latest/flask_db2.html
@app.route('/dbcheck')
def testdb():
    try:
        # db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        inventors = db.session.execute(db.select(User)
                                       .order_by(User.firstname)).scalars()

        inventor_text = '<ul>'
        for inventor in inventors:
            inventor_text += '<li>'+',' + inventor.firstname + ', ' + inventor.lastname + \
                ', ---  ' + inventor.username + ', ---  '+inventor.password + '</li>'
        inventor_text += '</ul>'
        return inventor_text
        # return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text




@app.route('/addpatent', methods=["GET", "POST"])
def add_patents():
    form = PatentForm()
    if form.validate_on_submit():
        patent_number = form.patent_number.data
        # patent_number = request.args["patent_number"]

        url = f"{API_BASE_URL}/query?q={{\"patent_number\": {patent_number}}}&f=[\"patent_number\",\"patent_title\",\"patent_date\",\"inventor_first_name\" ,\"inventor_last_name\" , \"inventor_key_id\"  ]"

        resp = requests.get(url)

        data = resp.json()
        for patent in data['patents']:
            patent_number = patent['patent_number']
            patent_title = patent['patent_title']
            issued_date = patent['patent_date']
            isInthePatentTable = Patent.query.filter_by(patent_number=  patent['patent_number']).first()
            if(isInthePatentTable == None):

                p = Patent(patent_number = patent_number, patent_title = patent_title, issued_date = issued_date, username = session[CURR_USER_KEY])
                db.session.add(p)
                db.session.commit()
                inventors = patent['inventors']
                for inventor in inventors:

                    name = inventor['inventor_first_name'] + " " + inventor['inventor_last_name']

                    inventor_id = inventor['inventor_key_id']
                    isIntheInventorList = Inventor.query.filter_by( inventor_id = inventor['inventor_key_id']).first()
                    if(isIntheInventorList == None):
                        i = Inventor(inventor_name = name ,inventor_id = inventor_id, username = session[CURR_USER_KEY])
                        db.session.add(i)
                        db.session.commit()
                        isIntheInvPatTable = InventorPatent.query.filter_by(patent_number=  patent['patent_number'],inventor_id = inventor['inventor_key_id']).first()
                        if(isIntheInvPatTable == None):
                          ip =  InventorPatent(patent_number = patent_number , inventor_id = inventor_id, username = session[CURR_USER_KEY])
                          db.session.add(ip)
                          db.session.commit()

        # patents = get_patent(patent_number)
        # addPatent= Patent(patent_number=patents["patent_number"],patent_name=patents["patent_name"] ,title=patents["title"])

        return redirect('/dashboard')
    else:
        return render_template('add-patents.html', form=form)

@app.route('/dashboard')
def dashboard():
     getAllPatents = InventorPatent.query.filter_by(username= session[CURR_USER_KEY] ).all()



     patents = Patent.query.all()
     inventors_patents = InventorPatent.query.all()

     inventors = Inventor.query.all()



     return render_template("inventor-list.html", patents=patents,inventors=inventors ,inventors_patents = inventors_patents ,getAllPatents= getAllPatents )





@app.route('/addinventor', methods=["GET", "POST"])
def add_inventors():
    form = InventorForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data


        # url = f"{API_BASE_URL}/query?q={{\"_contains\":{{\"inventor_last_name\": \"{lastname}\"}}}}&f=[\"patent_number\",\"patent_title\",\"patent_date\",\"inventor_first_name\" ,\"inventor_last_name\" , \"inventor_key_id\"  ]"
        url = f"{API_BASE_URL}/query?q={{\"_and\":[{{\"_contains\":{{\"inventor_last_name\": \"{lastname}\"}}}},{{\"_contains\":{{\"inventor_first_name\": \"{firstname}\"}}}}]}}&f=[\"patent_number\",\"patent_title\",\"patent_date\",\"inventor_first_name\" ,\"inventor_last_name\" , \"inventor_key_id\"]"

        resp = requests.get(url)

        data = resp.json()
        for patent in data['patents']:
            patent_number = patent['patent_number']
            patent_title = patent['patent_title']
            issued_date = patent['patent_date']
            isInthePatentTable = Patent.query.filter_by(patent_number=  patent['patent_number']).first()
            if(isInthePatentTable == None):

                p = Patent(patent_number = patent_number, patent_title = patent_title, issued_date = issued_date, username = session[CURR_USER_KEY])
                db.session.add(p)
                db.session.commit()
                inventors = patent['inventors']
                for inventor in inventors:

                    name = inventor['inventor_first_name'] + " " + inventor['inventor_last_name']

                    inventor_id = inventor['inventor_key_id']
                    isIntheInventorList = Inventor.query.filter_by( inventor_id = inventor['inventor_key_id']).first()
                    if(isIntheInventorList == None):
                        i = Inventor(inventor_name = name ,inventor_id = inventor_id, username = session[CURR_USER_KEY])
                        db.session.add(i)
                        db.session.commit()
                        # isIntheInvPatTable = InventorPatent.query.filter_by(patent_number=  patent['patent_number'],inventor_id = inventor['inventor_key_id']).first()
                        # raise
                        # if(isIntheInvPatTable == None):
                    ip =  InventorPatent(patent_number = patent_number , inventor_id = inventor_id, username = session[CURR_USER_KEY])

                    db.session.add(ip)
                    db.session.commit()

        # patents = get_patent(patent_number)
        # addPatent= Patent(patent_number=patents["patent_number"],patent_name=patents["patent_name"] ,title=patents["title"])

        return redirect('/dashboard')
    else:
        return render_template('add-inventors.html', form=form)


@app.route('/<int:patent_number>' , methods=["GET", "POST"])

def show_patent_info(patent_number):



    url = f"{API_BASE_URL}/query?q={{\"patent_number\": {patent_number}}}&f=[\"patent_number\",\"patent_title\",\"patent_date\",\"inventor_first_name\" ,\"inventor_last_name\" , \"inventor_key_id\" ,\"app_date\"  ]"

    resp = requests.get(url)

    data = resp.json()

    for patent in data['patents']:
        patent_number = patent['patent_number']
        patent_title = patent['patent_title']
        issued_date = patent['patent_date']

        application = patent['applications']


        filing_date = application[0]['app_date']

        inventors = patent['inventors']
        for inventor in inventors:

            name = inventor['inventor_first_name'] + " " + inventor['inventor_last_name']

    return render_template("patent-info.html", patent_number=patent_number,patent_title=patent_title,issued_date=issued_date  ,inventors = inventors , filing_date = filing_date)
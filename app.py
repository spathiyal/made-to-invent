from flask import Flask, request, redirect, render_template,flash,g,session
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from email_validator import validate_email
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from models import db, connect_db, User
from forms import UserForm, LoginForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///made_to_invent_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
bcrypt = Bcrypt(app)
connect_db(app)


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



@app.route('/signup',methods=["GET","POST"])

def signup():
    form = UserForm()
    if form.validate_on_submit():
        # is this post request and valid?
        try:
            new_user = User.newUserSignUp(
            firstname   = form.firstname.data,
            middlename  = form.middlename.data,
            lastname    = form.lastname.data,
            email       = form.email.data,
            username    = form.username.data,
            password    = form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            flash(f"User {new_user.username} already exists.")
            return render_template('signup.html', form=form)

        return render_template("inventor-list.html")
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
            return render_template('/inventor-list.html',user=auth_user)
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash("Invalid password.")
        if not user:
            flash("Invalid username.")


    return render_template('/login.html', form=form)

@app.route('/<int:id>/edit',methods=["GET","POST"])
def edit(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        firstname   = form.firstname.data,
        middlename  = form.middlename.data,
        lastname    = form.lastname.data,
        email       = form.email.data
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
            inventor_text += '<li>'+',' + inventor.firstname + ', ' + inventor.lastname+ ', ---  ' + inventor.username + ', ---  '+inventor.password +'</li>'
        inventor_text += '</ul>'
        return inventor_text
        # return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
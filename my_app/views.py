# from flask import  render_template

# from . import db, app, rbac

# @app.route('/')
# @rbac.exempt
# def index():
#     return "<html> Hello </html>"

# @app.route('/login', methods=['GET'])
# @rbac.exempt
# def login():
#     return render_template('login.html')


from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, rbac,app




@app.route('/login', methods=['GET'])
@rbac.exempt
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
@rbac.exempt
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.find_by_email(email)

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)

    return redirect(url_for('profile'))

@app.route('/signup')
@rbac.exempt
def signup():

    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
@rbac.exempt
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.find_by_email(email) # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    new_user.save_to_db()
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# main

@app.route('/')
@rbac.exempt
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
@rbac.exempt
def profile():
    return render_template('profile.html', name=current_user.name)

@app.route('/admin', methods=['GET'])
@login_required
@rbac.allow(['admin'], methods=['GET'])
def admin_page():
    return render_template('profile.html', name=current_user.name)
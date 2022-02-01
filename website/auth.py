import sqlite3
import imp
from unicodedata import name
from flask import Blueprint, render_template, request, redirect, url_for, flash
from matplotlib.style import use
import pyautogui as py
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # py.alert(text='', title='', button='OK')
    # data = request.form
    # print(data)
    tries = 0

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged In Succesfully!!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid Password.', category='error')

        else:
            flash('User Does not exist.', category='error')

    return render_template('login.html', user=current_user)


@ auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@ auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # data = request.form
    # print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email aldready exists.', category='error')
        if len(email) < 4:
            flash('Email must be greater than 4 charecters.', category='error')
            pass
        elif len(password1) < 6:
            flash('Password must be greater than 6 charecters.', category='error')
            pass
        elif password1 != password2:
            flash('Passwords do not match', category='error')
            pass
        elif len(first_name) < 2:
            flash('Name cannot be less than 2 charecters', category='error')
            pass
        else:
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

            # db.session.commit()
            login_user(user, remember=True)
            flash('User added successfully', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


# @auth.route('/home')
# def home():
#     return render_template("home.html")

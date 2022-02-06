import sqlite3
import imp
from unicodedata import name
from flask import Blueprint, render_template, request, redirect, url_for, flash
from matplotlib.style import use
import pyautogui as py
from .models import User, Note
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from .py_ocr import ocr as image_to_text
from .webcam import theft_detection as cam
from .Pyt_mailer import send_mail
auth = Blueprint('auth', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def forgetpassword():
    # py.alert(text='', title='', button='OK')
    py.prompt(
        text='', title='Enter the Access key sent to your Email/phone', default='')

    # use tkinter or pyqt insted of pyautogui
    # email verification using the same access key
    # gui for entering email and keyy
    # enter the key and validate if validated
    #
    # redirect to login page




@auth.route('/login', methods=['GET', 'POST'])
def login():

    # py.alert(text='', title='', button='OK')
    # data = request.form
    # print(data)

    if request.method == 'POST':

        if request.form.get('action1') == 'Login':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()

            if user:
                if check_password_hash(user.password, password):
                    flash(f"{user.first_name} has been logged In Succesfully!!",
                          category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    cam()
                    send_mail(email, 'Intruder Alert!')
                    flash('Invalid Password.', category='error')

            else:
                flash('User Does not exist.', category='error')
        elif request.form.get('action2') == 'Forget Password':
            forgetpassword()
            pass
    # user = User.query.all()
    # for i in user:
    #     print(i.first_name)
    #     print(i.email)
    #     print(i.password)
    #     print(i.id)
    # user2 = Note.query.all()
    # for i in user2:
    #     print(i.data)
    #     print(i.data_amt)
    #     print(i.date)
    #     print(i.user_id)
    # print(User.query.all())
    # print(Note.query.all())
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
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/Ocr', methods=['GET', 'POST'])
def ocr():
    return render_template('ocr.html', user=current_user)
# @auth.route('/home')
# def home():
#     return render_template("home.html")


@auth.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading', category='error')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(
            f"C:/Users/mskas/OneDrive/Desktop/py4e/.vscode/ML/New folder/flask Web app/website/test_ocr/{filename}")
        #print('upload_image filename: ' + filename)
        image_to_text(
            f"C:/Users/mskas/OneDrive/Desktop/py4e/.vscode/ML/New folder/flask Web app/website/test_ocr/{filename}")
        # flash('Image successfully uploaded and displayed below', category='success')
        return redirect(url_for('views.home'))
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

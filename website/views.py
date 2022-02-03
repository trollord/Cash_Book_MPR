from django import views
from flask import Blueprint, flash, render_template
from flask import request as rq
from flask_login import login_user, logout_user, login_required, current_user
from httpx import request
from .models import Note, db

views = Blueprint('views', __name__)
c = 0
# sum of the data_amt


def sum_data_amt(user):
    sum = 0
    for note in user.notes:
        sum += note.data_amt
    return sum


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if rq.method == 'POST':
        note = rq.form.get('note')
        amt = rq.form.get('amt')
        try:
            int(amt)
            it_is = True
        except ValueError:
            it_is = False

        if len(note) < 1:
            flash('Note too short!', category='error')
        elif it_is == False:
            flash('Amount must be a number!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id, data_amt=amt)
            db.session.add(new_note)
            db.session.commit()
            flash("Expense added succesfully ! ", category='success')
    return render_template("home.html", user=current_user, sum=sum_data_amt(current_user))


@views.route('/delete', methods=['GET', 'POST'])
def delete_note():
    if rq.method == 'POST':
        note_id = rq.form.get('note_id')
        note = Note.query.filter_by(id=note_id).first()
        db.session.delete(note)
        db.session.commit()
        flash('Expense deleted succesfully!', category='success')
    return render_template("home.html", user=current_user, sum=sum_data_amt(current_user))

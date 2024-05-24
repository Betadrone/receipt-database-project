from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Note, Receipt

views = Blueprint("views", __name__)


@views.route('/', methods={'GET', 'POST'})
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) <= 1:
            flash("note is too short!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")

    return render_template("home.html", user=current_user)


@views.route('/receipt', methods=['GET', 'POST'])
@login_required
def receipt():
    if request.method == "POST":
        date = request.form.get("date")
        time = request.form.get("time")
        liters = request.form.get("liters")
        total_dollar = request.form.get("total_dollar")
        vehicle = request.form.get("vehicle")
        odometer = request.form.get("odometer")
        fuel_card = request.form.get("fuel_card")
        payment_method = request.form.get("payment_method")

        if not date:
            flash("Date missing.", category='error')
        elif not time:
            flash("Time missing.", category='error')
        elif not liters:
            flash("liters missing.", category='error')
        elif not total_dollar:
            flash("total dollars missing.", category='error')
        elif not vehicle:
            flash("vehicle number missing.", category='error')
        elif not odometer:
            flash("odometer value missing", category='error')
        elif not fuel_card:
            flash("fuel card number missing.", category='error')
        elif not payment_method:
            flash("payment method value missing.", category='error')
        else:
            new_receipt = Receipt(
                user_id=current_user.id,
                date=date,
                time=time,
                liters=liters,
                total_dollar=total_dollar,
                vehicle=vehicle,
                odometer=odometer,
                fuel_card=fuel_card,
                payment_method=payment_method
            )

            db.session.add(new_receipt)
            db.session.commit()
            flash("Receipt created!", category='success')

    return render_template("receipt.html", user=current_user)


@views.route('/database')
def database():
    return render_template("database.html", user=current_user)
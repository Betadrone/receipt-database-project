from datetime import datetime
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Note, Receipt
import json

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


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/delete-receipt', methods=['POST'])
def delete_receipt():
    receipt = json.loads(request.data)
    print(receipt)
    receiptId = receipt['receiptId']
    receipt = Receipt.query.get(receiptId)
    if receipt:
        if receipt.user_id == current_user.id:
            db.session.delete(receipt)
            db.session.commit()
    return jsonify({})


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
                payment_method=payment_method,
                user_last_updated=current_user.first_name,
                date_last_updated=datetime.today().strftime('%Y-%m-%d')
            )

            db.session.add(new_receipt)
            db.session.commit()
            flash("Receipt created!", category='success')

    return render_template("receipt.html", user=current_user)


@views.route('/database')
def database():
    return render_template("database.html", user=current_user)


@views.route('/edit_receipt/<int:receiptId>', methods=['GET', 'POST'])
@login_required
def receipt_detail(receiptId):
    receipt = Receipt.query.filter_by(id=receiptId).first()
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
            receipt.date = date
            receipt.time = time
            receipt.liters = liters
            receipt.total_dollar = total_dollar
            receipt.vehicle = vehicle
            receipt.odometer = odometer
            receipt.fuel_card = fuel_card
            receipt.payment_method = payment_method
            receipt.user_last_updated = current_user.first_name
            receipt.date_last_updated = datetime.today().strftime('%Y-%m-%d')

            db.session.commit()
            flash("Receipt edited!", category='success')
            return redirect(url_for("views.database"))

    return render_template("edit_receipt.html", user=current_user, date=receipt.date,
                           time=receipt.time, liters=receipt.liters, totalDollar=receipt.total_dollar,
                           vehicle=receipt.vehicle, odometer=receipt.odometer, fuelCard=receipt.fuel_card,
                           paymentMethod=receipt.payment_method)

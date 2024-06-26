from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    liters = db.Column(db.Float)
    total_dollar = db.Column(db.Float)
    vehicle = db.Column(db.String(50))
    odometer = db.Column(db.Integer)
    fuel_card = db.Column(db.Integer)
    payment_method = db.Column(db.Integer)
    user_last_updated = db.Column(db.String(50))
    date_last_updated = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10_000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    receipts = db.relationship('Receipt')




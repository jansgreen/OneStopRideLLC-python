from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    




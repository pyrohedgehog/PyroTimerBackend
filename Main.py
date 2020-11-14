import os
# import MYSQL
import bson as bson
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import (
    json,
    Flask,
    render_template,
    request
)
from sqlalchemy_serializer import serializer, SerializerMixin

file_path = "MainDatabase.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
db = SQLAlchemy(app)


class CustomSerializerMixin(SerializerMixin):
    serialize_types = (
        (bson.UUID, lambda x: str(x)),
    )


class User(db.Model, CustomSerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String)
    salt = db.Column(db.String)
    defaultTask = db.Column(db.Integer, unique=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.salt = genSalt()
        self.password = hashpassword(email, password)


    def __repr__(self):
        return '<User %r>' % self.username
def genSalt():
    return str(os.urandom(120))


def convToArray(string):
    return string.split("\n")


def convFromArray(arr):
    ans = ""
    for x in arr:
        ans += x
        ans += "\n"
    return ans[:-1]


class Task(db.Model, CustomSerializerMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    public = db.Column(db.BOOLEAN)
    writeIDs = db.Column(db.String)
    readIDs = db.Column(db.String)
    title = db.Column(db.String)
    info = db.Column(db.String)
    linkedTasks = db.Column(db.String)

    def __init__(self, id, writeID, readID, title, info):
        self.id = id
        self.writeIDs = convToArray([writeID])
        self.readIDs = convToArray([readID])
        self.title = title
        self.info = info
        self.linkedTasks = ''  # an empty array


def hashpassword(salt, plaintext):
    return str(hash((salt, plaintext)))


@app.route('/user', methods=["GET", 'POST'])
def getUser():
    if not request.json:
        return "Error, no user information given"
    else:
        re = request.json

# db.create_all()  # In case user table doesn't exists already. Else remove it.
# user = User("test",'Test', 'password')
#
# db.session.add(user)
# db.session.commit()

# User.query.filter_by(username='admin').first()



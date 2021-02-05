import os

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
def convToArray(string):
    return string.split("\n")


def convFromArray(arr):
    ans = ""
    for x in arr:
        ans += x
        ans += "\n"
    return ans[:-1]

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
        self.password = hashPassword(self.salt, password)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def genNewUserFromDict(data):
        username = data["username"]
        email = data["email"]
        password = data["password"]
        user = User(username, email, password)
        generateDefaultUserLoginTasks(user)
        return user



class Task(db.Model, CustomSerializerMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    public = db.Column(db.BOOLEAN)
    writeIDs = db.Column(db.String)
    readIDs = db.Column(db.String)
    title = db.Column(db.String)
    info = db.Column(db.String)
    linkedTasks = db.Column(db.String)

    def __init__(self, writeID, readID, title, info):
        self.public = False
        self.writeIDs = convFromArray(writeID)
        self.readIDs = convFromArray(readID)
        self.title = title
        self.info = info
        self.linkedTasks = ''  # an empty array

    def __repr__(self):
        return "id:{}, writeIDs:{}, readIDs{}, public:{}, title:{}, info:{}, linkedTasks:{}".format(
            self.id, self.writeIDs, self.readIDs, self.public, self.title, self.info, self.linkedTasks)

    def getLinkedTasks(self):
        tasks = []
        for x in convFromArray(self.linkedTasks):
            tasks.append(self.query.filter_by(id=int(x)).first())
        return tasks

    def getAllLinkedTasks(self, tasks):
        # yes its repeating code, but its more efficient repeating code
        for x in convFromArray(self.linkedTasks):
            foo = self.query.filter_by(id=int(x)).first()
            if foo not in tasks:
                tasks.append(foo)
                foo.getAllLinkedTasks(tasks)
        return tasks


def hashPassword(salt, plaintext):
    return str(hash((salt, plaintext)))

def genSalt():
    return str(os.urandom(120))

def generateDefaultUserLoginTasks(user):
    ids = user.id
    defaultTask = Task(ids,ids,"","")
    tutorial = Task(ids,ids,"Click Me", "what more do you need?") #tutorials can be added here
    defaultTask.linkedTasks = convToArray(str(tutorial.id))
    user.defaultTask = defaultTask
    return defaultTask


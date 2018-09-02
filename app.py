import time
import psycopg2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
import socket

from ops import Ops

app = Flask(__name__)
app.debug = True

# Setup SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://duane.dos:LX:954Dos#@localhost:5432/steemydata';
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(120), unique=False)
    memo = db.Column(db.String(120), unique=True)
    block = db.Column(db.String(120), unique=True)
    time = db.Column(db.String(120), unique=True)
    trans_id = db.Column(db.String(120), unique=True)
    amount = db.Column(db.String(120), unique=True)
    ctype = db.Column(db.String(120), unique=False)

    def __init__(self, sender, memo, block, time, trans_id, amount, ctype):
        #self.id = id
        self.sender = sender
        self.memo = memo
        self.block = block
        self.time = time
        self.trans_id = trans_id
        self.amount = amount
        self.ctype = ctype

    def __repr__(self):
        return '<Transaction %>' % self.trans_id

steemOps = Ops(db, User)

def startBlockchain():
    print(steemOps.lastTransaction())
    return steemOps.listenForTrans()
    # steemOps.run()

@app.route("/freevote/<string:memo1>/<string:memo2>/<string:memo3>/<string:memo4>/")
def freev(memo1, memo2, memo3, memo4):
    memo = memo1 + '/' + memo2 + '/' + memo3 + '/' + memo4 + '/'
    steemOps.freePost(memo)
    return memo

@app.route("/")
def hello():
    startBlockchain()
    return "<h1 style='color:blue'>Hello There!</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
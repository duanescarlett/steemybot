import time
from flask import Flask
#from redis import Redis, RedisError

import os
import socket

# Connect to Redis
from ops import Ops

app = Flask(__name__)
app.debug = True

steemOps = Ops()

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
    app.run(host='0.0.0.0', debug=True)
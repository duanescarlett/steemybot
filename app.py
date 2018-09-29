from flask import Flask
from redis import Redis, RedisError
import os
import socket

from ops import Ops

# Connect to Redis
redis = Redis(host="db", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)
#app.config.from_object('config')
steemOps = Ops(redis)

def startBlockchain():
    print(steemOps.lastTransaction())
    return steemOps.listenForTrans()
    # steemOps.run()

@app.route("/freevote/<string:memo1>/<string:memo2>/<string:memo3>/<string:memo4>")
def freev(memo1, memo2, memo3, memo4):
    memo = memo1 + '/' + memo2 + '/' + memo3 + '/' + memo4
    steemOps.freePost(memo)
    return memo

@app.route("/")
def hello():
    startBlockchain()
    return "<h1 style='color:blue'>Hello There!</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
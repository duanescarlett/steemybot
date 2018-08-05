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


# def get_hit_count():
#     retries = 5
#     while True:
#         try:
#             return redis.incr('hits')
#         except redis.exceptions.ConnectionError as exc:
#             if retries == 0:
#                 raise exc
#             retries -= 1
#             time.sleep(0.5)


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
    # try:
    #     #visits = redis.incr("counter")
    #     startBlockchain()
    # except RedisError:
    #     visits = "<i>cannot connect to Redis, counter disabled</i>"
    #     startBlockchain()
    #
    # html = "<h3>Hello {name}!</h3>" \
    #        "<b>Hostname:</b> {hostname}<br/>" \
    #        "<b>Visits:</b> {visits}"
    # return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)
    startBlockchain()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
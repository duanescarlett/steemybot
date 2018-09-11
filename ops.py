import random
import time

from steem.blockchain import Blockchain
from steem.post import Post
from steem.account import Account
from steem.steem import Commit
from steem import Steem
from flask import request

class Ops:

    steem_nodes = ['https://api.steemit.com',
                   'https://rpc.buildteam.io',
                   'https://steemd.minnowsupportproject.org']

    def __init__(self, redis_store):

        self.s = Steem(nodes=self.steem_nodes, keys=['5KAnYvEubpkgG1ooAQWyKzzYmhagE4jUvNpTiJocrvvGDDEjRz2',
                             '5JKUi7X7VM7AUQVVijA8xTiy15stBRj4WFbshTh6yBYCTKur49g'])
        self.data = redis_store

    def lastTransaction(self):
        acc = Account("steemybot", steemd_instance=self.s)
        steemd = list(acc.get_account_history(-1, 1, filter_by=["transfer"]))
        # print(steemd)
        return steemd

    # def poster(self):
    #     self.s.commit.post(
    #         "Automation services on the steem blockchain",
    #         "This is a test post created by my new bot. This bot will have multiple services like upvote and resteem. More details are coming soon.",
    #         "duane.dos",
    #         tags=["test", ]
    #     )

    def comment(self, post, link):
        post(
            "Automation services on the steem blockchain",
            "Awesome post",
            "steemybot",
            reply_identifier=link,
            tags=["test", ]
        )

    def freePost(self, memo):
        memo = "https://" + memo
        post = Post(memo)

        # get a voting weight between 80 and 100
        vote_weight = float(random.randint(+5, +15))
        # Upvote the post
        post.commit.vote(post.identifier, vote_weight, account="steemybot")
        print("I ran")

        # Check to see if memo is in the database
        # if self.redis_server.get(memo):
        #     #continue
        #     # send message saying that post has already been upvoted and send money back if
        #     # steemy got paid
        #
        #     print("Already upvoted this post")
        # else:
        #     self.redis_server.set(memo, memo)
        #     # get a voting weight between 80 and 100
        #     vote_weight = float(random.randint(+5, +15))
        #     # Upvote the post
        #     post.commit.vote(post.identifier, vote_weight, account="steemybot")
        #     print("I ran")

    def listenForTrans(self):
        while True:
            transfers = self.lastTransaction()
            for transfer in transfers:
                if transfer["to"] != "steemybot":
                    print("This is a empty transfer " + transfer["to"])
                    continue
                else:
                    try:
                        post = Post(transfer.get("memo"))
                        amount = transfer.get("amount")
                        memo = transfer.get("memo")
                        sender = transfer.get("from")
                        block = transfer.get("block")
                        timestamp = transfer.get("timestamp")
                        transId = transfer.get("trx_id")

                        # if self.redis_server.get(memo):
                        if self.data.get(memo):
                            print("Already upvoted this post")
                            continue
                        else:
                            coin = amount.split(" ")
                            print(coin[1])  # Print the amount
                            crypcoin = float(coin[0])  # Crypto value
                            cryptoType = coin[1]  # Crypto type

                            # Init and put memo into the database
                            self.data.set(memo, memo)

                            post.reply(
                                "This post was upvoted by @steemybot, Send at least 0.01 STEEM or SBD and get an upvote. Join my discord server for a free upvote for each post. <br><br>@steemybot our mission is to support high quality posts which will raise the value of the STEEM Blockchain.",
                                "", "steemybot")

                            if cryptoType == "STEEM":
                                print("This is steem")
                                # print("Amount Sent => " + crypcoin)
                                # Calculate vote power based on amount sent
                                if crypcoin < 1.000:
                                    # get a voting weight between 80 and 100
                                    vote_weight = float(random.randint(+10, +40))
                                    # Upvote the post
                                    post.commit.vote(post.identifier, vote_weight, account="steemybot")

                                elif crypcoin >= 1.000 and crypcoin < 3.000:
                                    # get a voting weight between 80 and 100
                                    vote_weight = float(random.randint(+40, +60))
                                    # Upvote the post
                                    post.commit.vote(post.identifier, vote_weight, account="steemybot")

                                elif crypcoin >= 3.000:
                                    # get a voting weight
                                    vote_weight = float(random.randint(+60, +95))
                                    # Upvote the post
                                    post.commit.vote(post.identifier, vote_weight, account="steemybot")


                            elif cryptoType == "SBD":
                                print("This is SBD")
                                # print("Amount Sent => " + crypcoin)

                                # Calculate vote power based on amount sent
                                if crypcoin < 1.000:
                                    # get a voting weight between 80 and 100
                                    vote_weight = float(random.randint(+10, +40))
                                    # Upvote the post
                                    post.commit.vote(post.identifier, vote_weight, account="steemybot")
                                elif crypcoin >= 1.000 and crypcoin < 3.000:
                                    # get a voting weight between 80 and 100
                                    vote_weight = float(random.randint(+40, +60))
                                    # Upvote the post
                                    post.commit.vote(post.identifier, vote_weight, account="steemybot")
                                elif crypcoin >= 3.000:
                                    # get a voting weight between 80 and 100
                                    vote_weight = float(random.randint(+60, +95))
                                    # Upvote the post
                                    post.commit.vote(post.identifier, vote_weight, account="steemybot")
                            else:
                                print("Nothing Happened, I wonder why")

                    except ValueError as e:
                        if 'Invalid identifier' == e.args[0]:
                            print("Invalid post link. Consider a refund. [%s]" %
                                  transfer.get("memo"))
                            continue

                print("Sleeping for 3 seconds")
                time.sleep(10)

    def upVote(self, permalink, weight, user):
        post = Post(permalink)
        post.upvote(weight, user)

    def refund(self, acc, amount, sbdorsteem, memoText, sender):

        Commit.transfer(
            acc,
            amount,
            sbdorsteem,
            memo=memoText,
            account=sender
        )

    def run(self):
        # upvote posts with 30% weight
        upvote_pct = 30
        whoami = 'duane.dos'

        # stream comments as they are published on the blockchain
        # turn them into convenient Post objects while we're at it
        b = Blockchain()
        stream = map(Post, b.stream(filter_by=['comment']))

        try:

            for post in stream:
                if post.json_metadata:
                    mentions = post.json_metadata.get('users', [])

                    # if post mentions more than 10 people its likely spam
                    if mentions and len(mentions) < 10:
                        post.upvote(weight=upvote_pct, voter=whoami)

        except Exception:
            print("Post array search complete")
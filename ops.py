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

    def refund(self, to, amount, asset, memo='', account=None):
        self.s.transfer(to, amount, asset, memo, account)

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

        # Check to see if memo is in the database
        if self.data.get(memo):
            #continue
            # send message saying that post has already been upvoted and send money back if
            # steemy got paid

            print("Already upvoted this post")
        else:
            self.data.set(memo, memo)
            # get a voting weight between 80 and 100
            vote_weight = float(random.randint(+5, +9))
            # Upvote the post
            post.commit.vote(post.identifier, vote_weight, account="steemybot")
            print("I ran")
            post.reply(
                "This post was upvoted by @steemybot, Send at least 0.01 STEEM or SBD "
                "and get an upvote. Join my discord server for free weighted upvoting for each post, just put the command !upvote before the web address of the post and you will get a free upvote within 2 mins."
                "<br><br>@steemybot our mission is to support high quality posts which will raise the value of the STEEM Blockchain.",
                "", "steemybot")

    def listenForTrans(self):
        while True:
            transfers = self.lastTransaction()
            for transfer in transfers:
                if transfer["to"] != "steemybot":
                    #This transfer does not belong to steemybot
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

                        # Parse string for coin type
                        coin = amount.split(" ")
                        print(coin[1])  # Print the amount
                        crypcoin = float(coin[0])  # Crypto value
                        cryptoType = coin[1]  # Crypto type

                        if not memo:
                            self.s.transfer(sender, float(amount), crypcoin, "Your memo is empty, here is your refund",
                                            "steemybot")

                        if self.data.get(memo):
                            print("Already upvoted this post")
                            # Give a refund
                            self.refund(sender, float(amount), crypcoin, memo, "steemybot")
                            # post.reply(
                            #     "You received a refund from Steemy Bot, your post was already upvoted",
                            #     "", "steemybot")
                            continue
                        else:
                            # coin = amount.split(" ")
                            # print(coin[1])  # Print the amount
                            # crypcoin = float(coin[0])  # Crypto value
                            # cryptoType = coin[1]  # Crypto type

                            # Init and put memo into the database
                            self.data.set(memo, memo)
                            # Set transaction ID to prove that post was already upvoted
                            self.data.set(transId, transId)

                            post.reply(
                                "This post was upvoted by @steemybot, Send at least 0.01 STEEM or SBD "
                                "and get an upvote. Join my discord server discord.gg/MEBXbbY for free weighted upvoting for each post, just put the command !upvote before the web address of the post and you will get a free upvote within 2 mins."
                                "<br><br>@steemybot our mission is to support high quality posts which will raise the value of the STEEM Blockchain.",
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

                            if self.data(transfer.get("trx_id")):
                                continue
                            else:
                                amount = transfer.get("amount")
                                coin = amount.split(" ")
                                crypcoin = float(coin[0])

                                self.s.transfer(transfer.get("from"), crypcoin, coin[1], "Your memo is empty, here is your refund",
                                       "steemybot")


                print("Sleeping for 3 seconds")
                time.sleep(3)


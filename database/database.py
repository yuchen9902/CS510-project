import json
import os
from _md5 import md5
from collections import OrderedDict

from bson import ObjectId
from pymongo import MongoClient
from flask.cli import load_dotenv

import datetime

from database import schema

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_PW = os.getenv("SECRET_PW")

POST = "Posts"
USER = "Users"
DB_NAME = "forum"


class Database:
    """
    insert user information into database
    """

    def __init__(self):
        try:
            self.client = MongoClient("mongodb+srv://" + SECRET_KEY + ":" + SECRET_PW +
                                      "@cluster0.dfeu0.mongodb.net/" + DB_NAME + "?retryWrites=true&w=majority")

            self.db = self.client.forum
            self.db_users = self.db.Users
            self.db_posts = self.db.Posts

        except ConnectionAbortedError:
            print("[ERROR]: Connection Error")

    def reset_collections(self):
        """
        Define collection's schema

        :param curr_db: database's port
        :return: no return newValue
        """
        self.db[POST].drop()
        self.db[USER].drop()
        self.db.create_collection(POST)
        self.db.create_collection(USER)
        self.db.command(OrderedDict(schema.user_schema))
        self.db.command(OrderedDict(schema.post_schema))

    def get_db_user_by_username(self, data):
        """
        get user information by username
        """
        res = list(self.db_users.find({"_id": data}, projection={'_id': False}))
        if len(res) == 0:
            return None
        return res[0]

    def post_user(self, data):
        """
        register user information into database
        """
        try:
            self.db_users.insert_one(data)
            msg = "You've successfully registered!! Please login"
        except Exception:
            msg = "[WARNING]: User has already registered, please log in"
        return msg

    def insert_post(self, data, is_post=True):
        # curr_db = connect_db()
        try:
            post_id = self.db[POST].insert_one(data).inserted_id
            msg = None
        except Exception:
            post_id = None
            msg = "[WARNING]: Failed to insert"
        return post_id, msg

    def get_all_posts_by_username(self, data):
        return list(self.db_posts.find({'user_id': data}, projection={'_id': False}))

    def get_all_posts(self, need_reply=False):
        """
        Out put all posts to json
        TODO:Get rid of reply, add a boolean need_reply
        """
        if need_reply:
            return list(self.db_posts.find())
        else:
            return list(self.db_posts.find({'is_post': True}))

    def get_post_by_id(self, id):
        objectId = ObjectId(id)
        return list(self.db_posts.find({'_id': objectId}, projection={'_id': False}))

    def get_reply_by_post_id(self, id):
        return list(self.db_posts.find({'to_which_post': id}, projection={'_id': False}))

    def update_user_info(self, user_info):
        self.db_users.update_one({'_id': user_info['_id']},
                                 {'$set': {'post_count': user_info['post_count'],
                                           'depression_count': user_info['depression_count']}})


if __name__ == "__main__":
    database = Database()
    # d = {"_id": "td2@illinois.edu",
    #      "password": "password",
    #      "post_count": 0,
    #      "depression_count": 0
    #      }
    #
    # p = {"content": "Hello123",
    #      "is_depressed": 1,
    #      "user_id": "td2@illinois.edu",
    #      "title": "see",
    #      "created_time": "now"
    #     }
    # print(database.get_post_by_id("6278507f357808838813b2db"))
    # print(user.post_user(d))
    # print(user.get_db_user_by_username("td2@illinois.edu"))
    # res = database.get_all_posts(True)
    # time = res[0]['created_time']
    # print(res)
    # print(time)
    # print(datetime.datetime.now())
    data = {"user_id": "我是小甜",
            "content": "开心开心开心！",
            "is_depressed": False,
            "is_post": True,
            "title": "我爱吃西兰花",
            "created_time": datetime.datetime.now()}
    #
    database.insert_post(data)

    # reply = {"user_id": "天涯",
    #          "content": "事实真的如此么，且不说公司完全可以为大牛搞个特例，就算回公司，真的有那么困难么？",
    #          "is_depressed": False,
    #          "is_post": False,
    #          "created_time": datetime.datetime.now(),
    #          "to_which_post": "6278a5699388fca0394d3863"}
    # database.insert_post(reply)

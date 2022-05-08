import os

from pymongo import MongoClient
from flask.cli import load_dotenv

import datetime
import schema
from bson.objectid import ObjectId

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
                                      "@cluster0.dfeu0.mongodb.net/"+DB_NAME+"?retryWrites=true&w=majority")

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
        return list(self.db_users.find({"_id": data}, projection={'_id': False}))

    def post_user(self, data):
        """
        register user information into database
        """
        try:
            self.db_users.insert_one(data)
            msg = None
        except Exception:
            msg = "[WARNING]: User has already registered, please log in"
        return msg

    def insert_post(self, data, is_post=True):
        # curr_db = connect_db()
        self.db[POST].insert_many(data)

    def get_all_posts_by_username(self, data):
        return list(self.db_posts.find({'user_id': data}, projection={'_id': False}))

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
    #
    # print(user.post_user(d))
    # print(user.get_db_user_by_username("td2@illinois.edu"))
    # res = user.get_all_posts_by_username("1")
    # time = res[0]['created_time']
    # print(res)
    # print(time)

    data = [{"user_id": "1",
             "content": "third post",
             "is_depressed": True,
             "is_post": True,
             "title": "bbb",
             "created_time": datetime.datetime.now()}]

    database.insert_post(data)

    reply = [{"user_id": "2",
             "content": "reply",
             "is_depressed": False,
             "is_post": False,
             "created_time": datetime.datetime.now(),
             "to_which_post": "62772ec0a91bb48998360c43"}]
    database.insert_post(reply)

import os
import sys
import json
from collections import OrderedDict
import pymongo
from pymongo import MongoClient
import flask
# import dotenv
# from pathlib import Path
import datetime
import schema
from bson.objectid import ObjectId
from flask.cli import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_PW = os.getenv("SECRET_PW")
DB_NAME = "forum"
MONGOURL = "mongodb+srv://" + SECRET_KEY + ":" + SECRET_PW + "@cluster0.dfeu0.mongodb.net/"+DB_NAME+"?retryWrites=true&w=majority"


POST = "Posts"
USER = "Users"

def reset_collections(curr_db):
    """
    Define collection's schema

    :param curr_db: database's port
    :return: no return newValue
    """
    curr_db[POST].drop()
    curr_db[USER].drop()
    curr_db.create_collection(POST)
    curr_db.create_collection(USER)
    curr_db.command(OrderedDict(schema.user_schema))
    curr_db.command(OrderedDict(schema.post_schema))

def insert_post(data, is_post=True):
    curr_db = connect_db()
    curr_db[POST].insert_many(data)

def connect_db():
    """
    Helper to connect with mongoDB
    :return: connection port
    """
    # mongo_url = os.environ['MONGOURL']
    # mongo_db = os.environ['DB']
    print(MONGOURL)
    client = MongoClient(MONGOURL)
    curr_db = client[DB_NAME]

    print("conneted")
    return curr_db

if __name__ == '__main__':
    curr_db = connect_db()
    # curr_db.create_collection(POST)
    # curr_db.command(OrderedDict(schema.post_schema))
    # data = [{"user_id": "1",
    #          "content": "second post",
    #          "is_depressed": True,
    #          "is_post": True,
    #          "title": "bbb",
    #          "created_time": datetime.datetime.now()}]
    #
    # reply = [{"user_id": "2",
    #          "content": "reply",
    #          "is_depressed": False,
    #          "is_post": False,
    #          "created_time": datetime.datetime.now(),
    #          "to_which_post": "62772ec0a91bb48998360c43"}]
    #
    # insert_post(data)
    # insert_post(reply)

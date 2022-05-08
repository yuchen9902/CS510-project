import pandas
import requests
import json
from pymongo import ReturnDocument
from backend.scraper import Scraper
from backend.users import User
from flask import Flask, request, render_template, abort, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

user = User()
db_users = user.get_db_users()


# data_file = pandas.read_excel('users.csv')
# number = 7
# data_csv = user.from_csv_to_database(data_file, number)

def get_user_query():
    """
    helper function to get users query
    @return: query parsed
    """
    val = request.args
    query = {}
    for params in val:
        if params == 'Username':
            query = {'Username': val[params].replace('"', '')}
    return query


@app.route('/api/users', methods=['GET', 'PUT', 'POST', 'DELETE'])
# # @login_required
def get_users():
    """
    get/put/post/delete users
    @return: json data
    """
    if request.method == 'GET':
        query = get_user_query()
        result = db_users.find(query, projection={'_id': False})
        result = list(result)
        return {'data': result}, 200

    elif request.method == 'PUT':
        if not request.content_type.startswith('application/json'):
            abort(415, 'please sent data in json format')
        new_data = request.json
        query = get_user_query()
        result = db_users.find_one_and_update(query,
                                              {'$set': new_data}, projection={'_id': False},
                                              return_document=ReturnDocument.AFTER)
        return {'data': result}, 200

    elif request.method == 'POST':
        if not request.content_type.startswith('application/json'):
            abort(415, 'please sent data in json format')
        new_data = request.json
        db_users.insert_one(new_data)
        return {'data': list(db_users.find({}, projection={'_id': False}))}, 201

    elif request.method == 'DELETE':
        query = get_user_query()
        print(query)
        db_users.delete_one(query)
        return {'data': list(db_users.find({}, projection={'_id': False}))}, 200
    else:
        return 400


@app.route('/api/home')
def get_recipes():
    """
    get recipes from home
    @return: json data with id
    """
    if request.method == 'GET':
        with open("recipes.json") as json_file:
            data = json.load(json_file)
        print("requested!!")
        id = 0
        for item in data:
            item.__setitem__("_id", id)
            id += 1
        return {'data': data}, 200


@app.route('/api/index')
def get_index():
    """
    get recipes from index page
    @return: json data for stest
    """
    return {'data': {"dish_name": "Spicy Crispy Potatoes"}}, 200

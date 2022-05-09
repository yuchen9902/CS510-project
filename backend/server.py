from flask import Flask, request, abort
from backend.database.database import Database

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

db = Database()


def get_query(key):
    """
    helper function to get users query
    @return: query parsed
    """
    val = request.args
    query = {}
    for params in val:
        if params == key:
            query = val[params]
    return query


@app.route('/api/user', methods=['GET', 'POST'])
# @login_required
def user_api():
    """
    get/put users
    @return: json data
    """
    if request.method == 'GET':
        query = get_query("username")
        result = db.get_db_user_by_username(query)
        return {'data': result, 'msg': ""}, 200

    elif request.method == 'POST':
        if not request.content_type.startswith('application/json'):
            abort(415, 'please sent data in json format')
        new_data = request.json
        msg = db.post_user(new_data)
        if msg:
            return {'data': [], 'msg': msg}, 422
        return {'data': [], 'msg': msg}, 201

    else:
        return 400


@app.route('/api/posts')
def posts_api():
    """
    get all posts from home
    @return: json data
    """
    if request.method == 'GET':
        data = db.get_all_posts()
        return {'data': data}, 200


@app.route('/api/post', methods=['GET', 'POST'])
def post_api():
    """
    get/put posts
    @return: json data
    """
    if request.method == 'GET':
        query = get_query("_id")
        result = db.get_post_by_id(query)
        return {'data': result, 'msg': ""}, 200

    elif request.method == 'POST':
        if not request.content_type.startswith('application/json'):
            abort(415, 'please sent data in json format')
        new_data = request.json
        msg = db.insert_post(new_data)
        if msg:
            return {'data': [], 'msg': msg}, 422
        return {'data': [], 'msg': msg}, 201

    else:
        return 400


if __name__ == "__main__":
    app.run()

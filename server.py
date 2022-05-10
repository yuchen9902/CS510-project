from flask import Flask, request, abort, render_template
from backend.database.database import Database
from flask_login import LoginManager


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

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('profile.html', name=name)


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
        # result = "abc"
    elif request.method == 'POST':
        print("else")
        # xyz
        # if not request.content_type.startswith('application/json'):
        #     abort(415, 'please sent data in json format')
        new_data = request.form
        print("new_data")
        print(new_data)
        user = {
            "_id": request.form.get('username'),
            "password": request.form.get('password'),
            "post_count": 0,
            "depression_count": 0
        }
        msg = db.post_user(user)
        # if msg:
            # return {'data': [], 'msg': msg}, 422
        # return {'data': [], 'msg': msg}, 201
        print(msg)
        return render_template('register.html', message=msg)
    else:
        return 400


@app.route('/test')
def render_register():
    return render_template('register.html')


@app.route('/api/posts')
def posts_api():
    """
    get all posts from home
    @return: json data
    """
    if request.method == 'GET':
        query = get_query("username")
        if len(query) == 0:
            data = db.get_all_posts()
            for r in data:
                r['created_time'] = str(r['created_time'])[:19]
            return {'data': data}, 200
        else:
            # xzy
            posts = db.get_all_posts_by_username(query)
            for r in posts:
                r['created_time'] = str(r['created_time'])[:19]
            print(posts)

            user_info = db.get_db_user_by_username(query)[0]
            print(user_info)
            return render_template('profile.html', username=query,
                                   posts=posts, post_count=user_info["post_count"],
                                   depression_count=user_info["depression_count"])


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
    app.run(host="127.0.0.1", port=8080)

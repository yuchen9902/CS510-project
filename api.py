import datetime
from flask import Flask, request, abort, render_template, redirect, url_for
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


@app.route('/user', methods=['GET', 'POST'])
# @login_required
def user_api():
    """
    get/put users
    @return: json data
    """
    if request.method == 'GET':
        query = get_query("username")
        result = db.get_db_user_by_username(query)
        return render_template("login.html")

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


@app.route('/posts')
def posts_api():
    """
    Home page
    """
    data = db.get_all_posts()
    for r in data:
        r['_id'] = str(r['_id'])
        r['created_time'] = str(r['created_time'])[:19]
    return render_template("forum.html", posts=data)


@app.route('/post', methods=['GET', 'POST'])
def post_api():
    """
    get/put posts
    @return: json data
    """
    if request.method == 'GET':
        query = get_query("_id")
        result = db.get_post_by_id(query)[0]
        result['created_time'] = str(result['created_time'])[:19]
        print(result)
        replies = db.get_reply_by_post_id(query)
        for r in replies:
            r['created_time'] = str(r['created_time'])[:19]
        print(replies)
        return render_template("post.html", postId=query, post=result, replies=replies)

    elif request.method == 'POST':
        new_data = request.form.to_dict()
        new_data['created_time'] = datetime.datetime.now()
        new_data['is_depressed'] = False
        new_data['is_post'] = bool(int(new_data['is_post']))
        print(new_data)
        post_id, msg = db.insert_post(new_data)
        print(msg)
        if new_data['is_post'] == 1:
            query = post_id
        else:
            query = new_data['to_which_post']

        result = db.get_post_by_id(query)[0]
        result['created_time'] = str(result['created_time'])[:19]
        print(result)

        replies = db.get_reply_by_post_id(query)
        for r in replies:
            r['created_time'] = str(r['created_time'])[:19]
        print(replies)

        return redirect(url_for('post_api', code=303, _id=query))

    else:
        return 400


@app.route('/profile/<username>')
def profile(username):
    posts = db.get_all_posts_by_username(username)
    for r in posts:
        r['created_time'] = str(r['created_time'])[:19]
    print(posts)
    print(username)
    user_info = db.get_db_user_by_username(username)[0]
    print(user_info)
    return render_template('profile.html', username=username,
                           posts=posts, post_count=user_info["post_count"],
                           depression_count=user_info["depression_count"])


if __name__ == "__main__":
    app.run()

import datetime
import os
import pickle
from hashlib import md5
from flask import Flask, request, render_template, redirect, url_for

from database.database import Database
from flask_login import LoginManager, login_user, login_required, UserMixin, current_user, logout_user

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
db = Database()

# use login manager to manage session
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


class User(UserMixin):
    def __init__(self, username):
        self.id = username


class ML:
    def __init__(self):
        filename = 'finalized_model.sav'
        self.loaded_model = pickle.load(open(filename, 'rb'))
        file_tfidf = 'tfidf_vectorizer.sav'
        self.tfidf_vectorizer = pickle.load(open(file_tfidf, 'rb'))

    def predict(self, X_test):
        X_test = self.tfidf_vectorizer.transform(X_test)
        result = self.loaded_model.predict(X_test)
        return result


model = ML()


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
        # new_data['is_depressed'] = model.predict([])
        new_data['is_post'] = bool(int(new_data['is_post']))
        new_data['user_id'] = current_user.id

        # Here will run the ML model on the post
        text = new_data['content'] + new_data['title']
        pred = model.predict([text])
        print("content to be predict: ", text)
        print("predict result: ", pred)

        if pred[0] == 1:
            new_data['is_depressed'] = True
        else:
            new_data['is_depressed'] = False
        print(new_data)

        # db interaction
        post_id, msg = db.insert_post(new_data)
        user_info = db.get_db_user_by_username(current_user.id)
        user_info['_id'] = current_user.id
        user_info['depression_count'] += 1 if pred[0] == 1 else 0
        user_info['post_count'] += 1
        db.update_user_info(user_info)

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


@app.route('/profile')
def profile():
    username = current_user.id
    posts = db.get_all_posts_by_username(username)
    for r in posts:
        r['created_time'] = str(r['created_time'])[:19]
    print(posts)

    user_info = db.get_db_user_by_username(username)
    print(user_info)
    return render_template('profile.html', username=username,
                           posts=posts, post_count=user_info["post_count"],
                           depression_count=user_info["depression_count"])


@app.route('/register', methods=['GET', 'POST'])
def user_api():
    """
    get/put users
    @return: json data
    """
    if request.method == 'GET':
        return render_template('register.html', message="")
    elif request.method == 'POST':
        print("else")
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
        print(msg)
        return redirect(url_for('login', msg=msg))


@app.route('/login', methods=['GET', 'POST'])  # POST
def login():
    query = get_query("msg")
    msg = None
    if type(query) is str:
        msg = query

    if request.method == 'GET':
        return render_template('login.html', message=msg)
    elif request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        user = db.get_db_user_by_username(username)
        print(user)
        if user:
            if md5(password.encode('utf-8')).hexdigest() == md5(user['password'].encode('utf-8')).hexdigest():
                login_user(User(username))
                return redirect(url_for('profile'))
        return redirect(url_for('login', msg="You haven't been registered. Please register first!"))
    else:
        return 400


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()
    # read model from file
    # content = ["What's the game plan? It was a nice run, Kev; had to close out some day. Nobody wins them all."]
    # res = model.predict(content)
    # print(res)

import os

from pymongo import MongoClient
from flask.cli import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_PW = os.getenv("SECRET_PW")


class User:
    """
    insert user information into database
    """

    def __init__(self):
        try:
            self.client = MongoClient("mongodb+srv://" + SECRET_KEY + ":" + SECRET_PW +
                                      "@cluster0.dfeu0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

            self.db = self.client.forum
            self.db_users = self.db.Users
            self.db_posts = self.db.Posts

        except ConnectionAbortedError:
            print("[ERROR]: Connection Error")

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

    def get_all_posts_by_username(self, data):
        return list(self.db_posts.find({'user_id': data}, projection={'_id': False}))


if __name__ == "__main__":
    user = User()
    d = {"_id": "td2@illinois.edu",
         "password": "password",
         "post_count": 0,
         "depression_count": 0
         }

    p = {"content": "Hello123",
         "is_depressed": 1,
         "user_id": "td2@illinois.edu",
         "title": "see",
         "created_time": "now"
        }

    print(user.post_user(d))
    print(user.get_db_user_by_username("td2@illinois.edu"))
    res = user.get_all_posts_by_username("1")
    time = res[0]['created_time']
    print(res)
    print(time)

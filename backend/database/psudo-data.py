import string
import random
import datetime
from database import Database

database = Database()
def random_string(length=4):
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=length))
    return res


def insert_users():
    posts = database.get_all_posts(False)
    for p in posts:
        curr_user = p['user_id']
        password = random_string(7)
        user = {"_id": curr_user,
                "password": password,
                "post_count": random.randint(1, 2),
                "depression_count": random.randint(0, 1)
                }
        database.post_user(user)


if __name__=="__main__":
    # for i in range(10):
    #     username = random_string(4)
    #     for j in range(2):
    #         title = random_string(6)
    #         content = random_string(20)
    #
    #         rand_num = random.randint(0,1)
    #         depress = True if rand_num == 0 else False
    #         post = {"content": content,
    #                  "is_depressed": depress,
    #                  "user_id": username,
    #                  "title": title,
    #                  "created_time": datetime.datetime.now(),
    #                  "is_post": True
    #                 }
    #         database.insert_post(post)
    insert_users()
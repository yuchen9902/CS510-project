user_attr = ["_id",
             "password",
             "post_count",
             "depression_count"
            ]

user_schema = [
    ("collMod", "Users"),
    ("validator", {
        "$jsonSchema": {
            "bsonType": "object",
            "required": user_attr,
            "properties": {
                "post_count": {
                    "bsonType": "int"
                },
                "depression_count": {
                    "bsonType": "int"
                }
            }
        }
    }),
    ("validationLevel", "strict")
]

required_post_attr = ["user_id",
                     "content",
                     "is_depressed",
                     "is_post",
                     "created_time"
                     ]

post_schema = [
    ("collMod", "Posts"),
    ("validator", {
        "$jsonSchema": {
            "bsonType": "object",
            "required": required_post_attr,
            "properties": {
                "is_depressed": {
                    "bsonType": "bool"
                },
                "is_post": {
                    "bsonType": "bool"
                },
                "created_time": {
                    "bsonType": "date"
                },
                "to_which_post": {
                    "bsonType": "string"
                }
            }
        }
    }),
    ("validationLevel", "strict")
]

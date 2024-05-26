#!/usr/bin/env python3
""" """
from models.engine.db_storage import DBStorage
from models.user import User
from models.post import Post

storage = DBStorage()

# Create a new user
new_user = User(
    user_name="johndoe",
    name="John Doe",
    email="johndeoo@example.com",
    password="password123",  # Note that we're passing 'password' here
    bio="A software developer.",
    profile_picture_url="http://example.com/johndoe.jpg"
)
storage.new(new_user)
storage.save()
new_post = Post(
    user_id=new_user.id,
    content="This is a post content.",
    media_type="image",
    media_url="http://example.com/media.jpg"
)


# storage.new(new_user)
storage.new(new_post)
storage.save()

# Query all users
users = storage.all()

for k, v in users.items():
    print(k, v)


# Close the session
storage.close()


# SG_DB_USER=sg_test_user SG_DB_PWD=sg_test_pwd SG_DB_HOST=localhost SG_DB_NAME=sg_test_db ./main.py

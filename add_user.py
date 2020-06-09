from main import db
from main.models import User, Post
from werkzeug.security import generate_password_hash
from faker import Faker
import sys
import os
from random import choice
from main.posts.picture_handler import add_photo
import argparse

class MockFileField():
    def __init__(self, filename):
        self.filename=filename

    def read(self):
        return open(self.filename,'rb').read()

parser = argparse.ArgumentParser()
parser.add_argument('--flush-db',help='Deletes everything fro DB.',action='store_true')
parser.add_argument('--username', help='Provide a new admin username.', type=str)
parser.add_argument('--password', help='Provide a password for the username provided.', type=str)
parser.add_argument('--posts', help='Create n mock posts to test blog layout.', type=int)
parser.add_argument('--delete-user', help='Delete a specific user from db.', type=str)
args = parser.parse_args()

if args.flush_db:
    db.reflect()
    db.drop_all()
    db.create_all()

    print('Database cleared!')

if args.username and args.password:
    if User.query.filter_by(username=args.username).first():
        print('Username {} already exists.'\
            .format(User.query.filter_by(username=args.username))\
                .first().username)
    else:
        test_user = User(
            username=args.username,
            password_hash=generate_password_hash(args.password)
        )
        db.session.add_all([test_user])
        db.session.commit()
        print('User {} created.'.format(args.username))   

# check if both username and password have been provided
elif bool(args.username) is not bool(args.password):
    print('Please provide both --username and --password')

if args.posts:
    
    image_file = MockFileField(filename='static/img/home.jpg')
    image_uri=add_photo(image_file)
    fake = Faker()
    fake.text()
    posts = []
    n = 0

    while n < int(args.posts):
        post = Post(
            title = fake.text(100),
            author_id=1,
            image_caption=fake.text(40),
            image_uri=image_uri,
            text_raw = fake.text(1000)
        )
        posts.append(post)
        if n > 1000:
            break
        n+=1

    db.session.add_all(posts)
    db.session.commit()
    print('{} mock posts created.'.format(n))

if args.delete_user:

    user = User.query.filter_by(username=args.delete_user).first()

    # check if user exists; exit if it doesn't
    if user is None:  
        print('User <{}> does not exist!'.format(args.delete_user))
        sys.exit()

    # delete user
    db.session.delete(user)
    db.session.commit()
    
    print(
        'User <{}> deleted from database!'\
            .format(args.delete_user)
    )
from main import db
from main.models import User, Post
from werkzeug.security import generate_password_hash
from faker import Faker
import sys
import os
from random import choice
from main.posts.picture_handler import add_photo
import argparse

class BlogAdminTasks():

    def __init__(self):
        pass
    
    @staticmethod
    def add_user(username,password):
        user = User.query\
            .filter_by(username=username)\
                .first()

        if user is not None:
            return print('Username {} already exists.'.format(user))

        else:
            user = User(
                    username=username,
                    password_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
        
            return print('User {} created.'.format(username))
            

    @staticmethod
    def delete_user(username):
        user = User.query\
            .filter_by(username=username)\
                .first()

        # check if user exists; exit if it doesn't
        if user is None:  
            return print('User <{}> does not exist!'\
                .format(args.delete_user))

        # delete user
        db.session.delete(user)
        db.session.commit()
        
        return print('User <{}> deleted from database!'\
            .format(args.delete_user))

    @staticmethod
    def flush_db(flush=False):

        if flush:
            db.reflect()
            db.drop_all()
            db.create_all()

            return print('Database cleared!')
    
    @staticmethod
    def mock_posts(n=0):
        image_file = MockFileField(filename='static/img/home.jpg')
        image_uri=add_photo(image_file)
        fake = Faker()
        fake.text()
        posts = []
        counter = 0

        while counter < int(n):
            post = Post(
                title = fake.text(100),
                author_id=1,
                image_caption=fake.text(40),
                image_uri=image_uri,
                text_raw = fake.text(1000)
            )
            posts.append(post)
            if counter > 1000:
                break
            counter+=1

        db.session.add_all(posts)
        db.session.commit()
        return print('{} mock posts created.'.format(n))

class MockFileField():
    def __init__(self, filename):
        self.filename=filename

    def read(self):
        return open(self.filename,'rb').read()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--flush-db', 
        help='Deletes everything fro DB.',
        action='store_true')

    parser.add_argument('--username', 
        help='Provide a new admin username.', 
        type=str)

    parser.add_argument('--password', 
        help='Provide a password for the username provided.', 
        type=str)

    parser.add_argument('--posts', 
        help='Create n mock posts to test blog layout.', 
        type=int)

    parser.add_argument('--delete-user', 
        help='Delete a specific user from db.', 
        type=str)

    parser.add_argument('--dry-run', 
        help='Tests all of the script function. CLEARS DB!!', 
        action='store_true')

    args = parser.parse_args()

    if args.dry_run:

        response = ''

        while response.lower() not in ['y','n']:

            response = input('This test will clear all of the database.\n'+
            'Are you want to continue? [y|n]: ')
                
        
        if response.lower() == 'n':
            print('Dry run aborted by user input.')
            sys.exit()

        elif response.lower() == 'y':
            BlogAdminTasks.flush_db(flush=True)
            BlogAdminTasks.add_user(
                username='test',
                password='test'
            )
            BlogAdminTasks.mock_posts(n=10)

            print(User.query.filter_by(username='test').first())
            print(Post.query.filter_by(author_id=1).first())

            BlogAdminTasks.flush_db(flush=True)

    if args.flush_db:
        BlogAdminTasks.flush_db(flush=True)

    if args.username and args.password:
        BlogAdminTasks.add_user(
            username=args.username,
            password=args.password
        )
    elif bool(args.username) is not bool(args.password):
        print('Please provide both --username and --password')

    if args.posts:
        BlogAdminTasks.mock_posts(n=args.posts)

    if args.delete_user:
        BlogAdminTasks.delete_user(username=args.delete_user)

from main import db
from main.models import User, Post
from werkzeug.security import generate_password_hash
from faker import Faker
import sys
import os
from random import choice

db.reflect()
db.drop_all()
db.create_all()

if sys.argv[1]=='--username' and sys.argv[3]=='--password':
    if User.query.filter_by(username=sys.argv[2]).first():
        print('Username {} already exists.'.format(User.query.filter_by(username=sys.argv[2])).first().username)
    else:
        test_user = User(
            username=sys.argv[2],
            password_hash=generate_password_hash(sys.argv[4])
        )
        db.session.add_all([test_user])
        db.session.commit()
        print('User {} created.'.format(sys.argv[2]))
else:
    print('Correct syntax is "python add_user.py -username <username> --password <password>"')

if sys.argv[5]=='--posts' and sys.argv[6].isdigit():
    fake = Faker()
    fake.text()
    posts = []
    n = 0
    while n < int(sys.argv[6]):
        post = Post(
            title = fake.text(100),
            author_id=1,
            image_caption=fake.text(40),
            image_uri=choice(os.listdir('static/img/thumbnail')) if os.listdir('static/img/thumbnail') else '../home.jpg',
            text_raw = fake.text(1000)
        )
        posts.append(post)
        if n > 1000:
            break
        n+=1

    db.session.add_all(posts)
    db.session.commit()

print('{} mock posts created.'.format(n))

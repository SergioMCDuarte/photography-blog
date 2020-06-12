from main import db
from datetime import datetime
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from markdown import markdown
import bleach

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    posts = db.relationship('Post', backref='user')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=True)
    password_hash = db.Column(db.String(512), nullable=True)

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def __repr__(self):
        return '{}'.format(self.username)

    def verify_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User',backref='post',uselist=False)
    created_on = db.Column(db.DateTime, nullable=True)
    updated_on = db.Column(db.DateTime, nullable=True)
    image_caption = db.Column(db.String(256), nullable=True, default='')
    image_uri = db.Column(db.String(256), nullable=True, default='')
    text_raw = db.Column(db.Text, nullable=True)
    text_html = db.Column(db.Text, nullable=True)
    text_preview = db.Column(db.Text, nullable=True)

    def __init__(
        self,
        title,
        author_id,
        image_caption,
        image_uri,
        text_raw
        ):

        self.title = title
        self.created_on = datetime.now()
        self.updated_on = None
        self.author_id=author_id
        self.image_caption = image_caption
        self.image_uri = image_uri
        self.text_raw = text_raw

    def __repr__(self):
        return str({
            'title': self.title,
            'author': self.author,
            'id': self.id,
            'created_on': self.created_on,
            'image_caption': self.image_caption,
            'image_uri': self.image_uri,
            'text': self.text_raw
        })

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags=['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                      'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                      'h1', 'h2', 'h3', 'p']
        target.text_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

        target.text_preview = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=[], strip=True))[0:200]

#db.create_all()
db.event.listen(Post.text_raw, 'set', Post.on_changed_body)

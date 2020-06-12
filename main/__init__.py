from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_pagedown import PageDown
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'static'))

# -- App Configurations -- #
bootstrap = Bootstrap(app=app)
app.config['SECRET_KEY'] = 'Develpment Key'  # change before deployment

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app=app)

Migrate(app=app,db=db)

login_manager = LoginManager()
login_manager.login_view = 'core.login'
login_manager.init_app(app)

# -- Markdown Interpreter -- #
pagedown = PageDown()
pagedown.init_app(app)

# -- Registered Blueprints -- #
from main.core.views import core
from main.posts.views import posts
from main.gallery.views import gallery

app.register_blueprint(core)
app.register_blueprint(posts)
app.register_blueprint(gallery)

## --- errors handling -- ##
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

## -- Admin Page -- ##
from main.models import User, Post
app.config['FLASK_ADMIN_SWATCH'] = 'sandstone'

class BlogModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('core.login', next=request.url))

class UserView(BlogModelView):
    column_exclude_list = ['password_hash']

class PostView(BlogModelView):
    column_exclude_list = [
        'text_raw',
        'text_html',
        'text_preview',
        'user'
    ]

admin = Admin(app=app, template_mode='bootstrap3')
admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
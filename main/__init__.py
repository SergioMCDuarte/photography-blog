from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pagedown import PageDown

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

## -- DataBase Setup -- ##

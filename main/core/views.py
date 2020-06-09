from flask import render_template, request, Blueprint, redirect, url_for, flash, request
from main.core.forms import SignInForm
from main.models import Post, User
from main import login_manager
from flask_login import login_user, login_required, logout_user

core = Blueprint(
    'core', __name__,
    template_folder='templates/core'
)

@core.route('/', methods=['POST','GET'])
def index():
    page = request.args.get('page', 1, type=int)

    posts = Post\
            .query\
            .filter_by(author_id=1)\
            .order_by(Post.created_on.desc()) \
            .paginate(page, 3, False)

    next_url = url_for('core.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('core.index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', posts=posts,
                            next_url=next_url, prev_url=prev_url)

@core.route('/about', methods=['POST','GET'])
def about():
    return render_template('about.html')

@core.route('/contact', methods=['POST','GET'])
def contact():
    return render_template('contact.html')

@core.route('/login', methods=['POST','GET'])
def login():
    form = SignInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and user.verify_password_hash(form.password.data):
            login_user(user)
            next = request.args.get('next')

            if next is None or not next.startswith('/'):
                next = url_for('core.index')

            return redirect(next)

            flash("Invalid Username or Password")
    return render_template('login.html', form=form)

@core.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from flask import render_template, request, Blueprint, redirect, url_for
from main.models import Post

gallery = Blueprint('gallery', __name__)

@gallery.route('/gallery')
def view_gallery():

    posts = Post\
            .query\
            .filter_by(author_id=1)\
            .order_by(Post.created_on.desc())

    return render_template('gallery.html', posts=posts)

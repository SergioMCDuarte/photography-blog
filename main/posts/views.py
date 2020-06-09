from flask import render_template, request, Blueprint, redirect, url_for
from main.posts.forms import NewPostForm, EditPostForm, DeletePostForm
from main.core.forms import SignInForm
from main.models import User, Post
from flask_login import login_required, current_user
import os
from main import db
from main.posts.picture_handler import add_photo

posts = Blueprint(
    'posts', __name__,
    template_folder='templates/posts'
)

@posts.route('/posts/<int:id>')
def view_post(id):

    post = Post.query.get_or_404(id)

    if post:
        return render_template('post.html', post=post)
    else:
        return render_template('404.html')

@posts.route('/posts/<id>/edit', methods=['POST','GET'])
@login_required
def edit_post(id):
    form = EditPostForm()
    delete_form = DeletePostForm()

    post = Post.query.get_or_404(id)

    if request.method == 'GET': # necessary to pre-fill text area
        form.post_text.data = post.text_html  # only on the get method in order to correctly update on the post

    if form.validate_on_submit():

        post.title = form.post_title.data
        post.image_caption=form.image_caption.data
        post.image_uri=add_photo(form.image_file.data)
        post.text_raw = form.post_text.data

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('core.index'))

    if delete_form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()

        return redirect(url_for('core.index'))
    return render_template('edit_post.html', post=post, form=form, delete_form=delete_form)

@posts.route('/posts/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = NewPostForm()

    if form.validate_on_submit():
        print(add_photo(form.image_file.data))
        post = Post(
            title = form.post_title.data,
            author_id=current_user.id,  # will always be 1 in this case
            image_caption=form.image_caption.data,
            image_uri=add_photo(form.image_file.data),
            text_raw = form.post_text.data
        )
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('core.index'))

    return render_template('new_post.html', form=form)

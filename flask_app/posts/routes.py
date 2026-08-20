from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from flask_app import db
from flask_app.posts.forms import PostForm
from flask_app.models import Post

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    # Uses the Form to extract the User Input Data
    form = PostForm()
    # Validates the form using the Validators defined in the PostForm class
    if form.validate_on_submit():
        # Creates a new Post object with the title, content, and author (current user) from the form data and adds it to the database
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))

    # Passes the form parameter to access this form in the HTML template
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    # Queries the Post object from the database using the post_id parameter and returns a 404 error if not found
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Checks if the current user is the author of the post. If not, aborts with a 403 error (Forbidden)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    # Validates the form using the Validators defined in the PostForm class
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        # Commits the changes to the database after updating the post's title and content
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        # Pre-populates the form fields with the current post's title and content when the page is loaded for the first time
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create_post.html", title="New Post", form=form, legend="Update Post")

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    # Deletes the post from the database and commits the changes
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
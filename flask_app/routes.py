import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flask_app import app, db, bcrypt
from flask_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# Creates the Home Page and About Page routes
@app.route("/")
@app.route("/home")
def home():
    # Gets the page number from the query parameters, defaulting to 1 if not provided
    page = request.args.get('page', 1, type=int)
    # Queries the Post model to get all posts, paginated with 5 posts per page. The posts are ordered by the date they were posted in descending order (newest first)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template("home.html", posts=posts)

# Creates the About Page route
@app.route("/about")
def about():
    return render_template("about.html", title="About")

# Need to add the methods to allow GET/POST requests (using the Submit Button)
@app.route("/register", methods=['GET', 'POST'])
def register():
    # Redirects to Home Page is user is logged in correctly
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    # Uses the Form to extract the User Input Data
    form = RegistrationForm()
    # Validates the form using the Validators defined in the RegistrationForm class
    if form.validate_on_submit():
        # Hashes the User Password before storing in the Database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Creates an User, and stores in the DB
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # Provides a Flash Message after successful registration. Built-in category for Bootstrap
        flash('Your acccount has been created! You are now able to log in.', 'success')

        return redirect(url_for('login'))
    
    # Passes the form parameter to access this form in the HTML template
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Redirects to Home Page if user is logged in correctly
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    # Uses the Form to extract the User Input Data
    form = LoginForm()
    # Validates the form using the Validators defined in the LoginForm class
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Validates User email and password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # Gets the next parameter from the url if it exists
            next_page = request.args.get('next')
            
            # Redirects to the next_page or Home Page
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            # Provides a Flash Message after Log in failure. Built-in category for Bootstrap
            flash('Login Unsuccessful. Please check email and password', 'danger')

    # Passes the form parameter to access this form in the HTML template
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    # Logs the user out
    logout_user()

    return redirect(url_for('home'))

# Function to resize & save the profile picture uploaded by the user
def save_picture(form_picture):
    # Generates a random hex to avoid filename conflicts and maintain uniqueness
    random_hex = secrets.token_hex(8)
    # Splits the filename into name and extension - the extension is needed to save the file in the correct format
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # Creates the path to save the profile picture in the static/profile_pics directory
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Resize the image to a smaller size to save space and improve performance
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
# Tells the user that Login is required to access this page/route. The login route is specified by "login_view" in the __init__.py file
@login_required
def account():
    # Uses the Form to extract the User Input Data
    form = UpdateAccountForm()
    # Validates the form using the Validators defined in the UpdateAccountForm class
    if form.validate_on_submit():
        # Checks if the user has uploaded a new profile picture
        if form.picture.data:
            # Saves the new profile picture and updates the current user's image_file attribute
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        # Updates the current user's username and email attributes with the new values from the form
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        # Provides a Flash Message after successful account update. Built-in category for Bootstrap
        flash('Your account has been updated!', 'success')

        return redirect(url_for('account'))
    elif request.method == 'GET':
        # Pre-populates the form fields with the current user's username and email when the page is loaded for the first time
        form.username.data = current_user.username
        form.email.data = current_user.email

    # Generates the URL for the current user's profile picture to be displayed on the account page
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    # Renders the account.html template with the title, image_file, and form parameters
    return render_template("account.html", title="Account", image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
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
        return redirect(url_for('home'))

    # Passes the form parameter to access this form in the HTML template
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")


@app.route("/post/<int:post_id>")
def post(post_id):
    # Queries the Post object from the database using the post_id parameter and returns a 404 error if not found
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        # Pre-populates the form fields with the current post's title and content when the page is loaded for the first time
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create_post.html", title="New Post", form=form, legend="Update Post")

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    # Deletes the post from the database and commits the changes
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

# Creates the User Posts route to display all posts by a specific user
@app.route("/user/<string:username>")
def user_posts(username):
    # Gets the page number from the query parameters, defaulting to 1 if not provided
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # The query filters the posts by the author (user) and orders them by the date they were posted in descending order. The results are then paginated to show 5 posts per page, based on the current page number.
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5, page=page)
    return render_template("user_posts.html", posts=posts, user=user)
from flask import Blueprint, render_template, request
from flask_app.models import Post

main = Blueprint('main', __name__)

# Creates the Home Page and About Page routes
@main.route("/")
@main.route("/home")
def home():
    # Gets the page number from the query parameters, defaulting to 1 if not provided
    page = request.args.get('page', 1, type=int)
    # Queries the Post model to get all posts, paginated with 5 posts per page. The posts are ordered by the date they were posted in descending order (newest first)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template("home.html", posts=posts)

# Creates the About Page route
@main.route("/about")
def about():
    return render_template("about.html", title="About")


from flask import Blueprint, redirect, render_template, request, url_for
from models import Post, db
from forms import PostForm

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/adios")
def adios():
    return "adios"

@main.route("/posts")
def posts():
    posts = Post.query.all()
    return render_template("posts.html", posts=posts)

@main.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)

@main.route("/createpost", methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = request.form.get("title")
        post = Post(title=title)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("main.home"))
    return render_template("create_post.html", form=form)
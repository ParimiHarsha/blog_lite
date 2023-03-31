import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_jwt_extended import JWTManager
from flask_login import LoginManager, current_user, login_required, login_user
from flask_security import Security, SQLAlchemyUserDatastore

from config import LocalDevelopmentConfig
from forms import BlogForm, LoginForm, SignupForm
from models import Blog, Role, User, db

app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)

# Define the Flask-Security data store
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Initialize Flask-Security and Flask-JWT-Extended
security = Security(app=app, datastore=user_datastore)

db.init_app(app)
app.app_context().push()


@app.route("/")
def index():
    """Contrller for the landing page"""
    return render_template("index.html")


@app.route("/feed")
@login_required
def feed():
    """Feed Controller"""

    posts = Blog.query.order_by(Blog.updated_at.desc()).all()
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blog(
            title=form.title.data,
            content=form.content.data,
            author=current_user,
        )
        db.session.add(blog)
        db.session.commit()
        flash("Your post has been created!")
        return redirect(url_for("feed"))
    return render_template("feed.html", posts=posts, form=form)


# @app.route("/blogs", methods=["GET"])
# def get_blogs():
#     blogs = Blog.query.all()
#     return render_template("blogs.html", blogs=blogs)


@app.route("/blogs/create", methods=["GET", "POST"])
def create_blog():
    form = BlogForm()

    if request.method == "POST" and form.validate_on_submit():
        blog = Blog(
            title=form.title.data,
            caption=form.caption.data,
            image_url=form.image_url.data,
            created_at=datetime.now(),
            user_id=current_user.id,
        )
        db.session.add(blog)
        db.session.commit()
        flash("Blog created successfully!", "success")
        return redirect(url_for("feed"))

    return render_template("create_blog.html", form=form)


@app.route("/blogs/update/<int:id>", methods=["GET", "POST"])
def update_blog(id):
    blog = Blog.query.get_or_404(id)
    form = BlogForm(obj=blog)

    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(blog)
        db.session.commit()
        flash("Blog updated successfully!", "success")
        return redirect(url_for("feed"))  # maybe change this to userpage later

    return render_template("update_blog.html", form=form, blog_id=id)


@app.route("/blogs/delete/<int:id>", methods=["POST"])
def delete_blog(id):
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    flash("Blog deleted successfully!", "success")
    return redirect(url_for("feed"))  # maybe change this to userpage later


@app.route("/user/<username>")
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    blog_count = Blog.query.filter_by(user_id=user.id).count()
    followers_count = len(user.followers)
    following_count = user.friends.count()
    blog_posts = Blog.query.filter_by(user_id=user.id).all()
    return render_template(
        "user_profile.html",
        user=user,
        blog_count=blog_count,
        followers_count=followers_count,
        following_count=following_count,
        blog_posts=blog_posts,
    )


if __name__ == "__main__":
    # with app.app_context():
    #     db.drop_all()  # to reset all the tables in the database
    #     db.create_all()
    app.run(host="0.0.0.0", debug=True, port=8080)

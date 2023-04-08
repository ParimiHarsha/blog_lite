from datetime import datetime

from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from application.models import Blog, User, db
from forms import BlogForm


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


@app.route("/userprofile")
@login_required
def user_profile():
    # user = User.query.filter_by(username=username).first_or_404()
    blog_count = Blog.query.filter_by(user_id=current_user.id).count()
    followers_count = len(current_user.followers.all())
    following_count = len(current_user.friends)
    blog_posts = Blog.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "user_profile.html",
        user=current_user,
        blog_count=blog_count,
        followers_count=followers_count,
        following_count=following_count,
        blog_posts=blog_posts,
    )

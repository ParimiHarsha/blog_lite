from datetime import datetime

from flask import current_app as app
from flask import flash, redirect, render_template, request
from flask_caching import Cache
from flask_login import current_user, login_required, logout_user

from application.forms import BlogForm
from application.models import Blog, User, db

cache = Cache(app)


@app.route("/")
@login_required
@cache.memoize(600)
def feed():
    """Feed Controller"""

    # Create a cache key that includes the user's id
    cache_key = f"feed_{current_user.id}"
    # Check if the result is in the cache
    result = cache.get(cache_key)
    if result is None:
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
            return redirect("/")

        result = render_template(
            "feed.html",
            posts=posts,
            form=form,
            auth_token=current_user.get_auth_token(),
        )

        # Store the result in the cache with the cache key that depends on the user's id
        cache.set(cache_key, result)

    return result


@app.route("/blogs/create", methods=["GET", "POST"])
def create_blog():
    if request.method == "POST":
        try:
            f = request.files["image"]
            f.save(f"static/{f.filename}")
            image_url = f"static/{f.filename}"
        except IsADirectoryError:
            image_url = request.form.get("image_url")
        blog = Blog(
            title=request.form.get("title"),
            caption=request.form.get("caption"),
            image_url=image_url,
            created_at=datetime.now(),
            user_id=current_user.id,
        )
        db.session.add(blog)
        db.session.commit()
        flash("Blog created successfully!", "success")
        return redirect("/")

    return render_template("create_blog.html")


@app.route("/user_profile/<int:user_id>")
@login_required
def user_profile(user_id):
    user = User.query.get(user_id)
    blog_count = Blog.query.filter_by(user_id=user.id).count()
    followers_count = len(user.followers.all())
    following_count = len(user.friends)
    blog_posts = Blog.query.filter_by(user_id=user.id).all()
    return render_template(
        "user_profile.html",
        user=user,
        blog_count=blog_count,
        followers_count=followers_count,
        following_count=following_count,
        blog_posts=blog_posts,
        auth_token=current_user.get_auth_token(),
    )


@app.route("/logout_user")
@login_required
def logout():
    # Invalidate the cache for the current user
    cache.delete(f"feed_{current_user.id}")
    # Log out the user
    logout_user()
    return redirect("/login")

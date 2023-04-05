from datetime import datetime

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask.views import MethodView
from flask_login import current_user, login_required
from flask_restful import Api, Resource
from flask_security import Security, SQLAlchemyUserDatastore

from config import LocalDevelopmentConfig
from forms import BlogForm
from models import Blog, Friends, Role, User, db

app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)

# Define the Flask-Security data store
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Initialize Flask-Security and Flask-JWT-Extended
security = Security(app=app, datastore=user_datastore)

db.init_app(app)
api = Api(app)
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
    )


# class UserAPI(Resource):
#     # get user
#     def get():
#         query = request.args.get("query")
#         users = User.query.filter(User.username.contains(query)).all()
#         return jsonify({"users": [user.serialize() for user in users]})

#     # get user profile
#     def get(user_id):
#         user = User.query.get(user_id)
#         if user is None:
#             return jsonify({"error": "User not found"}), 404
#         return jsonify(user.serialize())


# class FollowAPI(Resource):
#     # get followers
#     def get(self, user_id):
#         user = User.query.get(user_id)
#         if user is None:
#             return jsonify({"error": "User not found"}), 404
#         followers = Friends.query.filter_by(followed_id=user_id).all()
#         return jsonify(
#             {"followers": [follower.follower.serialize() for follower in followers]}
#         )

#     # user following
#     def post(self, user_id):
#         user = User.query.get(user_id)
#         if user is None:
#             return jsonify({"error": "User not found"}), 404
#         following = Friends.query.filter_by(follower_id=user_id).all()
#         return jsonify(
#             {"following": [followed.followed.serialize() for followed in following]}
#         )


class SearchAPI(MethodView):
    # API for searching users
    # @app.route('/search')
    def get(self):
        search_term = request.args.get("searchTerm")

        if search_term:
            users = User.query.filter(User.username.ilike(f"%{search_term}%")).all()
        else:
            users = User.query.all()
        breakpoint()
        result = []
        for user in users:
            result.append(
                {"id": user.id, "username": user.username, "email": user.email}
            )
        return jsonify({"users": result})

    # API for following a user
    # @app.route('/users/<int:user_id>/follow', methods=['POST'])
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": f"User with id {user_id} does not exist"}), 404
        breakpoint()

        # Follow the user here
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": f"User with id {user_id} does not exist"}), 404
        # current_user = (
        #     get_current_user()
        # )  # You need to implement this function to get the current user
        if not current_user.is_authenticated:
            return jsonify({"error": "you are not authenticated"})
        if current_user == user:
            return jsonify({"error": "You cannot follow yourself"}), 400
        if current_user.is_following(user):
            return jsonify({"error": f"You are already following {user.username}"}), 400

        current_user.follow(user)
        db.session.commit()
        return jsonify({"message": f"You are now following {user.username}."})

    # API for unfollowing a user
    # @app.route('/users/<int:user_id>/unfollow', methods=['POST'])
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": f"User with id {user_id} does not exist"}), 404

        # Unfollow the user here
        # ...

        return jsonify({"message": f"You are no longer following {user.username}."})


# api.add_resource(UserAPI, "/api/user", "/api/<int:user_id>")
# api.add_resource(FollowAPI, "/api/<int:user_id>")
api.add_resource(
    SearchAPI,
    "/api/search",
    "/api/users/<int:user_id>/follow",
    "/api/users/<int:user_id>/unfollow",
)


if __name__ == "__main__":
    app.run()


if __name__ == "__main__":
    # with app.app_context():
    #     db.drop_all()  # to reset all the tables in the database
    #     db.create_all()
    app.run(host="0.0.0.0", debug=True, port=8080)

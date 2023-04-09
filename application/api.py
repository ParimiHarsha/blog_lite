import datetime
import os

from flask import jsonify, make_response, request
from flask_login import current_user
from flask_restful import Resource
from flask_security import auth_token_required

from application.models import Blog, User, db
from application.tasks import export_csv


class CurrentUserAPI(Resource):
    """API to fetch the Current User"""

    @auth_token_required
    def get(self):
        return current_user.to_dict()


class SearchAPI(Resource):
    """API for searching users"""

    @auth_token_required
    def get(self):
        search_term = request.args.get("search")
        if search_term:
            users = (
                User.query.filter(User.username.ilike(f"%{search_term}%"))
                .limit(5)
                .all()
            )
        else:
            users = []
        result = [user.to_dict() for user in users]
        return jsonify({"users": result})


class FollowAPI(Resource):
    """API for following a user"""

    @auth_token_required
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response(
                jsonify({"error": f"User with id {user_id} does not exist"}), 404
            )
        if not current_user.is_authenticated:
            return make_response(jsonify({"error": "you are not authenticated"}))
        if current_user == user:
            return make_response(jsonify({"error": "You cannot follow yourself"}, 400))
        if current_user.is_following(user):
            return make_response(
                jsonify({"error": f"You are already following {user.username}"}), 400
            )
        current_user.follow(user)
        db.session.commit()
        return make_response(
            jsonify({"message": f"You are now following {user.username}."})
        )


class UnfollowAPI(Resource):
    """API for unfollowing a user"""

    @auth_token_required
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": f"User with id {user_id} does not exist"}), 404

        if not current_user.is_authenticated:
            return make_response(jsonify({"error": "you are not authenticated"}))
        if current_user == user:
            return make_response(
                jsonify({"error": "You cannot unfollow yourself"}, 400)
            )
        if not current_user.is_following(user):
            return make_response(
                jsonify({"error": f"You are not following {user.username}"}), 400
            )
        current_user.unfollow(user)
        return make_response(
            jsonify({"message": f"You are no longer following {user.username}."})
        )


class BlogsAPI(Resource):
    """API for blogs."""

    @auth_token_required
    def get(self):
        user_id = request.args.get("user_id")
        user = User.query.filter_by(id=user_id).first()
        # Get the list of followers' ids
        follower_ids = [follower.id for follower in user.followers] + [user_id]
        # Get the blogs of followers
        blogs = (
            Blog.query.filter(Blog.user_id.in_(follower_ids))
            .order_by(Blog.updated_at.desc())
            .all()
        )
        blogs_list = [blog.to_dict() for blog in blogs]
        return make_response(jsonify({"blogs": blogs_list}))

    @auth_token_required
    def put(self, blog_id):
        # Get the blog with the given ID from the database
        blog = Blog.query.get_or_404(blog_id)
        # Parse the JSON request data
        data = request.get_json()
        # Update the blog fields with the data from the request
        blog.title = data.get("title", blog.title)
        blog.caption = data.get("caption", blog.caption)
        blog.image_url = data.get("image_url", blog.image_url)

        # Update the blog in the database
        db.session.commit()

        # Return a JSON response with a success message
        return jsonify({"message": "Blog updated successfully"})

    @auth_token_required
    def delete(self, blog_id):
        blog = Blog.query.get(blog_id)
        if not blog:
            return make_response(jsonify({"message": "Blog not found"}), 404)
        db.session.delete(blog)
        db.session.commit()

        return make_response(jsonify({"message": "Blog deleted successfully"}), 200)


class ExportCSVAPI(Resource):
    """API for exporting blogs as CSVs"""

    def post(self):
        blogs = request.get_json()
        user = blogs[0]["user"]

        cur_dir = f"/Users/parimiharsha/Downloads/downloaded_blogs/{user['id']}"
        if not os.path.isdir(cur_dir):
            os.mkdir(cur_dir)

        for blog in blogs:
            del blog["user"]
        export_csv.delay(
            blogs,
            f"/Users/parimiharsha/Downloads/downloaded_blogs/{user['id']}/{datetime.datetime.now()}.csv",
        )

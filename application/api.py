from flask import jsonify, make_response, request
from flask.views import MethodView
from flask_login import current_user

from application.models import Blog, User, db


class SearchAPI(MethodView):
    """API for searching users"""

    def get(self):
        search_term = request.args.get("searchTerm")

        if search_term:
            users = (
                User.query.filter(User.username.ilike(f"%{search_term}%"))
                .limit(5)
                .all()
            )
        else:
            users = User.query.limit(5).all()

        result = [user.to_dict() for user in users]
        return jsonify({"users": result})


class FollowAPI(MethodView):
    """API for following a user"""

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
        if current_user.is_following(user):  # TODO:may be redundant
            return make_response(
                jsonify({"error": f"You are already following {user.username}"}), 400
            )
        current_user.follow(user)
        db.session.commit()
        return make_response(
            jsonify({"message": f"You are now following {user.username}."})
        )


class UnfollowAPI(MethodView):
    """API for unfollowing a user"""

    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": f"User with id {user_id} does not exist"}), 404

        # Unfollow the user here
        if not current_user.is_authenticated:
            return make_response(jsonify({"error": "you are not authenticated"}))
        if current_user == user:
            return make_response(
                jsonify({"error": "You cannot unfollow yourself"}, 400)
            )
        if not current_user.is_following(user):  # TODO:may not be needed
            return make_response(
                jsonify({"error": f"You are not following {user.username}"}), 400
            )
        current_user.unfollow(user)
        return make_response(
            jsonify({"message": f"You are no longer following {user.username}."})
        )


class BlogsAPI(MethodView):
    """API which returns a list of blogs."""

    def get(self):
        blogs = Blog.query.order_by(
            Blog.updated_at.desc()
        ).all()  # We can also only return the blogs of followers first and then all other blogs
        blogs_list = [blog.to_dict() for blog in blogs]
        return make_response(jsonify({"blogs": blogs_list}))

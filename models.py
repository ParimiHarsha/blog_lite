from datetime import datetime

from flask_security import RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

friends = db.Table(
    "friends",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("friend_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)
# Define a User model for Flask-Security
class User(db.Model, UserMixin):
    """This is the model for the user table in blog-store.db"""

    __table_name__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)

    roles = db.relationship(
        "Role", secondary="user_roles", backref=db.backref("users", lazy="dynamic")
    )

    # add a many-to-many relationship with itself through the Friend model
    friends = db.relationship(
        "User",
        secondary=friends,
        primaryjoin=("friends.c.user_id == User.id"),
        secondaryjoin=("friends.c.friend_id == User.id"),
        # backref=db.backref("friend_of", lazy="dynamic"),
        backref="followers",
        lazy="dynamic",
    )


class Blog(db.Model):
    """This is the model for the blog table in blog-store.db"""

    __table_name__ = "blog"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(250), nullable=False)
    image_url = db.Column(db.String(250))
    # content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="blogs")

    def __repr__(self):
        return f"<Blog {self.id}>"


# class Friends(db.Model):
#     """This is the model for the friends relationship in blog-store.db"""

#     __table_name__ = "friends"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id_1 = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     user_id_2 = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class UserBlog(db.Model):
    """This is the model for the user-blog relationship in blog-store.db"""

    __table_name__ = "user_blog"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"), nullable=False)

    # Add a unique constraint to ensure a user can only write one blog per post
    # __table_args__ = (
    #     db.UniqueConstraint("user_id", "blog_id", name="unique_user_blog"),
    # )


# Define a Role model for Flask-Security
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# Define a UserRoles model for Flask-Security
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id", ondelete="CASCADE"))


# Define a Token model for Flask-JWT-Extended
class Token(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

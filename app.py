from flask import Flask
from flask_restful import Api
from flask_security import Security, SQLAlchemyUserDatastore

from application.api import (
    BlogsAPI,
    CurrentUserAPI,
    ExportCSVAPI,
    FollowAPI,
    SearchAPI,
    UnfollowAPI,
)
from application.config import LocalDevelopmentConfig
from application.models import Role, User, db
from application.workers import ContextTask, celery

app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)
# Define the Flask-Security data store
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Initialize Flask-Security and Flask-JWT-Extended
security = Security(app=app, datastore=user_datastore)

db.init_app(app)
api = Api(app)
app.app_context().push()
celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
)
celery.Task = ContextTask

from application.controllers import *

# adding the API resources
api.add_resource(
    SearchAPI,
    "/api/search",
)
api.add_resource(
    FollowAPI,
    "/api/users/<int:user_id>/follow",
)
api.add_resource(
    UnfollowAPI,
    "/api/users/<int:user_id>/unfollow",
)
api.add_resource(
    CurrentUserAPI,
    "/api/current-user",
)
api.add_resource(
    BlogsAPI,
    "/api/blogs",
    "/api/blogs/<int:blog_id>/delete",
    "/api/blogs/<int:blog_id>/put",
)
api.add_resource(ExportCSVAPI, "/api/export-csv")

# Run the flask app
if __name__ == "__main__":
    # with app.app_context():
    #     db.drop_all()  # to reset all the tables in the database
    #     db.create_all()
    app.run(host="0.0.0.0", debug=True, port=8080)


# TODO: add href to user profile

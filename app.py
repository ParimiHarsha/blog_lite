import os

from flask import Flask, flash, redirect, render_template, url_for
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
# jwt = JWTManager()
# login_manager = LoginManager()
# login_manager.init_app(app)  # Initialize Flask-Login
# login_manager.login_view = "login"
db.init_app(app)
app.app_context().push()

# helper functions
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


@app.route("/")
def index():
    """Contrller for the landing page"""
    return render_template("index.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Login Controller"""

#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash("Invalid email or password")
#             return redirect(url_for("login"))
#         login_user(user, remember=form.remember_me.data)
#         return redirect(url_for("feed"))
#     return render_template("login.html", title="Log in", form=form)


# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     """Signup Controller"""

#     form = SignupForm()
#     if form.validate_on_submit():
#         # Check if the username already exists in the database
#         existing_user = User.query.filter_by(username=form.username.data).first()
#         if existing_user:
#             flash("Username is already taken. Please choose a different username.")
#             return redirect(url_for("signup"))

#         # User name is unique
#         user = User(
#             username=form.username.data,
#             email=form.email.data,
#             password=form.password.data,
#         )
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash("Congratulations, you are now a registered user!")
#         return redirect(url_for("login"))
#     return render_template("signup.html", title="Sign Up", form=form)


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


if __name__ == "__main__":
    # with app.app_context():
    # db.create_all()
    # db.drop_all()  # to reset all the tables in the database
    app.run(host="0.0.0.0", debug=True, port=8080)


# This is the search functionality for the application
# @app.route("/search")
# def search_users():
#     search_query = request.args.get("q")
#     with app.app_context():
#         users = User.query.filter(User.name.ilike(f"%{search_query}%")).all()
#         return render_template("search_results.html", users=users)


# @app.route("/user_dashboard/<client_name>", methods=["GET", "POST"])
# def user_dashboard(client_name):
#     if request.method == "GET":
#         # Get the list of trackers here and display them on the page
#         tracers = list()
#         print(client_name)
#         Cclient = client.query.filter(client.client_name == client_name).first()
#         rel_records = record.query.filter(record.client_id == Cclient.client_id).all()
#         # print(rel_records)
#         for r in rel_records:
#             tracer_name = (
#                 tracer.query.filter(tracer.tracer_id == r.tracer_id).first().tracer_name
#             )
#             tracers.append(tracer_name)

#         return render_template(
#             "user_dashboard.html", tracers=list(set(tracers)), client_name=client_name
#         )

#     # if request.method == 'POST':


# @app.route("/<tracer_name>/<client_name>", methods=["GET", "POST"])
# def tracer_dashboard(tracer_name, client_name):
#     # Get the tracer record of a given client and display them here
#     # Give the options of editing or deleting the records
#     # If possible show the graph(trendline) of the record for numerical
#     if request.method == "GET":
#         # records = list()
#         Cclient = client.query.filter(client.client_name == client_name).first()
#         Ctracer = tracer.query.filter(tracer.tracer_name == tracer_name).first()

#         rel_records = record.query.filter(
#             record.client_id == Cclient.client_id, record.tracer_id == Ctracer.tracer_id
#         ).all()
#         # for r in records:

#         return render_template(
#             "tracer_dashboard.html",
#             rel_records=rel_records,
#             tracer_name=tracer_name,
#             client_name=client_name,
#         )

#     # if request.method == 'POST':
#     #     pass

#     # return render_template('tracer_dashboard.html')


# @app.route("/<tracer_name>/<client_name>/add_record", methods=["GET", "POST"])
# def add_record(tracer_name, client_name):
#     """adds the record to the database with the tracer name, type , value and notes
#     then go back to the dashboard"""

#     if request.method == "GET":
#         # Here just display the form for giving a new entry for the data
#         return render_template(
#             "add_record.html", tracer_name=tracer_name, client_name=client_name
#         )
#     if request.method == "POST":
#         # Here make a new record in the datbase by giving all the values from above
#         # as arguments
#         record_value = request.form.get("record_value")
#         record_notes = request.form.get("record_notes")
#         record_date = request.form.get("record_date")

#         Nrecord = record(
#             tracer_id=tracer.query.filter(tracer.tracer_name == tracer_name)
#             .first()
#             .tracer_id,
#             client_id=client.query.filter(client.client_name == client_name)
#             .first()
#             .client_id,
#             value=record_value,
#             notes=record_notes,
#             date=record_date,
#         )
#         db.session.add(Nrecord)
#         db.session.commit()
#         # print(tracer.query.filter(tracer_name == tracer_name).first().tracer_name)
#         return redirect("/" + tracer_name + "/" + client_name)
#         # Need to work on the date module so that it picks the date automatically prefilling the field
#         # Nrecord = record(date = date, value = tracer_value, notes = tracer_notes,  )


# @app.route("/add_tracer/<client_name>", methods=["GET", "POST"])
# def add_tracer(client_name):
#     if request.method == "GET":

#         # Display the tracer adding html here and ask the user the fill the form
#         return render_template("add_tracer.html", client_name=client_name)
#     if request.method == "POST":
#         # post the form to this url and go back to the dashboard page
#         tracer_name = request.form.get("tracer_name")
#         tracer_desc = request.form.get("tracer_desc")
#         Ntracer = tracer(tracer_name=tracer_name, tracer_desc=tracer_desc)
#         db.session.add(Ntracer)
#         db.session.commit()
#         return redirect("/" + tracer_name + "/" + client_name)


# @app.route("/<tracer_name>/<client_name>/delete_tracer", methods=["GET", "POST"])
# def delete_tracer(tracer_name, client_name):
#     """Deletes the specified tracker form the database"""
#     # delete the tracer from the the  database
#     # record.delete().where(record.tracer_id == tracer_id)
#     tracer_id = tracer.query.filter(tracer.tracer_name == tracer_name).first().tracer_id
#     print(tracer_id)
#     record.query.filter(record.tracer_id == tracer_id).delete()
#     # tracer.query.filter(tracer.tracer_name == tracer_name).delete()
#     db.session.commit()

#     return redirect("/user_dashboard/" + client_name)


# @app.route("/<tracer_name>/<client_name>/<record_id>/delete", methods=["GET", "POST"])
# def delete_record(tracer_name, client_name, record_id):
#     """Deletes the specified record from the database"""
#     record.query.filter(record.record_id == record_id).delete()
#     db.session.commit()
#     return redirect("/" + tracer_name + "/" + client_name)


# @app.route("/<tracer_name>/<client_name>/<record_id>/edit", methods=["GET", "POST"])
# def edit_record(tracer_name, client_name, record_id):
#     """Edits the specified record in the database"""
#     if request.method == "GET":
#         return render_template(
#             "edit_record.html",
#             tracer_name=tracer_name,
#             client_name=client_name,
#             record_id=record_id,
#         )

#     if request.method == "POST":
#         rel_record = record.query.filter(record.record_id == record_id).first()
#         rel_record.value = request.form.get("record_value")
#         rel_record.notes = request.form.get("record_notes")
#         rel_record.date = request.form.get("record_date")
#         db.session.commit()
#         return redirect("/" + tracer_name + "/" + client_name)


# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # run the flask app
# app.run(host="0.0.0.0", debug=True, port=8080)

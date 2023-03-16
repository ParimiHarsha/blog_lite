import datetime as dt
import os

from flask import Flask, redirect, render_template, request

# from dateutil import parser
from flask_security import (
    RoleMixin,
    Security,
    SQLAlchemyUserDatastore,
    UserMixin,
    auth_token_required,
    current_user,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete

# from models import Role, User

current_dir = os.path.abspath(
    os.path.dirname(__file__)
)  # Used to get the path for the database

# Initializing Flask, Flask-Security
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config["SECURITY_PASSWORD_SALT"] = "password_salt"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    current_dir, "blog-store.sqlite3"
)

# Initialize the database
db = SQLAlchemy(app)
# db.init_app(app)

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )


app.app_context().push()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# class client(database.Model):
#     __tablename__ = "client"
#     client_id = database.Column(database.Integer, autoincrement=True, primary_key=True)
#     client_name = database.Column(database.String, nullable=False, unique=True)
#     passcode = database.Column(database.String, nullable=False)


# class record(database.Model):
#     __tablename__ = "record"
#     record_id = database.Column(
#         database.Integer, nullable=False, autoincrement=True, primary_key=True
#     )
#     tracer_id = database.Column(database.Integer, nullable=False)
#     client_id = database.Column(database.Integer, primary_key=True)
#     date = database.Column(database.String, nullable=False)
#     value = database.Column(database.String, nullable=False)
#     notes = database.Column(database.String, nullable=True)


# class tracer(database.Model):
#     __tablename__ = "tracer"
#     tracer_id = database.Column(database.Integer, autoincrement=True, primary_key=True)
#     tracer_name = database.Column(database.String, nullable=False, unique=True)
#     # tracer_type = database.Column(database.String, nullable = False)
#     tracer_desc = database.Column(database.String, nullable=True)


@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():  # done
    if request.method == "GET":
        return render_template("signin.html")
    if request.method == "POST":
        client_name = request.form.get("client_name")
        passcode = request.form.get("client_passcode")
        signed_client = client.query.filter(
            client.client_name == client_name, client.passcode == passcode
        ).first()
        print(signed_client)
        if signed_client != None:
            return redirect("/user_dashboard/" + client_name)
        else:
            return render_template("please_signup.html")


# Use this code block to debug the app
app.run(host="0.0.0.0", debug=True, port=8080)
breakpoint()


@app.route("/enroll", methods=["GET", "POST"])
def enroll():  # done
    if request.method == "GET":
        return render_template("enroll.html")
    if request.method == "POST":
        client_name = request.form.get("client_name")
        client_passcode = request.form.get("client_passcode")
        Nclient = client(client_name=client_name, passcode=client_passcode)
        db.session.add(Nclient)
        db.session.commit()
        return redirect("/user_dashboard/" + client_name)


@app.route("/user_dashboard/<client_name>", methods=["GET", "POST"])
def user_dashboard(client_name):
    if request.method == "GET":
        # Get the list of trackers here and display them on the page
        tracers = list()
        print(client_name)
        Cclient = client.query.filter(client.client_name == client_name).first()
        rel_records = record.query.filter(record.client_id == Cclient.client_id).all()
        # print(rel_records)
        for r in rel_records:
            tracer_name = (
                tracer.query.filter(tracer.tracer_id == r.tracer_id).first().tracer_name
            )
            tracers.append(tracer_name)

        return render_template(
            "user_dashboard.html", tracers=list(set(tracers)), client_name=client_name
        )

    # if request.method == 'POST':


@app.route("/<tracer_name>/<client_name>", methods=["GET", "POST"])
def tracer_dashboard(tracer_name, client_name):
    # Get the tracer record of a given client and display them here
    # Give the options of editing or deleting the records
    # If possible show the graph(trendline) of the record for numerical
    if request.method == "GET":
        # records = list()
        Cclient = client.query.filter(client.client_name == client_name).first()
        Ctracer = tracer.query.filter(tracer.tracer_name == tracer_name).first()

        rel_records = record.query.filter(
            record.client_id == Cclient.client_id, record.tracer_id == Ctracer.tracer_id
        ).all()
        # for r in records:

        return render_template(
            "tracer_dashboard.html",
            rel_records=rel_records,
            tracer_name=tracer_name,
            client_name=client_name,
        )

    # if request.method == 'POST':
    #     pass

    # return render_template('tracer_dashboard.html')


@app.route("/<tracer_name>/<client_name>/add_record", methods=["GET", "POST"])
def add_record(tracer_name, client_name):
    """adds the record to the database with the tracer name, type , value and notes
    then go back to the dashboard"""

    if request.method == "GET":
        # Here just display the form for giving a new entry for the data
        return render_template(
            "add_record.html", tracer_name=tracer_name, client_name=client_name
        )
    if request.method == "POST":
        # Here make a new record in the datbase by giving all the values from above
        # as arguments
        record_value = request.form.get("record_value")
        record_notes = request.form.get("record_notes")
        record_date = request.form.get("record_date")

        Nrecord = record(
            tracer_id=tracer.query.filter(tracer.tracer_name == tracer_name)
            .first()
            .tracer_id,
            client_id=client.query.filter(client.client_name == client_name)
            .first()
            .client_id,
            value=record_value,
            notes=record_notes,
            date=record_date,
        )
        db.session.add(Nrecord)
        db.session.commit()
        # print(tracer.query.filter(tracer_name == tracer_name).first().tracer_name)
        return redirect("/" + tracer_name + "/" + client_name)
        # Need to work on the date module so that it picks the date automatically prefilling the field
        # Nrecord = record(date = date, value = tracer_value, notes = tracer_notes,  )


@app.route("/add_tracer/<client_name>", methods=["GET", "POST"])
def add_tracer(client_name):
    if request.method == "GET":

        # Display the tracer adding html here and ask the user the fill the form
        return render_template("add_tracer.html", client_name=client_name)
    if request.method == "POST":
        # post the form to this url and go back to the dashboard page
        tracer_name = request.form.get("tracer_name")
        tracer_desc = request.form.get("tracer_desc")
        Ntracer = tracer(tracer_name=tracer_name, tracer_desc=tracer_desc)
        db.session.add(Ntracer)
        db.session.commit()
        return redirect("/" + tracer_name + "/" + client_name)


@app.route("/<tracer_name>/<client_name>/delete_tracer", methods=["GET", "POST"])
def delete_tracer(tracer_name, client_name):
    """Deletes the specified tracker form the database"""
    # delete the tracer from the the  database
    # record.delete().where(record.tracer_id == tracer_id)
    tracer_id = tracer.query.filter(tracer.tracer_name == tracer_name).first().tracer_id
    print(tracer_id)
    record.query.filter(record.tracer_id == tracer_id).delete()
    # tracer.query.filter(tracer.tracer_name == tracer_name).delete()
    db.session.commit()

    return redirect("/user_dashboard/" + client_name)


@app.route("/<tracer_name>/<client_name>/<record_id>/delete", methods=["GET", "POST"])
def delete_record(tracer_name, client_name, record_id):
    """Deletes the specified record from the database"""
    record.query.filter(record.record_id == record_id).delete()
    db.session.commit()
    return redirect("/" + tracer_name + "/" + client_name)


@app.route("/<tracer_name>/<client_name>/<record_id>/edit", methods=["GET", "POST"])
def edit_record(tracer_name, client_name, record_id):
    """Edits the specified record in the database"""
    if request.method == "GET":
        return render_template(
            "edit_record.html",
            tracer_name=tracer_name,
            client_name=client_name,
            record_id=record_id,
        )

    if request.method == "POST":
        rel_record = record.query.filter(record.record_id == record_id).first()
        rel_record.value = request.form.get("record_value")
        rel_record.notes = request.form.get("record_notes")
        rel_record.date = request.form.get("record_date")
        db.session.commit()
        return redirect("/" + tracer_name + "/" + client_name)


# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# run the flask app
app.run(host="0.0.0.0", debug=True, port=8080)

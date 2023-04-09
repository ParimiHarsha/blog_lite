import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import requests
from celery.schedules import crontab
from flask import current_app
from sqlalchemy import extract

from application.models import Blog, User
from application.workers import celery

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "parimi@mailhog.com"
SENDER_PASSOWRD = ""


@celery.task()
def export_csv(file, dir):
    df = pd.DataFrame(file)
    print(df)
    print(dir)
    df.to_csv(dir)
    return True


@celery.task()
def daily_reminder():
    url = "https://chat.googleapis.com/v1/spaces/AAAA0O3AO0I/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=dk1X_ZDyN9tpWwMI36-o6A9eu4MwQo9-uWDnhLFRDHA%3D"
    now = datetime.utcnow()
    last_24_hours = now - timedelta(hours=24)
    with current_app.app_context():
        # get all users
        users = User.query.all()
        for user in users:
            msg = f"Hello {user.username},\n\nYou have not posted a blog in the last 24 hours. Please log in to your account and post a new blog.\n\nBest regards,\nThe Blog Team"
            latest_blogs = (
                Blog.query.filter_by(user_id=user.id)
                .filter(Blog.created_at >= last_24_hours)
                .all()
            )
            # check if user posted a blog in the last 24 hours
            if not latest_blogs:
                # user did not post a blog in the last 24 hours, send reminder
                requests.post(url, json={"text": msg})
    return True


@celery.task
def send_email():
    # Get the current month and year
    now = datetime.now()
    month = now.strftime("%B")
    year = now.strftime("%Y")

    # Count the number of users following and being followed by each user
    with current_app.app_context():
        users = User.query.all()
        for user in users:
            followers_count = len(user.followers.all())
            following_count = len(user.friends)
            blogs = Blog.query.filter(
                extract("month", Blog.created_at) == now.month
            ).all()
            blogs_count = len(blogs)

            # Create an HTML report for the user
            report = f"""
            <!DOCTYPE html>
            <html lang="en">

            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Monthly Engagement Report</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            </head>

            <body>
            <div class="container mt-4">
                <div class="jumbotron">
                <h1 class="display-4">Engagement Report for {user.username}</h1>
                <hr class="my-4">
                <p class="lead">Month: {month}</p>
                <p class="lead">Year: {year}</p>
                <p class="lead">Number of Followers: {followers_count}</p>
                <p class="lead">Number of Users Followed: {following_count}</p>
                <p class="lead">Number of Blogs Posted this month: {blogs_count}</p>
                </div>
            </div>
            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
                integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
                crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
                integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
                crossorigin="anonymous"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
                integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
                crossorigin="anonymous"></script>
            </body>

            </html>
            """
            msg = MIMEMultipart()
            msg["From"] = SENDER_ADDRESS
            msg["To"] = "harsha.parimi@example.com"
            msg["Subject"] = "Monthly Reminder"

            msg.attach(
                MIMEText(
                    report,
                    "html",
                )
            )
            s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
            s.login(SENDER_ADDRESS, SENDER_PASSOWRD)
            s.send_message(msg)
            s.quit()

    return True

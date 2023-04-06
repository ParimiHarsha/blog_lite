import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import requests
from celery.schedules import crontab
from jinja2 import Template
from models import Blog, User
from sqlalchemy import extract

from application.workers import celery

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "parimi@mailhog.com"
SENDER_PASSOWRD = ""


@celery.task
def monthly_engagement_report():
    # Code to generate the monthly engagement report
    # This could involve querying your database or other sources of data
    # and generating an HTML report
    report = generate_report()

    # Code to send the report as an email
    send_email(report)


# for monthly engagement report
@celery.on_after_finalize.connect

celery.conf.beat_schedule = {
    "monthly_engagement_report": {
        "task": "tasks.monthly_engagement_report",
        "schedule": crontab(day_of_month=1, hour=0),
    },
}

# @celery.on_after_finalize.connect
# def periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(hour=6, minute=19),
#         daily_reminder.s("There are some tasks left to be done."),
#     )

#     sender.add_periodic_task(crontab(day_of_month=1), send_email.s())


# @celery.task()
# def daily_reminder(msg):
#     if not all(x.Date_completed for x in Cards.query.all()):
#         url = "https://chat.googleapis.com/v1/spaces/AAAAqRfiqNA/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=0is9XR063ddfzdHyrGBXWVzTqJi3RAnTGohcAy1wSlA%3D"
#         response = requests.post(url, json={"text": msg})
#     return


@celery.task()
def export_csv(file, dir):
    df = pd.DataFrame(file)
    df.to_csv(dir)
    return


@celery.task()
def send_email():
    # Get the current month and year
    now = datetime.now()
    month = now.strftime("%B")
    year = now.strftime("%Y")
    curr_time = datetime.datetime.now()

    blogs = Blog.query.filter(
        extract("month", Blog.created_at) == curr_time.month
    ).all()
     # Count the number of users following and being followed by each user
    users = User.query.all()
    for user in users:
        followers_count = len(user.followers.all())
        following_count = len(user.followed.all())
        blogs_count = len(user.blogs.all())

        # Create an HTML report for the user
        report = f"""
        <h1>Engagement Report for {user.username}</h1>
        <p>Month: {month}</p>
        <p>Year: {year}</p>
        <p>Number of Followers: {followers_count}</p>
        <p>Number of Users Followed: {following_count}</p>
        <p>Number of Blogs Posted: {blogs_count}</p>
        """

        # Send the report as an email to the user
        # subject = f"Monthly Engagement Report for {month} {year}"
        # msg = Message(subject=subject, recipients=[user.email], html=report)
        # mail.send(msg)


    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = "sharan342.kumar@example.com"
    msg["Subject"] = "Monthly Reminder"

    # file = open("templates/monthly.html")
    # message = Template(file.read())

    # msg.attach(
    #     MIMEText(
    #         message.render(
    #             tasks_completed=tasks_completed, late=late, hours_spent=hours_spent
    #         ),
    #         "html",
    #     )
    # )
    msg.attach(report)
    s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSOWRD)
    s.send_message(msg)
    s.quit()

    return True




def monthly_engagement_report():
    # Get the current month and year
    now = datetime.now()
    month = now.strftime("%B")
    year = now.strftime("%Y")

    # Count the number of users following and being followed by each user
    users = User.query.all()
    for user in users:
        followers_count = len(user.followers.all())
        following_count = len(user.followed.all())
        blogs_count = len(user.blogs.all())

        # Create an HTML report for the user
        report = f"""
        <h1>Engagement Report for {user.username}</h1>
        <p>Month: {month}</p>
        <p>Year: {year}</p>
        <p>Number of Followers: {followers_count}</p>
        <p>Number of Users Followed: {following_count}</p>
        <p>Number of Blogs Posted: {blogs_count}</p>
        """

        # Send the report as an email to the user
        subject = f"Monthly Engagement Report for {month} {year}"
        msg = Message(subject=subject, recipients=[user.email], html=report)
        mail.send(msg)
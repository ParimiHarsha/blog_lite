## Data Base Design:
- Users table
    This table will store user information such as username, password, email, etc. 
    Additionally, you can include columns to store user metadata like profile picture and biography. 
    The primary key for this table would be the user ID.

- Friends table:
    This table will store the relationships between users, i.e., who is friends with whom. 
    It will have two columns that reference the user ID column from the Users table.

- Blogs table:
    This table will store all the blog posts in the application. 
    It will have columns to store the blog title, content, date created, date last modified, and the user ID of the author. 
    The primary key for this table would be the blog ID.

- User_blog table:
    This table will establish a many-to-many relationship between users and blogs, as each user can write multiple blogs, 
    and each blog can have multiple authors. It will have two columns, one for the user ID and one for the blog ID.

************************

## Project Organization:
* The project is organised using a typical Flask application structure. The controllers, also known as views, are located in the application/controllers.py file and are responsible for handling the incoming HTTP requests from clients. 
* The models are defined in application/models.py and represent the database tables and their relationships. The app/templates directory contains the Jinja2 templates that are used to render HTML pages. 
* The app/static directory contains static files such as CSS, JavaScript, and images. The config.py file contains configuration variables for the application, such as the redis caching url, auth tokens etc.

**************************

## Steps to run the application:
* Once you open the folder you will find the project files in it. To run the application we need to run the app.py file and then run it in the broswer to start the application.
* Then we can use the GUI to navigate around the application and perform all sorts of CRUD operations on it. To verify whether the app is running well we can see the data being stored in the sqlite database which can be run using the DB Browser for SQlite.
* Upload the unzipped files in a Directory and execute the app.py file.

**************************

## Running the Backend Jobs:
* Starting the celery workers -  `celery -A app.celery worker --loglevel=DEBUG`
* Starting the scheduled jobs - `celery -A app.celery beat --max-interval 1 -l info`
* Running a celery task manually - `celery -A app.celery call application.tasks.send_email`


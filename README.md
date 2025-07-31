# Flask Blog-Platform — Local Setup & Developer Guide

Welcome! This README walks you from a clean machine to a fully-running copy of the project, then explains the data-model, layout, and background jobs. Follow the steps in order and you should be live in minutes.

---

## 1. Prerequisites

| Tool                  | Purpose                        | Quick install                                                                                        |
| --------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------- |
| **Python ≥ 3.9**      | Run the Flask/Celery code      | `brew install python` · `choco install python`                                                       |
| **Redis**             | Celery broker & result backend | `brew install redis && brew services start redis`<br>or Docker: `docker run -d -p 6379:6379 redis:6` |
| *(Optional)* **Make** | One-liner workflow scripts     | `brew install make` / use WSL on Windows                                                             |

---

## 2. Project Setup

```bash
# grab the code
git clone https://github.com/ParimiHarsha/blog_lite.git
cd blog_lite

# create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# install Python dependencies
pip install -r requirements.txt
```

> **Config defaults**
> *SQLAlchemy* points at `blog-store.sqlite3` in the repo root, and Celery looks for Redis on `redis://localhost:6379/0`.

---

## 3. First-time Database Initialisation

```bash
python - <<'PY'
from app import app, db
with app.app_context():
    db.create_all()
    print("✔️  SQLite schema created")
PY
```

(You only need this once, or whenever you wipe the database file.)

---

## 4. Running the Application

### 4.1  Web server

```bash
python app.py         # http://localhost:8080
```

### 4.2  Background workers

Open **two** additional terminals (activate the same `.venv`) and start:

```bash
# terminal 1 — task worker
celery -A app.celery worker --loglevel=info

# terminal 2 — scheduler / beat
celery -A app.celery beat --max-interval 1 --loglevel=info
```

You now have:

* **Flask** serving pages at `localhost:8080`
* A **Celery worker** executing queued tasks
* A **Celery beat** scheduler firing periodic jobs

### 4.3  (Optional) One-liners with Make

Create a tiny *Makefile*:

```makefile
run:        ## start Flask app
	python app.py

worker:     ## start Celery worker
	celery -A app.celery worker -l info

beat:       ## start Celery beat
	celery -A app.celery beat --max-interval 1 -l info
```

Then simply run `make run`, `make worker`, `make beat`.

---

## 5. Verifying Everything Works

1. Browse to **[http://localhost:8080](http://localhost:8080)**
   Sign up, create a blog post, follow/unfollow a user, etc.
2. Watch the Celery terminals for log messages when tasks (daily reminders, email reports) fire.
3. Open `blog-store.sqlite3` in *DB Browser for SQLite* to inspect data.

---

## 6. Database Design

| Table          | Key columns & notes                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------------------- |
| **users**      | `id` (PK), `username`, `password`, `email`, plus profile fields (bio, avatar, …).                    |
| **friends**    | `follower_id`, `followed_id` — both FKs to `users.id`; records follow relationships.                 |
| **blogs**      | `id` (PK), `title`, `content`, `created_at`, `updated_at`, `author_id` (FK → `users.id`).            |
| **user\_blog** | Junction table for many-to-many “co-author” support: `user_id` + `blog_id` (both composite PK / FK). |

- `Users`:
    This table will store user information such as username, password, email, etc. Additionally, you can include columns to store user metadata like profile picture and biography. The primary key for this table would be the user ID.

- `Friends`:
    This table will store the relationships between users, i.e., who is friends with whom. It will have two columns that reference the user ID column from the Users table.

- `Blogs`:
    This table will store all the blog posts in the application. It will have columns to store the blog title, content, date created, date last modified, and the user ID of the author. The primary key for this table would be the blog ID.

- `User_blog`:
    This table will establish a many-to-many relationship between users and blogs, as each user can write multiple blogs, and each blog can have multiple authors. It will have two columns, one for the user ID and one for the blog ID.


---

## 7. Running / Managing Background Jobs

| Action                     | Command                                                  |
| -------------------------- | -------------------------------------------------------- |
| **Start worker**           | `celery -A app.celery worker --loglevel=info`            |
| **Start scheduler (beat)** | `celery -A app.celery beat --max-interval 1 -l info`     |
| **Run a task manually**    | `celery -A app.celery call application.tasks.send_email` |

---

## 8. Troubleshooting

| Issue / Error                                | Fix                                                                        |
| -------------------------------------------- | -------------------------------------------------------------------------- |
| `redis.exceptions.ConnectionError`           | Start Redis (`brew services start redis` or Docker).                       |
| `OSError: [Errno 98] Address already in use` | Another app on port 8080 → export `PORT=5000` and edit `app.py` if needed. |
| `ModuleNotFoundError` for project modules    | Ensure you’re at repo root *and* the virtual-env is active.                |

---


## 9. Data Base Design



## 10. Project Organization

* The project is organised using a typical Flask application structure. The controllers, also known as views, are located in the application/controllers.py file and are responsible for handling the incoming HTTP requests from clients. 
* The models are defined in application/models.py and represent the database tables and their relationships. The app/templates directory contains the Jinja2 templates that are used to render HTML pages. 
* The app/static directory contains static files such as CSS, JavaScript, and images. The config.py file contains configuration variables for the application, such as the redis caching url, auth tokens etc.


## Running the Backend Jobs

* Starting the celery workers -  `celery -A app.celery worker --loglevel=DEBUG`
* Starting the scheduled jobs - `celery -A app.celery beat --max-interval 1 -l info`
* Running a celery task manually - `celery -A app.celery call application.tasks.send_email`
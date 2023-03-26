import os

current_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base Configs for the appplication"""

    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"


class LocalDevelopmentConfig(Config):
    """Local Development Configs for the appplication"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        current_dir, "blog-store.sqlite3"
    )
    DEBUG = True
    SECRET_KEY = "0f178911124b519b"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "vcnkso3452vnui9k32"
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_USERNAME_ENABLE = True

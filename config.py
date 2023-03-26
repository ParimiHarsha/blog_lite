import os

current_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # can create a secret key on the fly using os.urandom(32)
    SECRET_KEY = "0f178911124b519b"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        current_dir, "blog-store.sqlite3"
    )
    SECURITY_PASSWORD_SALT = "my-secret-key"
    SECURITY_PASSWORD_HASH = "sha512_crypt"
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authorization"
    SECURITY_TOKEN_AUTHENTICATION_KEY = "access_token"
    SECURITY_PASSWORDLESS = False
    SECURITY_DEFAULT_REMEMBER_ME = False

from flask import Flask
from controllers import db, cache

def create_app():

    app = Flask(__name__)

    app.secret_key = "placement_portal_secret"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True

    app.config["MAIL_USERNAME"] = "s.specific1@gmail.com"
    app.config["MAIL_PASSWORD"] = "sbrr qtoz hkon slix"

    app.config["CACHE_TYPE"] = "RedisCache"

    app.config["CACHE_REDIS_HOST"] = "localhost"
    app.config["CACHE_REDIS_PORT"] = 6379
    app.config["CACHE_DEFAULT_TIMEOUT"] = 60

    db.init_app(app)
    cache.init_app(app)

    return app
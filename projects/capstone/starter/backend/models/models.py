from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from .config import Config

db = SQLAlchemy()


def setup_db(app):
    app.config.from_object(Config)
    try:
        db.app = app
        db.init_app(app)
        migrate = Migrate(app, db)
    except Exception as e:
        print(e)

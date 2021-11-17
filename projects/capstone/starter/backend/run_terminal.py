from models import *
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


def run_terminal():
    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    return db

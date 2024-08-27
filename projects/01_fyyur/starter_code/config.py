import os


SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

DB_PSWD = os.getenv('DB_PSWD')

# DONE IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:{}@localhost:5432/fyyur".format(
    DB_PSWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False

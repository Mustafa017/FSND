import os

os.environ['DB_NAME'] = 'enrollment'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PSWD'] = 'Galacticos'
os.environ['DB_HOST'] = 'localhost:5432'

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_pswd = os.getenv('DB_PSWD')
db_host = os.getenv('DB_HOST')


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgres://{db_user}:{db_pswd}@{db_host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

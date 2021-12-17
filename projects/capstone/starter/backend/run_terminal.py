from models import *
from app import create_app

db.__dict__
db.app.__dict__
db.app.config['TESTING']
db.app.config['ENV']
db.app.config['SQLALCHEMY_DATABASE_URI']
db.app.instance_path
db.app.app_context
db.app.test_client().__dict__
db.app.test_client().get('/students')

# ***********************************************
# flask db migrate
# flask db

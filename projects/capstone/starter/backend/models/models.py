# from FSND.projects.capstone.starter import config
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy
# from .config import Config


db = SQLAlchemy()


def setup_db(app):
    try:
        db.app = app
        db.init_app(app)
        migrate = Migrate(app, db)
    except Exception as e:
        print(e)


class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    se_crs_id = db.Column(db.Integer, db.ForeignKey('course.crs_id'),
                          primary_key=True)
    se_std_id = db.Column(db.Integer, db.ForeignKey('student.std_id'),
                          primary_key=True)
    se_date = db.Column(db.String(30), nullable=False)
    student = db.relationship('Student', backref=db.backref(
        'enrollments', cascade="all, delete-orphan", lazy=True))
    course = db.relationship('Course', backref=db.backref(
        'enrollments', cascade="all, delete-orphan", lazy=True))

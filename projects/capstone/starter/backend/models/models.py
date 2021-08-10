# from FSND.projects.capstone.starter import config
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy


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
    se_semester = db.Column(db.String(30), primary_key=True)
    course = db.relationship('Course', backref='enrollments', lazy=True)

    def __init__(self, semester):
        self.se_semester = semester

    def __repr__(self) -> str:
        return "Course ID {} Student ID {} Semester {}".format(
            self.se_crs_id, self.se_std_id, self.se_semester)

from .models import db


class Lecturer(db.Model):
    __tablename__ = 'lecturer'
    lec_id = db.Column(db.Integer, primary_key=True)
    lec_title = db.Column(db.Integer, nullable=False)
    lec_fname = db.Column(db.String(20), nullable=False)
    lec_lname = db.Column(db.String(20), nullable=False)
    lec_email = db.Column(db.String(30), unique=True, nullable=False)
    lec_dob = db.Column(db.String(10), nullable=False)
    lec_gender = db.Column(db.String(10), nullable=False)
    lec_crs_id = db.Column(db.Integer, db.ForeignKey(
        'course.crs_id'), nullable=False)
    courses = db.relationship('Course', backref='lecturer', lazy=True)

    def __init__(self, title, fname, lname, email, dob, gender) -> None:
        self.lec_title = title
        self.lec_fname = fname
        self.lec_lname = lname
        self.lec_email = email
        self.lec_dob = dob
        self.lec_gender = gender

    def __repr__(self) -> str:
        return f'id:{self.lec_id}, title:{self.lec_title}, \
            first name:{self.lec_fname}, Last name:{self.lec_lname}'

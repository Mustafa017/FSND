from .models import db, Enrollments


class Course(db.Model):
    __tablename__ = 'course'
    crs_id = db.Column(db.Integer, primary_key=True)
    crs_code = db.Column(db.String(20), unique=True, nullable=False)
    crs_title = db.Column(db.String(50), unique=True, nullable=False)
    crs_desc = db.Column(db.Text, nullable=False)
    crs_book = db.Column(db.String(255))
    crs_lec_id = db.Column(db.Integer, db.ForeignKey(
        'lecturer.lec_id'), nullable=False)
    crs_cls_id = db.Column(db.Integer, db.ForeignKey(
        'classroom.cls_id'), nullable=False)

    def __init__(self, code, title, desc, book, lec, room) -> None:
        self.crs_code = code
        self.crs_title = title
        self.crs_desc = desc
        self.crs_book = book
        self.crs_lec_id = lec
        self.crs_cls_id = room

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f'<Course:{self.crs_id} {self.crs_title}>'

    @property
    def format(self):
        return{
            "course_id": self.crs_id,
            "course_code": self.crs_code,
            "course_title": self.crs_title,
            "course_desc": self.crs_desc,
            "course_book": self.crs_book
        }

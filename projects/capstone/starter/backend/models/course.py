from .models import db, Enrollments


class Course(db.Model):
    __tablename__ = 'course'
    crs_id = db.Column(db.Integer, primary_key=True)
    crs_code = db.Column(db.String(20), unique=True, nullable=False)
    crs_title = db.Column(db.String(50), unique=True, nullable=False)
    crs_desc = db.Column(db.Text, nullable=False)
    crs_book = db.Column(db.String(255))

    def __init__(self, code, title, desc, book) -> None:
        self.crs_code = code
        self.crs_title = title
        self.crs_desc = desc
        self.crs_book = book

    def __repr__(self) -> str:
        return f'id:{self.crs_id}, code:{self.crs_code}, \
            title:{self.crs_title}'

from .models import db


class Classroom(db.Model):
    __tablename__ = 'classroom'
    cls_id = db.Column(db.Integer, primary_key=True)
    cls_code = db.Column(db.String(20), unique=True, nullable=False)
    cls_size = db.Column(db.String(50), unique=True, nullable=False)
    courses = db.relationship('Course', backref='classroom', lazy=True)

    def __init__(self, code, size) -> None:
        self.cls_code = code
        self.cls_size = size

    def __repr__(self) -> str:
        return f'id:{self.cls_id}, code:{self.cls_code}'

from .models import db, Enrollments


class Student(db.Model):
    __tablename__ = 'student'
    std_id = db.Column(db.Integer, primary_key=True)
    std_regno = db.Column(db.Integer, unique=True, nullable=False)
    std_fname = db.Column(db.String(20), nullable=False)
    std_lname = db.Column(db.String(20), nullable=False)
    std_email = db.Column(db.String(30), unique=True, nullable=False)
    std_dob = db.Column(db.String(10), nullable=False)
    std_gender = db.Column(db.String(10), nullable=False)
    enrollments = db.relationship('Enrollments', backref=db.backref(
        'students', lazy=True))

    def __init__(self, regno, fname, lname, email, dob, gender) -> None:
        self.std_regno = regno
        self.std_fname = fname
        self.std_lname = lname
        self.std_email = email
        self.std_dob = dob
        self.std_gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def format(self):
        return {
            "student_id": self.std_id,
            "student_regno": self.std_regno,
            "student_first_name": self.std_fname,
            "student_last_name": self.std_lname,
            "student_email": self.std_email,
            "student_dob": self.std_dob,
            "student_sex": self.std_gender
        }

    def __repr__(self) -> str:
        return f'<student: {self.std_id} {self.std_lname}>'

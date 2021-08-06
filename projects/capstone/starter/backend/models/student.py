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

    def __init__(self, regno, fname, lname, email, dob, gender) -> None:
        self.std_regno = regno
        self.std_fname = fname
        self.std_lname = lname
        self.std_email = email
        self.std_dob = dob
        self.std_gender = gender

    def __repr__(self) -> str:
        return f'id:{self.std_id}, Reg_no:{self.std_regno}, \
            first name:{self.std_fname}, Last_name:{self.std_lname}'

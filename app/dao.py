import hashlib
from models import Student, Health
from app import db


def get_all_students():
    return Student.query.all()


def add_student(name, dob, gender, parent_name, phone):
    new_student = Student(
        name=name,
        dob=dob,
        gender=gender,
        parent_name=parent_name,
        phone=phone
    )

    db.session.add(new_student)
    db.session.commit()

def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()

def add_health_record(name, dob, gender, parent_name, phone):
    new_health_record = Health()
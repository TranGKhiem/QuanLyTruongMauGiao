import hashlib
from models import Student
# Import db từ file cấu hình gốc (thay 'tên_file_init_của_bạn' bằng tên file chứa biến app và db, ví dụ main, init...)
from app import db


def get_all_students():
    return Student.query.all()


def add_student(name, dob, gender, parent_name):
    new_student = Student(
        name=name,
        dob=dob,
        gender=gender,
        parent_name=parent_name
    )

    db.session.add(new_student)
    db.session.commit()

def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
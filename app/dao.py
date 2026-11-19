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

def add_health_record(student_id, record_date, weight, temperatures):
    for s_id, w, t in zip(student_id,weight,temperatures):
        if w.strip() and t.strip():
            weight_val = float(w)
            temperature_val = float(t)
            note_val = "Cảnh báo sốt" if temperature_val > 37.5 else "Bình thường"

            record = Health(
                student_id=int(s_id),
                record_date=record_date,
                weight=weight_val,
                temperature=temperature_val,
                note=note_val
            )
            db.session.add(record)
    db.session.commit()
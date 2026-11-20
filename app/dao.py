import hashlib
from models import Student, Health, User, UserRole
from app import app,db


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

def add_user(name, username, password, role=UserRole.USER):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    u = User(name=name, username=username, password=password, role=role)
    db.session.add(u)
    db.session.commit()

def auth_user(username,password):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    return User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()

def get_user_by_id(id):
    return User.query.get(id)

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


if __name__ == "__main__":
    with app.app_context():
        # Test tạo user
        # add_user(name="Quản Trị Viên", username="admin", password="123", role=UserRole.ADMIN)
        # add_user(name="Nguyễn Văn A", username="NVA", password="456", role=UserRole.USER)

        print("Tạo Thành Công")
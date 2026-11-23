import hashlib
from models import Student, Health, User, UserRole, Classroom, Rules
from app import app, db


def get_all_students(current_user):
    if current_user.role == UserRole.ADMIN:
        return Student.query.all()
    return Student.query.filter(Student.user_id == current_user.id).all()

def get_max_students():
    reg = Rules.query.first()
    return reg.max_students if reg else 25

def count_students_by_user(user_id):
    return Student.query.filter(Student.user_id == user_id).count()

def add_student(name, dob, gender, parent_name, phone, user_id, classroom_id=None):
    new_student = Student(
        name=name,
        dob=dob,
        gender=gender,
        parent_name=parent_name,
        phone=phone,
        user_id=user_id,
        classroom_id=classroom_id
    )

    db.session.add(new_student)
    db.session.commit()


def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()


def add_classroom(name):
    c = Classroom(name=name)
    db.session.add(c)
    db.session.commit()
    return c


def add_user(name, username, password, role=UserRole.USER, classroom_id=None):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    u = User(name=name, username=username, password=password, role=role, classroom_id=classroom_id)
    db.session.add(u)
    db.session.commit()


def auth_user(username, password):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    return User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()


def get_user_by_id(id):
    return User.query.get(id)


def add_health_record(student_id, record_date, weight, temperatures):
    for s_id, w, t in zip(student_id, weight, temperatures):
        if w.strip() and t.strip():
            weight_val = float(w)
            temperature_val = float(t)
            note_val = "Cảnh báo sốt" if temperature_val > 37.5 else "Bình thường"

            existing_record = Health.query.filter(
                Health.student_id == int(s_id),
                Health.record_date == record_date
            ).first()

            if existing_record:
                existing_record.weight = weight_val
                existing_record.temperature = temperature_val
                existing_record.note = note_val
            else:
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

        # c1 = add_classroom(name="Mầm 1")
        # c2 = add_classroom(name="Chồi 1")

        # add_user(name="Cô Lan", username="gv1", password="123", role=UserRole.USER, classroom_id=c1.id)
        # add_user(name="Cô Mai", username="gv2", password="123", role=UserRole.USER, classroom_id=c2.id)
        print("Tạo Thành Công")

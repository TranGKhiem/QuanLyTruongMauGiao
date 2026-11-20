from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from app import app, db
from enum import Enum as RoleEnum
from flask_login import UserMixin


# Data login
class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)

    def __str__(self):
        return self.name

# Data danh sách lớp
class Student(db.Model):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    dob = Column(String(20), nullable=False)  # yyyy-MM-dd
    gender = Column(String(10), nullable=False)
    parent_name = Column(String(50), nullable=False)
    phone=Column(String(20), nullable=False)

    health_records = relationship('Health', backref='student', lazy=True)
    def __str__(self):
        return self.name

#Data sức khỏe
class Health(db.Model):
    __tablename__ = 'health'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    record_date=Column(String(20), nullable=False) # yyyy-MM-dd
    weight = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    note=Column(String(50), default='Bình Thường')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Đã tạo bảng")
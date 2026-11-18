from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app import app, db


class Student(db.Model):
    __tablename__ = 'student'  # Đặt tên bảng trong MySQL

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    dob = Column(String(20), nullable=False)  # yyyy-MM-dd
    gender = Column(String(10), nullable=False)
    parent_name = Column(String(50), nullable=False)
    phone=Column(String(20), nullable=False)

    def __str__(self):
        return self.name

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
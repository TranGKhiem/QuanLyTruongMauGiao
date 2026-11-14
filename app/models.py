from sqlalchemy import Column, Integer, String

from app import app, db


class Student(db.Model):
    __tablename__ = 'student'  # Đặt tên bảng trong MySQL

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    dob = Column(String(20), nullable=False)  # DD/MM/YYYY
    gender = Column(String(10), nullable=False)
    parent_name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Đã tạo bảng")
from flask import render_template, request, redirect
import dao
from app import app

@app.route("/")
def index():
    students_list = dao.get_all_students()
    return render_template("index.html", students=students_list)


@app.route("/add-student", methods=['POST'])
def add_student_route():
    # Rút trích dữ liệu người dùng nhập từ Form HTML (thông qua thuộc tính 'name' của thẻ input)
    name = request.form.get('name')
    dob = request.form.get('dob')
    gender = request.form.get('gender')
    parent_name = request.form.get('parent_name')

    # Gọi hàm lưu vào database
    dao.add_student(name=name, dob=dob, gender=gender, parent_name=parent_name)

    # Lưu xong thì tải lại trang chủ để cập nhật bảng
    return redirect("/")


@app.route("/delete-student/<int:student_id>")
def delete_student_route(student_id):
    # Gọi hàm xóa từ dao.py, truyền ID vào
    dao.delete_student(student_id)

    # Xóa xong thì tải lại trang chủ
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
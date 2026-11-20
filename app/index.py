from flask import render_template, request, redirect
import dao
from app import app, login
from flask_login import login_user, logout_user, current_user


#============= Danh sách lớp ==================
@app.route("/")
def index():
    students_list = dao.get_all_students()
    return render_template("index.html", students=students_list)


@app.route("/add-student", methods=['POST'])
def add_student_route():
    name = request.form.get('name')
    dob = request.form.get('dob')
    gender = request.form.get('gender')
    parent_name = request.form.get('parent_name')
    phone = request.form.get('phone')

    dao.add_student(name=name, dob=dob, gender=gender, parent_name=parent_name, phone=phone)

    return redirect("/")


@app.route("/delete-student/<int:student_id>")
def delete_student_route(student_id):
    dao.delete_student(student_id)
    return redirect("/")

#============= login ==================
@app.route("/login", methods=["GET","POST"])
def login_my_user():
    err_msg = None
    if request.method.__eq__("POST"):
        user = request.form.get("username")
        password = request.form.get("password")

        u = dao.auth_user(username=user, password=password)

        if u:
            login_user(u)
            return redirect("/")
        else:
            err_msg = "Tài khoản hoặc mật khẩu chưa đúng!"

    return render_template("login.html", err_msg=err_msg)

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

#============= Logout ==================
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")  # Đăng xuất xong chuyển hướng về trang đăng nhập

#============= Sức khỏe ==================
@app.route("/health")
def health():
    students_list = dao.get_all_students()
    return render_template("health.html", students=students_list)


@app.route('/save-all-health', methods=['POST'])
def save_all_health():
    record_date = request.form.get('record_date')
    student_ids = request.form.getlist('student_id[]')
    weights = request.form.getlist('weight[]')
    temperatures = request.form.getlist('temperature[]')

    dao.add_health_record(student_ids, record_date, weights, temperatures)
    return redirect('/health')  # Chuyển hướng lại về trang sức khỏe

#============= Học phí ==================
@app.route("/fee")
def fee():
    return render_template("fee.html")

#============= Báo cáo - Thống kê ==================
@app.route("/statistics")
def statistics():
    return render_template("statistics.html")

#============= Cài đặt quy định ==================
@app.route("/setting")
def setting():
    return render_template("setting.html")

if __name__=="__main__":
    app.run(debug=True)
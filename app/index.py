from flask import render_template, request, redirect, flash
from flask_sqlalchemy import record_queries

import dao
from app import app, login
from flask_login import login_user, logout_user, current_user, login_required
from models import User, UserRole, Health, Rules
from datetime import datetime

login.login_view = 'login_my_user'

#============= Danh sách lớp ==================
@app.route("/")
@login_required
def index():
    if not current_user.is_authenticated:
        return render_template("index.html", students=[])

    students_list = dao.get_all_students(current_user)
    max_students = dao.get_max_students()
    current_count = len(students_list)

    students_list = dao.get_all_students(current_user)
    return render_template("index.html",
                           students=students_list,
                           max_students=max_students,
                           current_count=current_count)


@app.route("/add-student", methods=['POST'])
@login_required
def add_student_route():
    if current_user.role != UserRole.USER:
        return redirect("/")

    max_students = dao.get_max_students()
    current_count = dao.count_students_by_user(current_user.id)
    if current_count >= max_students:
        flash(f"Lớp đã đạt sĩ số tối đa ({max_students} học sinh), không thể thêm mới!", "danger")
        return redirect("/")

    name = request.form.get('name')
    dob = request.form.get('dob')
    gender = request.form.get('gender')
    parent_name = request.form.get('parent_name')
    phone = request.form.get('phone')

    dao.add_student(
        name=name,
        dob=dob,
        gender=gender,
        parent_name=parent_name,
        phone=phone,
        user_id=current_user.id,
        classroom_id=current_user.classroom_id
    )

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
    return redirect("/login")

#============= Sức khỏe ==================
@app.route("/health")
@login_required
def health():
    selected_date = request.args.get('date')
    students_list = dao.get_all_students(current_user)

    health_data = {}
    if selected_date:
        records = Health.query.filter(Health.record_date == selected_date).all()
        for r in records:
            health_data[r.student_id] = r

    return render_template("health.html",
                           students=students_list,
                           selected_date=selected_date,
                           health_data=health_data)


@app.route('/save-all-health', methods=['POST'])
@login_required
def save_all_health():
    if current_user.role != UserRole.USER:
        return redirect("/health")

    record_date = request.form.get('record_date')
    student_ids = request.form.getlist('student_id[]')
    weights = request.form.getlist('weight[]')
    temperatures = request.form.getlist('temperature[]')

    dao.add_health_record(student_ids, record_date, weights, temperatures)
    return redirect('/health')  # Chuyển hướng lại về trang sức khỏe

#============= Học phí ==================
@app.route("/fee")
@login_required
def fee():
    selected_month_year = request.args.get('month_year')

    if not selected_month_year:
        now = datetime.now()
        selected_month_year = now.strftime("%Y-%m")

    year, month = selected_month_year.split("-")

    fee_list = dao.get_fee_list(int(month), int(year), current_user)

    rule = Rules.query.first()
    tuition_fee = rule.tuition_fee if rule else 1500000
    meal_fee = rule.meal_fee if rule else 25000

    return render_template("fee.html",
                           fee_list=fee_list,
                           selected_month_year=selected_month_year,
                           tuition_fee=tuition_fee,
                           meal_fee=meal_fee)

#============= Báo cáo - Thống kê ==================
@app.route("/statistics")
@login_required
def statistics():
    return render_template("statistics.html")

#============= Cài đặt quy định ==================
@app.route("/setting")
@login_required
def setting():
    return render_template("setting.html")

if __name__=="__main__":
    app.run(debug=True)
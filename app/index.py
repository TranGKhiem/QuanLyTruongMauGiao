from flask import render_template, request, redirect
import dao
from app import app

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

@app.route("/health")
def health():
    return render_template("health.html")

if __name__=="__main__":
    app.run(debug=True)

# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin, current_user
from werkzeug.security import check_password_hash
from datetime import datetime



app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="IS668Gradebook",
    password="Databasepwd",
    hostname="IS668Gradebook.mysql.pythonanywhere-services.com",
    databasename="IS668Gradebook$project",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = "jxl40zl2mgh59c1mp3x6"
login_manager = LoginManager()
login_manager.init_app(app)

#################################################
#################### TABLES #####################

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(128))
    fname = db.Column(db.String(128))
    lname = db.Column(db.String(128))
    email = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

class Student(db.Model):

    __tablename__ = "students"

    StudentId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(4096))
    LastName = db.Column(db.String(4096))
    Major = db.Column(db.String(4096))
    Email = db.Column(db.String(4096))
    CreditsTaken = db.Column(db.Integer)
    ClassDesignation = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)

class Assignment(db.Model):

    __tablename__ = "assignments"

    AssignmentId = db.Column(db.Integer, primary_key=True)
    AssignmentName = db.Column(db.String(4096))
    ClassID = db.Column(db.Integer)
    ClassName = db.Column(db.String(4096))
    DateAssigned = db.Column(db.String(4096))
    DueDate = db.Column(db.String(4096))

class Gradebook(db.Model):

    __tablename__ = "gradebooks"

    ListId = db.Column(db.Integer, primary_key=True)
    AssignmentGrade = db.Column(db.String(4096))
    StudentId = db.Column(db.Integer, db.ForeignKey('students.StudentId'))
    AssignmentId = db.Column(db.Integer, db.ForeignKey('assignments.AssignmentId'))

class TestTable(db.Model):

    __tablename__ = "test_table"

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(128))
    lname = db.Column(db.String(128))
    email = db.Column(db.String(128))


#################################################
#################### ROUTES #####################

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        return render_template("main_page.html", gradebookcount=gradebookcount, studentcount=studentcount, assignmentcount = assignmentcount, students=Student.query.all(), users=User.query.all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

#################################################

@app.route("/Students", methods=["GET", "POST"])
def student():
    if request.method == "GET":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        return render_template("students.html", gradebookcount=gradebookcount, studentcount=studentcount, assignmentcount = assignmentcount, students=Student.query.order_by(Student.StudentId).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    student = Student(FirstName=request.form["fname"],LastName=request.form["lname"],Major=request.form["major"],Email=request.form["email"],CreditsTaken=request.form["creditstaken"],ClassDesignation=request.form["classdesignation"])
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('student'))

#################################################

@app.route("/StudentsSortFirst", methods=["GET", "POST"])
def studentsortfirst():
    if request.method == "GET":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        return render_template("students.html", gradebookcount=gradebookcount, studentcount=studentcount, assignmentcount = assignmentcount, students=Student.query.order_by(Student.FirstName.asc(),Student.LastName.asc()).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    student = Student(FirstName=request.form["fname"],LastName=request.form["lname"],Major=request.form["major"],Email=request.form["email"],CreditsTaken=request.form["creditstaken"],ClassDesignation=request.form["classdesignation"])
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('student'))

#################################################

@app.route("/StudentsSortLast", methods=["GET", "POST"])
def studentsortlast():
    if request.method == "GET":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        return render_template("students.html", gradebookcount=gradebookcount, studentcount=studentcount, assignmentcount = assignmentcount, students=Student.query.order_by(Student.LastName.asc(),Student.FirstName.asc()).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    student = Student(FirstName=request.form["fname"],LastName=request.form["lname"],Major=request.form["major"],Email=request.form["email"],CreditsTaken=request.form["creditstaken"],ClassDesignation=request.form["classdesignation"])
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('student'))

#################################################

@app.route("/StudentsSortMajor", methods=["GET", "POST"])
def studentsortmajor():
    if request.method == "GET":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        return render_template("students.html", gradebookcount=gradebookcount, studentcount=studentcount, assignmentcount = assignmentcount, students=Student.query.order_by(Student.Major.asc(),Student.FirstName.asc()).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    student = Student(FirstName=request.form["fname"],LastName=request.form["lname"],Major=request.form["major"],Email=request.form["email"],CreditsTaken=request.form["creditstaken"],ClassDesignation=request.form["classdesignation"])
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('student'))

#################################################

@app.route("/StudentsSortEmail", methods=["GET", "POST"])
def studentsortemail():
    if request.method == "GET":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        return render_template("students.html", gradebookcount=gradebookcount, studentcount=studentcount, assignmentcount = assignmentcount, students=Student.query.order_by(Student.Email.asc(),Student.FirstName.asc()).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    student = Student(FirstName=request.form["fname"],LastName=request.form["lname"],Major=request.form["major"],Email=request.form["email"],CreditsTaken=request.form["creditstaken"],ClassDesignation=request.form["classdesignation"])
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('student'))

#################################################

@app.route("/StudentsSortCredits", methods=["GET", "POST"])
def studentsortcredits():
    if request.method == "GET":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        return render_template("students.html", gradebookcount=gradebookcount, studentcount=studentcount, assignmentcount = assignmentcount, students=Student.query.order_by(Student.CreditsTaken.asc(),Student.FirstName.asc()).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    student = Student(FirstName=request.form["fname"],LastName=request.form["lname"],Major=request.form["major"],Email=request.form["email"],CreditsTaken=request.form["creditstaken"],ClassDesignation=request.form["classdesignation"])
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('student'))

#################################################

@app.route("/StudentsSortClass", methods=["GET", "POST"])
def studentsortclass():
    if request.method == "GET":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        return render_template("students.html", gradebookcount=gradebookcount, studentcount=studentcount, assignmentcount = assignmentcount, students=Student.query.order_by(Student.ClassDesignation.asc(),Student.FirstName.asc()).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    student = Student(FirstName=request.form["fname"],LastName=request.form["lname"],Major=request.form["major"],Email=request.form["email"],CreditsTaken=request.form["creditstaken"],ClassDesignation=request.form["classdesignation"])
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('student'))

#################################################

@app.route("/Assignments", methods=["GET", "POST"])
def assignment():
    if request.method == "GET":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        return render_template("assignments.html", gradebookcount=gradebookcount, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentId).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    assignment = Assignment(AssignmentName=request.form["assignmentname"],DateAssigned=request.form["assigneddate"],DueDate=request.form["duedate"])
    db.session.add(assignment)
    db.session.commit()

    assignmentcount = Assignment.query.count()
    studentcount = Student.query.count()
    assignment_skip = assignmentcount - 1
    last_assignment_id = Assignment.query.order_by(Assignment.AssignmentId).offset(assignment_skip).limit(1).first().AssignmentId
    for i in range(0,studentcount):
        get_student_id = Student.query.order_by(Student.StudentId).offset(i).limit(1).first().StudentId
        add_to_gradebook = Gradebook(AssignmentGrade="NA", StudentId= get_student_id, AssignmentId=last_assignment_id)
        db.session.add(add_to_gradebook)
        db.session.commit()

    return redirect(url_for('assignment'))

#################################################

@app.route("/AssignmentsSortName", methods=["GET", "POST"])
def assignmentsortname():
    if request.method == "GET":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        return render_template("assignments.html", gradebookcount=gradebookcount, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentName.asc(),Assignment.AssignmentId.asc()).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    assignment = Assignment(AssignmentName=request.form["assignmentname"],DateAssigned=request.form["assigneddate"],DueDate=request.form["duedate"])
    db.session.add(assignment)
    db.session.commit()

    assignmentcount = Assignment.query.count()
    studentcount = Student.query.count()
    assignment_skip = assignmentcount - 1
    last_assignment_id = Assignment.query.order_by(Assignment.AssignmentId).offset(assignment_skip).limit(1).first().AssignmentId
    for i in range(0,studentcount):
        get_student_id = Student.query.order_by(Student.StudentId).offset(i).limit(1).first().StudentId
        add_to_gradebook = Gradebook(AssignmentGrade="NA", StudentId= get_student_id, AssignmentId=last_assignment_id)
        db.session.add(add_to_gradebook)
        db.session.commit()

    return redirect(url_for('assignment'))

#################################################

@app.route("/Gradebook", methods=["GET", "POST"])
def gradebook():
    if request.method == "GET":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        student_grades = db.session.query(Assignment.AssignmentId, Assignment.AssignmentName, Student.FirstName, Student.LastName, Student.StudentId, Gradebook.AssignmentGrade).outerjoin(Gradebook, Assignment.AssignmentId == Gradebook.AssignmentId).outerjoin(Student, Student.StudentId == Gradebook.StudentId).order_by(Assignment.AssignmentId.asc(),Student.FirstName.asc()).all()
        return render_template("gradebook.html", gradebookcount=gradebookcount, student_grades=student_grades, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentId).order_by(Assignment.AssignmentName).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return redirect(url_for('gradebook'))

#################################################

@app.route("/GradebookSortAssignment", methods=["GET", "POST"])
def gradebooksortassignment():
    if request.method == "GET":
        # --- defaultload
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        # --- defaultload
        student_grades = db.session.query(Assignment.AssignmentId, Assignment.AssignmentName, Student.FirstName, Student.LastName, Student.StudentId, Gradebook.AssignmentGrade).outerjoin(Gradebook, Assignment.AssignmentId == Gradebook.AssignmentId).outerjoin(Student, Student.StudentId == Gradebook.StudentId).order_by(Assignment.AssignmentName.asc(),Student.FirstName.asc()).all()
        return render_template("gradebook.html", gradebookcount=gradebookcount, student_grades=student_grades, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentId).order_by(Assignment.AssignmentName).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return redirect(url_for('gradebook'))

#################################################

@app.route("/GradebookSortStudent", methods=["GET", "POST"])
def gradebooksortstudent():
    if request.method == "GET":
        # --- defaultload
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        # --- defaultload
        student_grades = db.session.query(Assignment.AssignmentId, Assignment.AssignmentName, Student.FirstName, Student.LastName, Student.StudentId, Gradebook.AssignmentGrade).outerjoin(Gradebook, Assignment.AssignmentId == Gradebook.AssignmentId).outerjoin(Student, Student.StudentId == Gradebook.StudentId).order_by(Student.FirstName.asc(),Assignment.AssignmentName.asc()).all()
        return render_template("gradebook.html", gradebookcount=gradebookcount, student_grades=student_grades, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentId).order_by(Assignment.AssignmentName).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return redirect(url_for('gradebook'))

#################################################

@app.route("/GradebookSortGrade", methods=["GET", "POST"])
def gradebooksortgrade():
    if request.method == "GET":
        # --- defaultload
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        # --- defaultload
        student_grades = db.session.query(Assignment.AssignmentId, Assignment.AssignmentName, Student.FirstName, Student.LastName, Student.StudentId, Gradebook.AssignmentGrade).outerjoin(Gradebook, Assignment.AssignmentId == Gradebook.AssignmentId).outerjoin(Student, Student.StudentId == Gradebook.StudentId).order_by(Gradebook.AssignmentGrade.asc(),Assignment.AssignmentId.asc(),Student.FirstName.asc()).all()
        return render_template("gradebook.html", gradebookcount=gradebookcount, student_grades=student_grades, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentId).order_by(Assignment.AssignmentName).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return redirect(url_for('gradebook'))


#################################################

@app.route("/StudentGrade", methods=["GET", "POST"])
def studentgrade():
    if request.method == "POST":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        id = request.form.get("Student_ID")
        student_assigned_id = id
        first_name = Student.query.filter_by(StudentId=id).first().FirstName
        last_name = Student.query.filter_by(StudentId=id).first().LastName
        student_assignments = db.session.query(Assignment.AssignmentId, Assignment.AssignmentName, Gradebook.AssignmentGrade, Student.StudentId).outerjoin(Gradebook, Assignment.AssignmentId == Gradebook.AssignmentId).outerjoin(Student, Student.StudentId == Gradebook.StudentId).filter_by(StudentId=id).order_by(Assignment.AssignmentId).all()
        student_grades_count = db.session.query(Gradebook.AssignmentGrade).outerjoin(Student, Student.StudentId == Gradebook.StudentId).filter_by(StudentId=id).count()
        student_grades_list = db.session.query(Gradebook.AssignmentGrade).outerjoin(Student, Student.StudentId == Gradebook.StudentId).filter_by(StudentId=id).all()
        points_awarded = 0
        points_available = 0

        if student_grades_count > 0:
            for i in range(0,student_grades_count):
                grade_to_calc = student_grades_list[i].AssignmentGrade
                if grade_to_calc == 'A':
                    points_awarded = points_awarded + 10
                    points_available = points_available + 10
                elif grade_to_calc == 'B':
                    points_awarded = points_awarded + 8
                    points_available = points_available + 10
                elif grade_to_calc == 'C':
                    points_awarded = points_awarded + 7
                    points_available = points_available + 10
                elif grade_to_calc == 'D':
                    points_awarded = points_awarded + 6
                    points_available = points_available + 10
                elif grade_to_calc == 'E':
                    points_awarded = points_awarded + 5
                    points_available = points_available + 10
                elif grade_to_calc == '4':
                    points_awarded = points_awarded + 4
                    points_available = points_available + 10
                elif grade_to_calc == 'NA':
                    points_awarded = points_awarded
                    points_available = points_available

            if points_available == 0:
                letter_grade = 'NA'
            elif points_available > 0:
                grade_percentage = ((points_awarded/points_available)*100)
                if grade_percentage < 50:
                    letter_grade = 'F'
                elif grade_percentage < 60:
                    letter_grade = 'E'
                elif grade_percentage < 70:
                    letter_grade = 'D'
                elif grade_percentage < 80:
                    letter_grade = 'C'
                elif grade_percentage <90:
                    letter_grade = 'B'
                elif grade_percentage < 101:
                    letter_grade = 'A'

            return render_template("student_gradebook.html", student_assigned_id=student_assigned_id, student_info=Student.query.filter_by(StudentId=id).first(), letter_grade=letter_grade, gradebookcount=gradebookcount, student_assignments=student_assignments, first_name=first_name, last_name=last_name, student=student, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentName).all())
        return render_template("student_gradebook.html", student_assigned_id=student_assigned_id, student_info=Student.query.filter_by(StudentId=id).first(), gradebookcount=gradebookcount, student_assignments=student_assignments, first_name=first_name, last_name=last_name, student=student, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentName).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return redirect(url_for('student'))

#################################################

@app.route("/StudentGradeSortGrade", methods=["GET", "POST"])
def studentgradesortgrade():
    if request.method == "POST":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        id = request.form.get("student_id_focus")
        student_assigned_id = id
        first_name = Student.query.filter_by(StudentId=id).first().FirstName
        last_name = Student.query.filter_by(StudentId=id).first().LastName
        student_assignments = db.session.query(Assignment.AssignmentId, Assignment.AssignmentName, Gradebook.AssignmentGrade, Student.StudentId).outerjoin(Gradebook, Assignment.AssignmentId == Gradebook.AssignmentId).outerjoin(Student, Student.StudentId == Gradebook.StudentId).filter_by(StudentId=id).order_by(Gradebook.AssignmentGrade.asc(), Assignment.AssignmentId.asc()).all()
        student_grades_count = db.session.query(Gradebook.AssignmentGrade).outerjoin(Student, Student.StudentId == Gradebook.StudentId).filter_by(StudentId=id).count()
        student_grades_list = db.session.query(Gradebook.AssignmentGrade).outerjoin(Student, Student.StudentId == Gradebook.StudentId).filter_by(StudentId=id).all()
        points_awarded = 0
        points_available = 0

        if student_grades_count > 0:
            for i in range(0,student_grades_count):
                grade_to_calc = student_grades_list[i].AssignmentGrade
                if grade_to_calc == 'A':
                    points_awarded = points_awarded + 10
                    points_available = points_available + 10
                elif grade_to_calc == 'B':
                    points_awarded = points_awarded + 8
                    points_available = points_available + 10
                elif grade_to_calc == 'C':
                    points_awarded = points_awarded + 7
                    points_available = points_available + 10
                elif grade_to_calc == 'D':
                    points_awarded = points_awarded + 6
                    points_available = points_available + 10
                elif grade_to_calc == 'E':
                    points_awarded = points_awarded + 5
                    points_available = points_available + 10
                elif grade_to_calc == '4':
                    points_awarded = points_awarded + 4
                    points_available = points_available + 10
                elif grade_to_calc == 'NA':
                    points_awarded = points_awarded
                    points_available = points_available

            if points_available == 0:
                letter_grade = 'NA'
            elif points_available > 0:
                grade_percentage = ((points_awarded/points_available)*100)
                if grade_percentage > 89:
                    letter_grade = 'A'
                elif grade_percentage > 79:
                    letter_grade = 'B'
                elif grade_percentage > 69:
                    letter_grade = 'C'
                elif grade_percentage >59:
                    letter_grade = 'D'
                elif grade_percentage > 49:
                    letter_grade ='E'
                elif grade_percentage < 50:
                    letter_grade = 'F'
            return render_template("student_gradebook.html", student_assigned_id=student_assigned_id, student_info=Student.query.filter_by(StudentId=id).first(), letter_grade=letter_grade, gradebookcount=gradebookcount, student_assignments=student_assignments, first_name=first_name, last_name=last_name, student=student, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentName).all())
        return render_template("student_gradebook.html", student_assigned_id=student_assigned_id, student_info=Student.query.filter_by(StudentId=id).first(), gradebookcount=gradebookcount, student_assignments=student_assignments, first_name=first_name, last_name=last_name, student=student, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentName).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return redirect(url_for('student'))

#################################################

@app.route("/StudentGradeSortAssignment", methods=["GET", "POST"])
def studentgradesortassignment():
    if request.method == "POST":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        id = request.form.get("student_id_focus")
        student_assigned_id = id
        first_name = Student.query.filter_by(StudentId=id).first().FirstName
        last_name = Student.query.filter_by(StudentId=id).first().LastName
        student_assignments = db.session.query(Assignment.AssignmentId, Assignment.AssignmentName, Gradebook.AssignmentGrade, Student.StudentId).outerjoin(Gradebook, Assignment.AssignmentId == Gradebook.AssignmentId).outerjoin(Student, Student.StudentId == Gradebook.StudentId).filter_by(StudentId=id).order_by(Assignment.AssignmentName.asc(), Gradebook.AssignmentGrade.asc()).all()
        student_grades_count = db.session.query(Gradebook.AssignmentGrade).outerjoin(Student, Student.StudentId == Gradebook.StudentId).filter_by(StudentId=id).count()
        student_grades_list = db.session.query(Gradebook.AssignmentGrade).outerjoin(Student, Student.StudentId == Gradebook.StudentId).filter_by(StudentId=id).all()
        points_awarded = 0
        points_available = 0

        if student_grades_count > 0:
            for i in range(0,student_grades_count):
                grade_to_calc = student_grades_list[i].AssignmentGrade
                if grade_to_calc == 'A':
                    points_awarded = points_awarded + 10
                    points_available = points_available + 10
                elif grade_to_calc == 'B':
                    points_awarded = points_awarded + 8
                    points_available = points_available + 10
                elif grade_to_calc == 'C':
                    points_awarded = points_awarded + 7
                    points_available = points_available + 10
                elif grade_to_calc == 'D':
                    points_awarded = points_awarded + 6
                    points_available = points_available + 10
                elif grade_to_calc == 'E':
                    points_awarded = points_awarded + 5
                    points_available = points_available + 10
                elif grade_to_calc == '4':
                    points_awarded = points_awarded + 4
                    points_available = points_available + 10
                elif grade_to_calc == 'NA':
                    points_awarded = points_awarded
                    points_available = points_available

            if points_available == 0:
                letter_grade = 'NA'
            elif points_available > 0:
                grade_percentage = ((points_awarded/points_available)*100)
                if grade_percentage > 89:
                    letter_grade = 'A'
                elif grade_percentage > 79:
                    letter_grade = 'B'
                elif grade_percentage > 69:
                    letter_grade = 'C'
                elif grade_percentage >59:
                    letter_grade = 'D'
                elif grade_percentage > 49:
                    letter_grade ='E'
                elif grade_percentage < 50:
                    letter_grade = 'F'
            return render_template("student_gradebook.html", student_assigned_id=student_assigned_id, student_info=Student.query.filter_by(StudentId=id).first(), letter_grade=letter_grade, gradebookcount=gradebookcount, student_assignments=student_assignments, first_name=first_name, last_name=last_name, student=student, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentName).all())
        return render_template("student_gradebook.html", student_assigned_id=student_assigned_id, student_info=Student.query.filter_by(StudentId=id).first(), gradebookcount=gradebookcount, student_assignments=student_assignments, first_name=first_name, last_name=last_name, student=student, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentName).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return redirect(url_for('student'))

#################################################

@app.route("/StudentGradeSortAssignmentId", methods=["GET", "POST"])
def studentgradesortassignmentid():
    if request.method == "POST":
        studentcount = Student.query.count()
        assignmentcount = Assignment.query.count()
        gradebookcount = Gradebook.query.filter_by(AssignmentGrade='NA').count()
        id = request.form.get("student_id_focus")
        student_assigned_id = id
        first_name = Student.query.filter_by(StudentId=id).first().FirstName
        last_name = Student.query.filter_by(StudentId=id).first().LastName
        student_assignments = db.session.query(Assignment.AssignmentId, Assignment.AssignmentName, Gradebook.AssignmentGrade, Student.StudentId).outerjoin(Gradebook, Assignment.AssignmentId == Gradebook.AssignmentId).outerjoin(Student, Student.StudentId == Gradebook.StudentId).filter_by(StudentId=id).order_by(Assignment.AssignmentId.asc()).all()
        student_grades_count = db.session.query(Gradebook.AssignmentGrade).outerjoin(Student, Student.StudentId == Gradebook.StudentId).filter_by(StudentId=id).count()
        student_grades_list = db.session.query(Gradebook.AssignmentGrade).outerjoin(Student, Student.StudentId == Gradebook.StudentId).filter_by(StudentId=id).all()
        points_awarded = 0
        points_available = 0

        if student_grades_count > 0:
            for i in range(0,student_grades_count):
                grade_to_calc = student_grades_list[i].AssignmentGrade
                if grade_to_calc == 'A':
                    points_awarded = points_awarded + 10
                    points_available = points_available + 10
                elif grade_to_calc == 'B':
                    points_awarded = points_awarded + 8
                    points_available = points_available + 10
                elif grade_to_calc == 'C':
                    points_awarded = points_awarded + 7
                    points_available = points_available + 10
                elif grade_to_calc == 'D':
                    points_awarded = points_awarded + 6
                    points_available = points_available + 10
                elif grade_to_calc == 'E':
                    points_awarded = points_awarded + 5
                    points_available = points_available + 10
                elif grade_to_calc == '4':
                    points_awarded = points_awarded + 4
                    points_available = points_available + 10
                elif grade_to_calc == 'NA':
                    points_awarded = points_awarded
                    points_available = points_available

            if points_available == 0:
                letter_grade = 'NA'
            elif points_available > 0:
                grade_percentage = ((points_awarded/points_available)*100)
                if grade_percentage > 89:
                    letter_grade = 'A'
                elif grade_percentage > 79:
                    letter_grade = 'B'
                elif grade_percentage > 69:
                    letter_grade = 'C'
                elif grade_percentage >59:
                    letter_grade = 'D'
                elif grade_percentage > 49:
                    letter_grade ='E'
                elif grade_percentage < 50:
                    letter_grade = 'F'
            return render_template("student_gradebook.html", student_assigned_id=student_assigned_id, student_info=Student.query.filter_by(StudentId=id).first(), letter_grade=letter_grade, gradebookcount=gradebookcount, student_assignments=student_assignments, first_name=first_name, last_name=last_name, student=student, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentName).all())
        return render_template("student_gradebook.html", student_assigned_id=student_assigned_id, student_info=Student.query.filter_by(StudentId=id).first(), gradebookcount=gradebookcount, student_assignments=student_assignments, first_name=first_name, last_name=last_name, student=student, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentName).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return redirect(url_for('student'))

#################################################

@app.route("/EnterGrade", methods=["GET", "POST"])
def entergrade():
    if request.method == "POST":
        assignment_id = request.form.get("assignment_id")
        student_id = request.form.get("student_id")
        new_grade = request.form.get("new_grade")
        gradebook_record = Gradebook.query.filter_by(AssignmentId=assignment_id).filter_by(StudentId=student_id).first()
        gradebook_record.AssignmentGrade = new_grade
        db.session.commit()
        return redirect(url_for('gradebook'))
        #return render_template("gradebook.html", gradebookcount=gradebookcount, student=student, studentcount=studentcount, assignmentcount = assignmentcount, assignments=Assignment.query.order_by(Assignment.AssignmentName).all())

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return redirect(url_for('gradebook'))

#################################################

@app.route("/RemoveStudent", methods=["GET", "POST"])
def remove():
    if request.method == "GET":
        return render_template("students.html", students=Student.query.all())

    id = request.form.get("studentid_remove") #getid
    preindex_count = Gradebook.query.filter_by(StudentId=id).count() #numberintable
    if preindex_count == 0: #if student is not in gradebook then only delete student
        student = Student.query.filter_by(StudentId=id).first()
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('student'))
    elif preindex_count > 1: #if student is in gradebook, then delete their assignments from gradebook
        studentassignment_exist = preindex_count-1 #substract 1 to accomodate index
        for i in range(0, studentassignment_exist):
            assingment_list = Gradebook.query.filter_by(StudentId=id).first()
            db.session.delete(assingment_list)
            db.session.commit()
        db.session.commit()
        student = Student.query.filter_by(StudentId=id).first()
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('student'))

#################################################

@app.route("/RemoveAssignment", methods=["GET", "POST"])
def remove_assignment():
    if request.method == "GET":
        return render_template("assignment.html", assignments=Assignment.query.all())

    id = request.form.get("assignment_delete")
    preindex_count = Gradebook.query.filter_by(AssignmentId=id).count() #numberintable
    if preindex_count > 1:
        assignment_exist = preindex_count-1 #substract 1 to accomodate index
        for i in range(0, assignment_exist):
            get_assignment = Gradebook.query.filter_by(AssignmentId=id).first()
            db.session.delete(get_assignment)
            db.session.commit()
        db.session.commit()

    assingment_list = Gradebook.query.filter_by(AssignmentId=id).first()
    db.session.delete(assingment_list)
    db.session.commit()

    assignment = Assignment.query.filter_by(AssignmentId=id).first()
    db.session.delete(assignment)
    db.session.commit()
    return redirect(url_for('assignment'))

#################################################

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))

#################################################

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#################################################

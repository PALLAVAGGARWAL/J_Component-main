from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cms_db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class CMS(db.Model) :
    sno = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(100), nullable=False)
    l_name = db.Column(db.String(100))
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)

class Student(db.Model) :
    reg_no = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer)
    batch = db.Column(db.Integer, nullable=False)

class Faculty(db.Model) :
    reg_no = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer)
    email = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.String(50), nullable=False)

class Courses(db.Model) :
    course_id = db.Column(db.String(30), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    course_type = db.Column(db.String(100), nullable=False)
    credit = db.Column(db.Integer)

class my_course(db.Model) :
    course_id = db.Column(db.String(30), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    course_type = db.Column(db.String(100), nullable=False)
    credit = db.Column(db.Integer)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_up', methods=['POST'])
def sign_up():
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    login = CMS(f_name=f_name, l_name=l_name, email=email, username=username, password=password)
    db.session.add(login)
    db.session.commit()
    return render_template('index.html', f_name=f_name, l_name=l_name)



# STUDENT
@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/student_view2')
def student_view2():
    allStudents = Student.query.all()
    return render_template('student_view2.html', allStudents=allStudents)

@app.route('/student_view')
def student_view():
    return render_template('student_view.html')

@app.route('/student_view', methods=['POST'])
def studetnView():
    reg_no = request.form['reg_no']
    username = request.form['username']
    password = request.form['password']
    stud = Student.query.filter_by(reg_no=reg_no)
    acct = CMS.query.filter_by(username=username).first()
    message = None
    if acct is None or acct.password != password :
        message = "Invalid Username or Password"
        return render_template('student_view.html', message=message)
    return render_template('student_view.html', stud=stud, message=message)

@app.route('/student_add')
def student_add():
    return render_template('student_add.html')

@app.route('/student_add', methods=['POST'])
def studentAdd():
    reg_no = request.form['reg_no']
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    batch = request.form['batch']
    course = request.form['course']
    phone = request.form['phone']
    stud = Student(reg_no=reg_no, name=name, email=email, age=age, batch=batch, course=course, phone=phone)
    db.session.add(stud)
    db.session.commit()
    return render_template('student_add.html', title=name)




# FACULTY
@app.route('/faculty')
def faculty():
    return render_template('faculty.html')

@app.route('/faculty_view')
def facultyview():
    allFaculty = Faculty.query.all()
    return render_template('faculty_view.html', allFaculty=allFaculty)

@app.route('/faculty_view', methods=['POST'])
def faculty_view():
    reg_no = request.form['reg_no']
    faculty = Faculty.query.filter_by(reg_no=reg_no)
    return render_template('faculty_view.html', faculty=faculty)

@app.route('/faculty_add')
def facultyadd():
    return render_template('faculty_add.html')

@app.route('/faculty_add', methods=['POST'])
def faculty_add():
    reg_no = request.form['reg_no']
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    rank = request.form['rank']
    fac = Faculty(reg_no=reg_no, name=name, phone=phone, email=email, rank=rank)
    db.session.add(fac)
    db.session.commit()
    return render_template('faculty_add.html', name=name)

@app.route('/faculty_edit')
def facultyedit():
    allFaculty = Faculty.query.all()
    return render_template('faculty_del.html', allFaculty=allFaculty)

@app.route('/faculty_edit', methods=['POST'])
def faculty_edit():
    reg_no = request.form['reg_no']
    faculty = Faculty.query.filter_by(reg_no=reg_no).first()
    db.session.delete(faculty)
    db.session.commit()
    allFaculty = Faculty.query.all()
    return render_template('faculty_del.html', faculty=faculty, allFaculty=allFaculty)




# COURSES
@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/course_view')
def course_view():
    allCourses = Courses.query.all()
    return render_template('course_view.html', allCourses=allCourses)

@app.route('/course_view2')
def course_view2():
    allCourses = my_course.query.all()
    total = 0
    for course in allCourses :
        total += course.credit
    return render_template('my_courses.html', allCourses=allCourses, total=total)

@app.route('/course_view', methods=['POST'])
def courseView():
    course_id = request.form['course_id']
    courses = Courses.query.filter_by(course_id=course_id)
    return render_template('course_view.html', courses=courses)

@app.route('/course_add')
def courseAdd():
    allCourses = Courses.query.all()
    return render_template('course_add2.html', allCourses=allCourses)

@app.route('/course_add2', methods=['POST'])
def course_add2():
    allCourses = Courses.query.all()
    course_id = request.form['course_id']
    cou = Courses.query.filter_by(course_id=course_id).first()
    mycourse = my_course(course_id=cou.course_id, title=cou.title, course_type=cou.course_type, credit=cou.credit)
    db.session.add(mycourse)
    db.session.commit()
    return render_template('course_add2.html', allCourses=allCourses, title=cou.title,)

@app.route('/course_add', methods=['POST'])
def course_add():
    course_id = request.form['course_id']
    title = request.form['title']
    course_type = request.form['type']
    credit = request.form['credits']
    cou = Courses(course_id=course_id, title=title, course_type=course_type, credit=credit)
    db.session.add(cou)
    db.session.commit()
    return render_template('course_add.html', title=title)

@app.route('/course_edit')
def course_edit():
    allCourses = my_course.query.all()
    return render_template('course_edit.html', allCourses=allCourses)

@app.route('/course_edit', methods=['POST'])
def courseEdit():
    course_id = request.form['course_id']
    cou = my_course.query.filter_by(course_id=course_id).first()
    db.session.delete(cou)
    db.session.commit()
    allCourses = my_course.query.all()
    return render_template('course_edit.html', title=cou.title, allCourses=allCourses)

if __name__ == '__main__':
    app.run(debug=True)
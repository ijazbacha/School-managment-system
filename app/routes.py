from sqlalchemy.orm import query
from app import app, db
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin, Student, Teacher, Worker, Class



@app.route('/')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/admin_login', methods=['POST', 'GET'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #remember_me = request.form['remember_me']


        admin = Admin.query.filter_by(username=username).first()
        if admin is None or not admin.check_password(password):
            flash('Invild password or username!')
            return redirect(url_for('admin_login'))

        if request.form.get('remember_me') == 'True':
            login_user(admin, remember=True)
            flash('Logged in successfully.')
            return redirect(url_for('index'))      

        login_user(admin, remember=False)
        flash('Logged in successfully.')
        return redirect(url_for('index'))

    return render_template('login.html', title='Login')


@app.route('/admin_logout')
def admin_logout():
    logout_user()
    flash('Successfully logout.')
    return redirect(url_for('admin_login'))


@app.route('/admin_registration', methods=['POST', 'GET'])
def admin_registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repeatpassword = request.form['repeatpassword']

        if len(password) < 8:
            flash('Password must be 8 or greater!')
            return redirect(url_for('admin_registration'))

        if password != repeatpassword:
            flash('Your password is not match!')
            return redirect(url_for('admin_registration'))
        
        user = Admin.query.filter_by(username=username).first()
        if user is not None:
            flash('Please use a different username!')
            return redirect(url_for('admin_registration'))

        user = Admin.query.filter_by(email=email).first()
        if user is not None:
            flash('Please use a different email!')
            return redirect(url_for('admin_registration'))

        admin = Admin(username=username, email=email)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        flash("Successfully register")
        return redirect(url_for('admin_login'))
    return render_template('register.html', title='Registration')


@app.route('/add_class', methods=['GET', 'POST'])
def add_class():
    classes = Class.query.all()
    if request.method == 'POST':
        cls_name = request.form['cls_name']
        db.session.add(Class(cls_name=cls_name))
        db.session.commit()
        return redirect(url_for('add_class'))
    return render_template('add_class.html', classes=classes)



@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    classes = Class.query.all()
    if request.method == 'POST':
        std_name = request.form['std_name']
        f_name = request.form['f_name']
        std_address = request.form['std_address']
        std_contact = request.form['std_contact']
        stdclass = request.form['stdclass']

        classes = Class.query.filter_by(id=stdclass).first()
        student = Student(
            std_name=std_name,
            f_name=f_name,
            std_address=std_address,
            std_contact=std_contact,
            stdclass=classes,
            admin=current_user
                        )
        db.session.add(student)
        db.session.commit()
        flash('Student successfully added')
        return redirect(url_for('add_student'))

    return render_template('add_student.html', title='Add Student', classes=classes)


@app.route('/student_Detials')
def student_Detials():
    students = Student.query.all()
    return render_template('student_Detials.html', title='Student Detials', students=students)



@app.route('/add_worker', methods=['GET', 'POST'])
@login_required
def add_worker():
    if request.method == 'POST':
        worker_name = request.form['worker_name']
        worker_address = request.form['worker_address']
        worker_contact = request.form['worker_contact']
        worker = Worker(worker_name=worker_name, worker_address=worker_address, worker_contact=worker_contact, admin=current_user)
        db.session.add(worker)
        db.session.commit()
        return redirect(url_for('add_worker'))

    return render_template('worker.html', title='Worker')


@app.route('/worker_detials')
def worker_detials():
    workers = Worker.query.all()
    return render_template('worker_detials.html', title='Worker Detials', workers=workers)


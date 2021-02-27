from sqlalchemy.orm import query
from app import app, db
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin, Student, Teacher, Worker, LeaveWorker, Class


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
    if request.method == 'POST':
        cls_name = request.form['cls_name']
        db.session.add(Class(cls_name=cls_name))
        db.session.commit()
        flash('{} is successfully added'.format(cls_name))
        return redirect(url_for('list_of_class'))
    return render_template('add_class.html')


@app.route('/list_of_class')
def list_of_class():
    classes = Class.query.all()
    return render_template('list_of_class.html', classes=classes)


@app.route('/class_wise_student/<std_class>')
def class_wise_student(std_class):
    class_name = Class.query.filter_by(id=std_class).first()
    students = Student.query.filter_by(std_class=std_class).all()
    return render_template('class_wise_student.html', title='Class Wise Student', class_name=class_name, students=students)




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
        flash('{} is successfully added'.format(std_name))
        return redirect(url_for('add_student'))

    return render_template('add_student.html', title='Add Student', classes=classes)


@app.route('/student_Detials')
def student_Detials():
    students = Student.query.all()
    return render_template('student_Detials.html', title='Student Detials', students=students)


@app.route('/student_profile/<id>')
def student_profile(id):
    student_profile = Student.query.filter_by(id=id).first()
    return render_template('student_profile.html', title='Student Profile', student_profile=student_profile)



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
        flash('{} is successfully added'.format(worker_name))
        return redirect(url_for('worker_detials'))

    return render_template('worker.html', title='Worker', worker=None)



@app.route('/worker_detials')
def worker_detials():
    query = request.args.get('query')
    if query:
        workers = Worker.query.filter(Worker.worker_name.contains(query))
        return render_template('worker_detials.html', title='Search Worker', workers=workers, query=query)
    
    page = request.args.get('page', 1, type=int)   
    workers = Worker.query.order_by(Worker.id.asc()).paginate(
        page, app.config['ENTRY_PER_PAGE'], False)
    next_url = url_for('worker_detials', page=workers.next_num) \
        if workers.has_next else None
    prev_url = url_for('worker_detials', page=workers.prev_num) \
        if workers.has_prev else None
    return render_template('worker_detials.html', title='Worker Detials', workers=workers.items, next_url=next_url, prev_url=prev_url, page=page)



@app.route('/update_worker/<id>', methods=['GET', 'POST'])
def update_worker(id):
    worker = Worker.query.filter_by(id=id).first()
    if request.method == 'POST':
        worker.worker_name = request.form['worker_name']
        worker.worker_address = request.form['worker_address']
        worker.worker_contact = request.form['worker_contact']
        worker.admin_id = current_user.id
        worker.join_date = datetime.utcnow()
        db.session.commit()
        flash('{} is successfully update'.format(worker.worker_name))
        return redirect(url_for('worker_detials'))

    return render_template('worker.html', title='Worker', worker=worker)



@app.route('/leave_worker/<id>')
def leave_worker(id):
    worker = Worker.query.filter_by(id=id).first()
    try:
        if worker:
            leave_worker_name = worker.worker_name
            leave_worker_address = worker.worker_address
            leave_worker_contact = worker.worker_contact
            admin_id = current_user.id
            l_worker = LeaveWorker(
                            leave_worker_name=leave_worker_name,
                            leave_worker_address=leave_worker_address, 
                            leave_worker_contact=leave_worker_contact,
                            admin_id=admin_id)
            db.session.add(l_worker)
            db.session.commit()
            
            db.session.delete(worker)
            db.session.commit()
            flash('{} is successfully leave'.format(worker.worker_name))
            return redirect(url_for('worker_detials'))
    except:
        return redirect(url_for('worker_detials'))


@app.route('/leave_worker_detials')
def leave_worker_detials():
    query = request.args.get('query')
    if query:
        leave_worker = LeaveWorker.query.filter(LeaveWorker.leave_worker_name.contains(query))
        return render_template('leave_worker.html', title='Leave Worker', leave_worker=leave_worker, query=query)

    page = request.args.get('page', 1, type=int)
    leave_worker = LeaveWorker.query.order_by(LeaveWorker.id.asc()).paginate(
        page, app.config['ENTRY_PER_PAGE'], False)
    next_url = url_for('leave_worker_detials', page=leave_worker.next_num) \
        if leave_worker.has_next else None
    prev_url = url_for('leave_worker_detials', page=leave_worker.prev_num) \
        if leave_worker.has_prev else None
    return render_template('leave_worker.html', title='Leave Worker', leave_worker=leave_worker.items, next_url=next_url, prev_url=prev_url)



@app.route('/leave_worker_delete/<id>')
def leave_worker_delete(id):
    leave_worker = LeaveWorker.query.filter_by(id=id).first()
    try:
        if leave_worker:
            db.session.delete(leave_worker)
            db.session.commit()
            flash('Worker {} is premenent delete!'.format(leave_worker.leave_worker_name))
            return redirect(url_for('leave_worker_detials'))
    except:
        return redirect(url_for('leave_worker_detials'))









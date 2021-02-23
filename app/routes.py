from app import app, db
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin, Student, Teacher, Worker



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


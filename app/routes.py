from app import app, db
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin



@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/admin_login', methods=['POST', 'GET'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = request.form['remember_me']

        admin = Admin.query.filter_by(username=username).first()
        if admin is None and not admin.check_password(password):
            flash('Invild password or username!')
            return redirect(url_for('admin_login'))
        login_user(admin, remember=remember_me)
        return redirect(url_for('index'))

    return render_template('login.html', title='Login')

@app.route('/admin_registration')
def admin_registration():
    return render_template('register.html')
from app import db, login, app
from flask import redirect, url_for
from flask_login import UserMixin, current_user
from datetime import datetime
from flask_admin import  Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash 



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    join_date = db.Column(db.DateTime, default=datetime.utcnow())
    student = db.relationship('Student', backref='admin')
    leavestudent = db.relationship('LeaveStudent', backref='admin')
    teacher = db.relationship('Teacher', backref='admin')
    leaveteacher = db.relationship('LeaveTeacher', backref='admin')
    worker = db.relationship('Worker', backref='admin')
    leaveworker = db.relationship('LeaveWorker', backref='admin')
    classs = db.relationship('Class', backref='admin')
    subject = db.relationship('Subject', backref='admin')

    def __repr__(self):
        return 'Admin -> {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cls_name = db.Column(db.String(64), index=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student = db.relationship('Student', backref='stdclass')
    leavestudent = db.relationship('LeaveStudent', backref='stdclass')

    def __repr__(self):
        return 'Class {}'.format(self.cls_name)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    std_name = db.Column(db.String(64), index=True)
    f_name = db.Column(db.String(64), index=True)
    std_address = db.Column(db.String(128), index=True)
    std_contact = db.Column(db.String(64), index=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow())
    std_class = db.Column(db.Integer, db.ForeignKey('class.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Student {}'.format(self.std_name)

class LeaveStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    std_name = db.Column(db.String(64), index=True)
    f_name = db.Column(db.String(64), index=True)
    std_address = db.Column(db.String(128), index=True)
    std_contact = db.Column(db.String(64), index=True)
    leave_date = db.Column(db.DateTime, default=datetime.utcnow())
    std_class = db.Column(db.Integer, db.ForeignKey('class.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Leave Student {}'.format(self.std_name)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.String(64))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    teacher = db.relationship('Teacher', backref='sub')
    leaveteacher = db.relationship('LeaveTeacher', backref='sub')

    def __repr__(self):
        return 'Subject {}'.format(self.sub_name)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tech_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True)
    tech_address = db.Column(db.String(128), index=True)
    tech_contact = db.Column(db.String(64), index=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow())
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tech_subject = db.Column(db.Integer, db.ForeignKey('subject.id'))
    uploadlecture = db.relationship('UploadLecture', backref='t_lecture')

    def __repr__(self):
        return 'Teacher {}'.format(self.tech_name)


class LeaveTeacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tech_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True)
    tech_address = db.Column(db.String(128), index=True)
    tech_contact = db.Column(db.String(64), index=True)
    leave_date = db.Column(db.DateTime, default=datetime.utcnow())
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tech_subject = db.Column(db.Integer, db.ForeignKey('subject.id'))

    def __repr__(self):
        return 'LeaveTeacher {}'.format(self.tech_name)


class UploadLecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    lecture = db.Column(db.String(64))
    img = db.Column(db.LargeBinary)
    img_name = db.Column(db.String(64))
    teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'))


    def __repr__(self):
        return 'Lecture {}'.format(self.title)


class Worker(db.Model):
    __searchable__ = ['worker_name', 'worker_address']
    
    id = db.Column(db.Integer, primary_key=True)
    worker_name = db.Column(db.String(64), index=True)
    worker_address = db.Column(db.String(128), index=True)
    worker_contact = db.Column(db.String(64), index=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow())
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Worker {}'.format(self.worker_name)


class LeaveWorker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leave_worker_name = db.Column(db.String(64), index=True)
    leave_worker_address = db.Column(db.String(128), index=True)
    leave_worker_contact = db.Column(db.String(64), index=True)
    leave_date = db.Column(db.DateTime, default=datetime.utcnow())
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Leave Worker {}'.format(self.leave_worker_name)



class MyAdminIndexViewView(AdminIndexView):

    def is_accessible(self):
        
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('admin_login'))
        
admin = Admin(app, name='schoolmanagment', template_mode='bootstrap3', index_view=MyAdminIndexViewView())






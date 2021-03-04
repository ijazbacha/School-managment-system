from app import db, login
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash 


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    join_date = db.Column(db.DateTime, default=datetime.utcnow())
    student = db.relationship('Student', backref='admin')
    leavestudent = db.relationship('LeaveStudent', backref='admin')
    teacher = db.relationship('Teacher', backref='admin')
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
    return Admin.query.get(int(id))


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cls_name = db.Column(db.String(64), index=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
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
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

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
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return 'Leave Student {}'.format(self.std_name)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.String(64))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    teacher = db.relationship('Teacher', backref='sub')

    def __repr__(self):
        return 'Subject {}'.format(self.sub_name)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tech_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True)
    tech_address = db.Column(db.String(128), index=True)
    tech_contact = db.Column(db.String(64), index=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow())
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    tech_subject = db.Column(db.Integer, db.ForeignKey('subject.id'))

    def __repr__(self):
        return 'Teacher {}'.format(self.tech_name)


class Worker(db.Model):
    __searchable__ = ['worker_name', 'worker_address']
    
    id = db.Column(db.Integer, primary_key=True)
    worker_name = db.Column(db.String(64), index=True)
    worker_address = db.Column(db.String(128), index=True)
    worker_contact = db.Column(db.String(64), index=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow())
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return 'Worker {}'.format(self.worker_name)


class LeaveWorker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leave_worker_name = db.Column(db.String(64), index=True)
    leave_worker_address = db.Column(db.String(128), index=True)
    leave_worker_contact = db.Column(db.String(64), index=True)
    leave_date = db.Column(db.DateTime, default=datetime.utcnow())
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return 'Leave Worker {}'.format(self.leave_worker_name)

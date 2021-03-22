from app import db, login, app
from flask import redirect, url_for
from flask_login import UserMixin, current_user
from datetime import datetime, date
from flask_admin import  Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash 



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(64), unique=True)
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


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.Text)
    sender = db.Column(db.String(64))
    notify_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return 'Notifaction {}'.format(self.notifaction[0:10])



class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cls_name = db.Column(db.String(64))
    cls_fee = db.Column(db.String(64))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student = db.relationship('Student', backref='stdclass')
    leavestudent = db.relationship('LeaveStudent', backref='stdclass')
    uploadlecture = db.relationship('UploadLecture', backref='stdclass')
    teacher = db.relationship('Teacher', backref='stdclass')
    attendance = db.relationship('StudentAttendance', backref='stdclass')

    def __repr__(self):
        return 'Class {}'.format(self.cls_name)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    std_name = db.Column(db.String(64))
    f_name = db.Column(db.String(64))
    std_address = db.Column(db.String(128))
    std_contact = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    join_date = db.Column(db.DateTime, default=datetime.utcnow())
    std_class = db.Column(db.Integer, db.ForeignKey('class.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    attendance = db.relationship('StudentAttendance', backref='std')
    
    

    def __repr__(self):
        return 'Student {}'.format(self.std_name)

class LeaveStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    std_name = db.Column(db.String(64))
    f_name = db.Column(db.String(64))
    std_address = db.Column(db.String(128))
    std_contact = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    leave_date = db.Column(db.DateTime, default=datetime.utcnow())
    std_class = db.Column(db.Integer, db.ForeignKey('class.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Leave Student {}'.format(self.std_name)


class StudentAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attendance = db.Column(db.String(64))
    std_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow())
    

    def __repr__(self):
        return 'Student Attendance {}'.format(self.date)



class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.String(64))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    teacher = db.relationship('Teacher', backref='sub')
    leaveteacher = db.relationship('LeaveTeacher', backref='sub')
    uploadlecture = db.relationship('UploadLecture', backref='sub')
    

    def __repr__(self):
        return 'Subject {}'.format(self.sub_name)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tech_name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    tech_address = db.Column(db.String(128))
    tech_contact = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    salary = db.Column(db.String(64))
    join_date = db.Column(db.DateTime, default=datetime.utcnow())
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tech_subject = db.Column(db.Integer, db.ForeignKey('subject.id'))
    tech_class = db.Column(db.Integer, db.ForeignKey('class.id'))
    uploadlecture = db.relationship('UploadLecture', backref='t_lecture')
    attendance = db.relationship('StudentAttendance', backref='t_lecture')

    def __repr__(self):
        return 'Teacher {}'.format(self.tech_name)


class LeaveTeacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tech_name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    tech_address = db.Column(db.String(128))
    tech_contact = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    salary = db.Column(db.String(64))
    leave_date = db.Column(db.DateTime, default=datetime.utcnow())
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tech_subject = db.Column(db.Integer, db.ForeignKey('subject.id'))

    def __repr__(self):
        return 'LeaveTeacher {}'.format(self.tech_name)


class UploadLecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    lecture = db.Column(db.Text)
    img = db.Column(db.LargeBinary)
    img_name = db.Column(db.String(64))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow())
    teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    tech_subject = db.Column(db.Integer, db.ForeignKey('subject.id'))
    tech_class = db.Column(db.Integer, db.ForeignKey('class.id'))


    def __repr__(self):
        return 'Lecture {}'.format(self.title)


class Worker(db.Model):
    __searchable__ = ['worker_name', 'worker_address']
    
    id = db.Column(db.Integer, primary_key=True)
    worker_name = db.Column(db.String(64))
    worker_address = db.Column(db.String(128))
    worker_contact = db.Column(db.String(64))
    join_date = db.Column(db.DateTime, default=datetime.utcnow())
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Worker {}'.format(self.worker_name)


class LeaveWorker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leave_worker_name = db.Column(db.String(64))
    leave_worker_address = db.Column(db.String(128))
    leave_worker_contact = db.Column(db.String(64))
    leave_date = db.Column(db.DateTime, default=datetime.utcnow())
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Leave Worker {}'.format(self.leave_worker_name)

'''

class MyAdminIndexViewView(AdminIndexView):

    def is_accessible(self):
        
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('admin_login'))
        
admin = Admin(app, template_mode='bootstrap3', index_view=MyAdminIndexViewView())

'''



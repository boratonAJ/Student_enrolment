# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from sqlalchemy import Column, Integer, DateTime

class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    lecturer_id =  db.Column(db.Integer, db.ForeignKey('lecturers.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(150))
    faculty_name = db.Column(db.String(60), index=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offers.id'))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200), index=True)
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class Course(db.Model):
    """
    Create a Course table
    """

    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(150))
    offer_id = db.Column(db.Integer, db.ForeignKey('offers.id'))
    include_id = db.Column(db.Integer, db.ForeignKey('includes.id'))
    enrolment_id = db.Column(db.Integer, db.ForeignKey('enrolments.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


    def __repr__(self):
        return '<Course: {}>'.format(self.course_name)

class Enrolment(db.Model):
    """
    Create a Enrolment table
    """

    __tablename__ = 'enrolments'

    id = db.Column(db.Integer, primary_key=True)
    year_enrol = db.Column(db.String(60))
    students = db.relationship('Student', backref='enrolment',
                                lazy='dynamic')
    courses = db.relationship('Course', backref='enrolment',
                                lazy='dynamic')

    def __repr__(self):
        return '<Enrolment: {}>'.format(self.year_enrol)

class Include(db.Model):
    """
    Create a Include table
    """

    __tablename__ = 'includes'

    id = db.Column(db.Integer, primary_key=True)
    term_enrol = db.Column(db.String(60), index=True)
    modules = db.relationship('Module', backref='include',
                                lazy='dynamic')
    courses = db.relationship('Course', backref='include',
                                lazy='dynamic')

    def __repr__(self):
        return '<Include: {}>'.format(self.term_enrol)

class Student(db.Model):
    """
    Create a Student table
    """

    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_fname = db.Column(db.String(60))
    student_lname = db.Column(db.String(60))
    student_number = db.Column(db.Integer)
    contact_mobile = db.Column(db.String(60))
    contact_email = db.Column(db.String(60))
    enrolment_id = db.Column(db.Integer, db.ForeignKey('enrolments.id'))
    take_id = db.Column(db.Integer, db.ForeignKey('takes.id'))
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))

    def __repr__(self):
        return '<Student: {}>'.format(self.student_fname)

class Module(db.Model):
    """
    Create a Student table
    """

    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(60))
    description = db.Column(db.String(150))
    Year_completed = db.Column(db.Integer)
    take_id = db.Column(db.Integer, db.ForeignKey('takes.id'))
    teach_id = db.Column(db.Integer, db.ForeignKey('teaches.id'))
    include_id = db.Column(db.Integer, db.ForeignKey('includes.id'))

    def __repr__(self):
        return '<Module: {}>'.format(self.module_name)

class Offer(db.Model):
    """
    Create a Offer table
    """

    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    offer_year = db.Column(db.Integer)
    departments = db.relationship('Department', backref='offer',
                                lazy='dynamic')
    courses = db.relationship('Course', backref='offer',
                                lazy='dynamic')

    def __repr__(self):
        return '<Offer: {}>'.format(self.offer_year)



class Take(db.Model):
    """
    Create a Take table
    """

    __tablename__ = 'takes'

    id = db.Column(db.Integer, primary_key=True)
    students = db.relationship('Student', backref='take',
                                lazy='dynamic')
    modules = db.relationship('Module', backref='take',
                                lazy='dynamic')

    def __repr__(self):
        return '<Take: {}>'.format(self.id)

class Tutor(db.Model):
    """
    Create a Tutor table
    """

    __tablename__ = 'tutors'

    id = db.Column(db.Integer, primary_key=True)
    tut_description = db.Column(db.String(150))
    students = db.relationship('Student', backref='tutor',
                                lazy='dynamic')
    lecturers = db.relationship('Lecturer', backref='tutor',
                                lazy='dynamic')

    def __repr__(self):
        return '<Tutor: {}>'.format(self.students)

class Lecturer(db.Model):
    """
    Create a Student table
    """
    __tablename__ = 'lecturers'

    id = db.Column(db.Integer, primary_key=True)
    lecturer_fname = db.Column(db.String(60))
    lecturer_lname = db.Column(db.String(60))
    Year_joined = db.Column(db.Integer)
    contact_mobile = db.Column(db.Integer)
    contact_email = db.Column(db.String(60))
    teach_id = db.Column(db.Integer, db.ForeignKey('teaches.id'))
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))
    employees = db.relationship('Employee', backref='lecturer',
                                  lazy='dynamic')

    def __repr__(self):
        return '<Lecturer: {}>'.format(self.lecturer_fname)

class Teach(db.Model):
    """
    Create a Tutor table
    """

    __tablename__ = 'teaches'

    id = db.Column(db.Integer, primary_key=True)
    teach_date = db.Column(db.String(60))
    modules = db.relationship('Module', backref='teach',
                              lazy='dynamic')
    lecturers = db.relationship('Lecturer', backref='teach',
                                lazy='dynamic')

    def __repr__(self):
        return '<Tutor: {}>'.format(self.teach_date)

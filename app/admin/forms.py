# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, IntegerField, DateTimeField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Department, Role, Student

class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')


class StudentForm(FlaskForm):
    """
    Form for student to add or edit a department
    """
    student_fname = StringField('First Name', validators=[DataRequired()])
    student_lname = StringField('Last Name_lname', validators=[DataRequired()])
    student_number = IntegerField('Student Number', validators=[DataRequired()])
    contact_mobile = IntegerField('Mobile Line', validators=[DataRequired()])
    contact_email = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CourseForm(FlaskForm):
    """
    Form for admin to assign students to a course for a given year
    """
    student = QuerySelectField(query_factory=lambda: Student.query.all(),
                                  get_label="student_number")
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')

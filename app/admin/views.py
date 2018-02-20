# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from . import admin
from .. import db
from forms import DepartmentForm, EmployeeAssignForm, RoleForm, StudentForm, CourseForm
from ..models import Department, Employee, Role, Student, Course


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Department Views

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")

@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")

# Role Views

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


# Employee Views

@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')

@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')



# existing code remains

# Student Views

@admin.route('/students')
@login_required
def list_students():
    check_admin()
    """
    List all students
    """
    students = Student.query.all()
    return render_template('admin/students/students.html',
                           students=students, title='Students')

@admin.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    """
    Add a student to the database
    """
    check_admin()

    add_student = True

    form = StudentForm()
    if form.validate_on_submit():
        student = Student(student_fname=form.student_fname.data,student_lname=form.student_lname.data,
                          student_number=form.student_number.data, contact_mobile=form.contact_mobile.data, contact_email=form.contact_email.data)

        try:
            # add student to the database
            db.session.add(student)
            db.session.commit()
            flash('You have successfully added a new student.')
        except:
            # in case student name already exists
            flash('Error: student name already exists.')

        # redirect to the students page
        return redirect(url_for('admin.list_students'))

    # load student template
    return render_template('admin/students/student.html', add_student=add_student,
                           form=form, title='Add Student')

@admin.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    """
    Edit a student
    """
    check_admin()

    add_student = False

    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.student_fname = form.student_fname.data
        student.student_lname = form.student_fname.data
        student.student_number = form.student_number.data
        student.contact_mobile = form.contact_mobile.data
        student.contact_email = form.contact_email.data
        db.session.add(student)
        db.session.commit()
        flash('You have successfully edited the student.')

        # redirect to the students page
        return redirect(url_for('admin.list_students'))

    form.contact_email.data = student.contact_email
    form.contact_mobile.data = student.contact_mobile
    form.student_number.data = student.student_number
    form.student_fname.data = student.student_lname
    form.student_fname.data = student.student_fname
    return render_template('admin/students/student.html', add_student=add_student,
                           form=form, title="Edit Student")

@admin.route('/students/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_student(id):
    """
    Delete a student from the database
    """
    check_admin()

    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('You have successfully deleted the student.')

    # redirect to the students page
    return redirect(url_for('admin.list_students'))

    return render_template(title="Delete Student")


# Course Views

@admin.route('/courses')
@login_required
def list_courses():
    """
    List all courses
    """
    check_admin()

    courses = Course.query.all()
    return render_template('admin/courses/courses.html',
                           courses=courses, title='Courses')

@admin.route('/courses/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_course(id):
    """
    Assign a student to a course for a given year
    """
    check_admin()

    course = Course.query.get_or_404(id)

    # prevent admin from being assigned a course
    if course.is_admin:
        abort(403)

    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.department = form.department.data
        course.role = form.role.data
        course.student = form.student.data
        course.enrolment = form.enrolment.data
        db.session.add(course)
        db.session.commit()
        flash('You have successfully assigned a student, department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_courses'))

    return render_template('admin/courses/course.html',
                           course=course, form=form,
                           title='Assign Course')
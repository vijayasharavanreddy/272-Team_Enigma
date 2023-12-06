import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()  # Create a Bcrypt instance

class HRUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(80), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Employee(db.Model):
    __tablename__ = 'employees'  # Ensure this matches the actual table name in your database

    emp_no = db.Column(db.Integer, primary_key=True)
    birth_date = db.Column(db.Date, nullable=False)
    first_name = db.Column(db.String(14), nullable=False)
    last_name = db.Column(db.String(16), nullable=False)
    gender = db.Column(db.Enum('M', 'F'), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.emp_no,
            'first_name': self.first_name,
            'last_name': self.last_name,
            # Add other fields you want to include
        }

class Department(db.Model):
    __tablename__ = 'departments'
    dept_no = db.Column(db.String(4), primary_key=True)
    dept_name = db.Column(db.String(40), nullable=False)
    managers = db.relationship('Dept_Manager', cascade='all, delete-orphan')
    employees = db.relationship('Dept_Emp', cascade='all, delete-orphan')

class Dept_Emp(db.Model):
    __tablename__ = 'dept_emp'
    emp_no = db.Column(db.Integer, db.ForeignKey('employees.emp_no'), primary_key=True)
    dept_no = db.Column(db.String(4), db.ForeignKey('departments.dept_no'), primary_key=True)
    # Add other columns as necessary, such as from_date and to_date
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)

    department = db.relationship('Department', backref='dept_emps')

class Title(db.Model):
    __tablename__ = 'titles'  # Replace with your actual table name

    # Assuming 'emp_no', 'title', 'from_date', and 'to_date' are the columns in your table
    emp_no = db.Column(db.Integer, db.ForeignKey('employees.emp_no'), primary_key=True)
    title = db.Column(db.String(50), primary_key=True)  # Adjust the type and length as needed
    from_date = db.Column(db.Date, primary_key=True)
    to_date = db.Column(db.Date)

    # Relationship to the Employee model, if you have one
    employee = db.relationship('Employee', backref='titles')

    # Add other columns if necessary

class Salary(db.Model):
    __tablename__ = 'salaries'  # Replace with your actual table name

    emp_no = db.Column(db.Integer, db.ForeignKey('employees.emp_no'), primary_key=True)
    salary = db.Column(db.Integer, nullable=False)
    from_date = db.Column(db.Date, primary_key=True)
    to_date = db.Column(db.Date)

    employee = db.relationship('Employee', backref='salaries')

class Dept_Manager(db.Model):
    __tablename__ = 'dept_manager'  # Replace with your actual table name

    emp_no = db.Column(db.Integer, db.ForeignKey('employees.emp_no'), primary_key=True)
    dept_no = db.Column(db.String(4), db.ForeignKey('departments.dept_no'), primary_key=True)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)

    # Relationships
    employee = db.relationship('Employee', backref='dept_manager')
    department = db.relationship('Department', backref='dept_manager')

class HRRequest(db.Model):
    __tablename__ = 'hr_request'

    req_type = db.Column(db.String(10), primary_key=True)
    first_name = db.Column(db.String(14), primary_key=True)
    last_name = db.Column(db.String(16), primary_key=True)
    hire_status = db.Column(db.Integer, primary_key=True)
    hire_date = db.Column(db.Date)
    dept_no = db.Column(db.String(4), nullable=False)
    manager_no = db.Column(db.Integer)
    title = db.Column(db.String(50))
    salary = db.Column(db.Integer)

    def __init__(self, req_type, first_name, last_name, hire_status, dept_no, manager_no=None, title=None, salary=None, hire_date=None):
        self.req_type = req_type
        self.first_name = first_name
        self.last_name = last_name
        self.hire_status = hire_status
        self.dept_no = dept_no
        self.manager_no = manager_no
        self.title = title
        self.salary = salary
        self.hire_date = hire_date

    def __repr__(self):
        return f'<HRRequest {self.dept_no} {self.first_name} {self.last_name} {self.req_type} {self.title}>'


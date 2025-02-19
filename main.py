import random
import string
from datetime import datetime

from flask import Flask, request, jsonify
from sqlalchemy import func, desc, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from functools import wraps

from models import db, HRUser, Title, Salary, Dept_Manager, HRRequest, ManagerRequest
from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, HRUser, Employee, Department, Dept_Emp
from flask_bcrypt import Bcrypt
from flask import Flask
# from flask_session import Session
import os
from werkzeug.security import check_password_hash

# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://vijay:vijayasharavan%40@localhost/hrdata'
app.config['SECRET_KEY'] = 'p9Bv<3Eid9%$i01'  # Replace with a real secret key
app.config['SERVER_START_IDENTIFIER'] = os.urandom(24)  # Configure session to use the file system
# session = Session()
# Session(app)

db.init_app(app)
bcrypt = Bcrypt()
bcrypt.init_app(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def check_server_restart():
    if 'server_start_identifier' in session:
        if session['server_start_identifier'] != app.config['SERVER_START_IDENTIFIER']:
            # Clear the session if the identifier doesn't match
            session.clear()


class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role


from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


@login_manager.user_loader
def user_loader(user_id):
    user = db.session.get(HRUser, int(user_id))
    if user:
        user_model = User(user.id, user.role)
        user_model.id = user.id
        return user_model
    return None


def hr_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(".................", current_user, ".............")
        if not current_user.is_authenticated or current_user.role != 'hr':
            flash("You don't have permission to access the previous page.")
            return redirect(url_for('logout'))  # Redirect to login or another appropriate page
        return f(*args, **kwargs)

    return decorated_function


def hr_or_manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(".................", current_user, ".............")
        if not current_user.is_authenticated or current_user.role != 'hr' or current_user.role != 'manager':
            flash("You don't have permission to access the previous page.")
            return redirect(url_for('logout'))  # Redirect to login or another appropriate page
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session['server_start_identifier'] = app.config['SERVER_START_IDENTIFIER']
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check for user with the given username
        user = HRUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            user_model = User(user.id, user.role)
            user_model.id = user.id
            login_user(user_model)

            # Redirect based on the user's role
            if user.role == 'manager':
                return redirect(url_for('dashboard_mgr', mgr_no=user_model.id))
            elif user.role == 'employee':
                return redirect(url_for('dashboard_emp', emp_no=user_model.id))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. If you do not have an account, please register.')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        mobile_number = request.form['mobile_number']
        password = request.form['password']

        existing_user = HRUser.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = HRUser(
                username=username,
                first_name=first_name,
                last_name=last_name,
                address=address,
                email=email,
                mobile_number=mobile_number,
                role='manager'
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists')
    return render_template('register.html')


@app.route('/dashboard')
@hr_required
@login_required
def dashboard():
    user = db.session.get(HRUser, int(current_user.id))
    return render_template('dashboard.html', first_name=user.first_name)


@app.route('/my_profile_mgr', methods=['GET', 'POST'])
@login_required
def my_profile():
    if not request.is_json:
        return jsonify({'error': 'Invalid request format'}), 400

    data = request.get_json()
    user_id = current_user.id

    # Fetch HRUser and Employee by user_id and their names
    user = db.session.get(HRUser, int(user_id))
    employee = Employee.query.filter_by(first_name=user.first_name, last_name=user.last_name).first()

    if user and employee:
        # Update HRUser
        user.first_name = data['first_name']
        user.last_name = data['last_name']

        # Update Employee
        employee.first_name = data['first_name']
        employee.last_name = data['last_name']
        employee.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        employee.gender = data['gender']

        # Commit changes to the database
        db.session.commit()
        return jsonify({'success': 'Profile updated successfully'}), 200
    else:
        return jsonify({'error': 'User or Employee not found'}), 404


@app.route('/dashboard_mgr')
@login_required
def dashboard_mgr():
    user = db.session.get(HRUser, int(current_user.id))
    employee = Employee.query.filter_by(first_name=user.first_name, last_name=user.last_name).first()
    dept_no = "d001"

    if employee:
        dept_manager = Dept_Manager.query.filter_by(emp_no=employee.emp_no).first()
        if dept_manager:
            dept_no = dept_manager.dept_no
            department = Department.query.filter_by(dept_no=dept_manager.dept_no).first()
            if department:
                dept_name = department.dept_name
            else:
                dept_name = "Not a manager"
        else:
            dept_name = "Not a manager"
    else:
        dept_name = "Employee not found"

    if employee is None:
        "Error: Employee not found", 404 

    return render_template(
        'dashboard-mgr.html',
        employee=employee,
        first_name=employee.first_name if employee else "N/A",
        dept_name=dept_name if dept_name else "N/A"
    )


@app.route('/approvals_count')
@login_required
def get_approval_count():
    count = HRRequest.query.filter_by(hire_status=0).count()
    return jsonify({'count': count})


@app.route('/dashboard_emp')
@login_required
def dashboard_emp():
    user = db.session.get(HRUser, int(current_user.id))
    employee = Employee.query.filter_by(first_name=user.first_name, last_name=user.last_name).first()
    dept_no = "d001"

    if employee:
        dept_emp = Dept_Emp.query.filter_by(emp_no=employee.emp_no).first()
        if dept_emp:
            dept_no = dept_emp.dept_no
            department = Department.query.filter_by(dept_no=dept_emp.dept_no).first()
            if department:
                dept_name = department.dept_name
            else:
                dept_name = "Not a Current Employee"
        else:
            dept_name = "Not a Current Employee"
    else:
        dept_name = "Employee not found"

    return render_template('dashboard_emp.html', employee=employee, first_name=employee.first_name, dept_name=dept_name,
                           dept_no=dept_no, mgr_no=employee.emp_no)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# @app.before_first_request
# def clear_session_on_restart():
#     if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
#         with app.app_context():
#             session.clear()

@app.route('/employee_history/<int:emp_no>')
@login_required
def employee_history(emp_no):
    # Fetch salary history
    salary_history_result = db.session.execute(
        text("SELECT salary, from_date, to_date FROM salaries WHERE emp_no = :emp_no"),
        {'emp_no': emp_no}
    ).fetchall()
    salary_history = [{'salary': row[0], 'from_date': row[1], 'to_date': row[2]} for row in salary_history_result]

    # Fetch title history
    title_history_result = db.session.execute(
        text("SELECT title, from_date, to_date FROM titles WHERE emp_no = :emp_no"),
        {'emp_no': emp_no}
    ).fetchall()
    title_history = [{'title': row[0], 'from_date': row[1], 'to_date': row[2]} for row in title_history_result]

    # Fetch department history
    dept_history_result = db.session.execute(
        text("SELECT dept_no, from_date, to_date FROM dept_emp WHERE emp_no = :emp_no"),
        {'emp_no': emp_no}
    ).fetchall()
    dept_history = [{'dept_no': row[0], 'from_date': row[1], 'to_date': row[2]} for row in dept_history_result]

    # Return JSON response
    return jsonify({
        'salary_history': salary_history,
        'title_history': title_history,
        'dept_history': dept_history
    })

@app.route('/employee_history_loader/<int:emp_no>')
@login_required
def employee_history_loader(emp_no):
    # Render the template and pass emp_no to it
    return render_template('employee_history.html', emp_no=emp_no)


@app.route('/employees')
@hr_required
@login_required
def employees():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    sort_by = request.args.get('sort_by', 'emp_no')  # Default sort column
    sort_direction = request.args.get('direction', 'asc')  # Default sort direction
    only_managers = request.args.get('onlyManagers', 'false') == 'true'
    search = request.args.get('search', '')

    # Define a subquery that gets the latest title per employee
    title_subquery = db.session.query(
        Title.emp_no.label('emp_no'),
        func.max(Title.from_date).label('max_date')
    ).group_by(Title.emp_no).subquery()

    # Define the main query with a left join on the title subquery
    query = db.session.query(
        Employee.emp_no,
        Employee.first_name,
        Employee.last_name,
        Employee.gender,
        Employee.hire_date,
        Department.dept_name,
        Title.title
    ).join(Dept_Emp, Employee.emp_no == Dept_Emp.emp_no) \
        .join(Department, Dept_Emp.dept_no == Department.dept_no) \
        .outerjoin(title_subquery, Employee.emp_no == title_subquery.c.emp_no) \
        .outerjoin(Title, db.and_(Employee.emp_no == Title.emp_no, title_subquery.c.max_date == Title.from_date))

    # If "Only Managers" is selected, add a filter for manager titles
    if only_managers:
        query = query.filter(Title.title.ilike('%manager%'))

    # Apply sorting
    if sort_by == 'dept_name':
        order = Department.dept_name.desc() if sort_direction == 'desc' else Department.dept_name.asc()
    else:
        order = db.desc(getattr(Employee, sort_by)) if sort_direction == 'desc' else getattr(Employee, sort_by)
    query = query.order_by(order)

    # Apply search filter
    if search:
        query = query.filter(Employee.first_name.like(f'%{search}%') | Employee.last_name.like(f'%{search}%'))

    # Distinct to prevent duplicates and then order and paginate
    query = query.distinct(Employee.emp_no)

    paginated_employees = query.paginate(page=page, per_page=per_page, error_out=False)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('partials/_employees_table_body.html', employees=paginated_employees.items,
                               pagination=paginated_employees, only_managers_state='true' if only_managers else 'false')

    return render_template('employees.html', employees=paginated_employees.items, pagination=paginated_employees,
                           only_managers_state='true' if only_managers else 'false')


@app.route('/get_manager_requests/<int:emp_no>')
@login_required
def get_manager_requests(emp_no):
    try:
        # Fetch manager_requests for the specified emp_no
        manager_requests = ManagerRequest.query.filter_by(assignee=emp_no, task_status=0).all()
        manager_requests_data = []

        for request in manager_requests:
            manager_requests_data.append({
                'id': request.id,
                'title': request.task_name,
                'description': request.description,
                'task_status': request.task_status,
                'deadline': request.deadline,
                'assignee': request.assignee
            })

        return jsonify(manager_requests_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/employees_mgr')
# @hr_or_manager_required
@login_required
def employees_mgr():
    dept_no = request.args.get('dept_no')
    manager_no = request.args.get('mgr_no')
    page = request.args.get('page', 1, type=int)
    per_page = 10  # You can change this number to show more/less items per page
    search = request.args.get('search', '')

    # Query to fetch employees in the specified department with pagination
    query = db.session.query(
        Employee.emp_no,
        Employee.first_name,
        Employee.last_name,
        Employee.gender,
        Employee.birth_date,
        Employee.hire_date
    ).join(Dept_Emp, Employee.emp_no == Dept_Emp.emp_no) \
        .filter(Dept_Emp.dept_no == dept_no, Dept_Emp.to_date > datetime.now())

    if search:
        query = query.filter(db.or_(
            Employee.first_name.ilike(f'%{search}%'),
            Employee.last_name.ilike(f'%{search}%')
        ))

    employees = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('employees-mgr.html', employees=employees, dept_no=dept_no, mgr_no=manager_no)


@login_required
@app.route('/get_employee_data/<int:emp_no>')
def get_employee_data(emp_no):
    # Subquery to get the latest title
    latest_title_subquery = db.session.query(
        Title.emp_no,
        Title.title,
        func.rank().over(
            partition_by=Title.emp_no,
            order_by=(desc(Title.from_date), desc(Title.to_date))
        ).label('rnk')
    ).subquery()

    # Subquery to get the latest salary
    latest_salary_subquery = db.session.query(
        Salary.emp_no,
        Salary.salary,
        func.rank().over(
            partition_by=Salary.emp_no,
            order_by=desc(Salary.from_date)
        ).label('rnk')
    ).filter(Salary.emp_no == emp_no).subquery()

    # Main query joining with the subquery
    employee_data = db.session.query(
        Employee.emp_no,
        Employee.first_name,
        Employee.last_name,
        Department.dept_name,
        Dept_Emp.dept_no,
        latest_title_subquery.c.title,
        latest_salary_subquery.c.salary
    ).join(Dept_Emp, Employee.emp_no == Dept_Emp.emp_no) \
        .join(Department, Dept_Emp.dept_no == Department.dept_no) \
        .outerjoin(latest_title_subquery, Employee.emp_no == latest_title_subquery.c.emp_no) \
        .outerjoin(latest_salary_subquery, Employee.emp_no == latest_salary_subquery.c.emp_no) \
        .filter(Employee.emp_no == emp_no, latest_title_subquery.c.rnk == 1, latest_salary_subquery.c.rnk == 1) \
        .first()

    if employee_data:
        return jsonify({
            'emp_no': employee_data.emp_no,
            'first_name': employee_data.first_name,
            'last_name': employee_data.last_name,
            'dept_name': employee_data.dept_name,
            'dept_no': employee_data.dept_no,
            'title': employee_data.title,
            'salary': employee_data.salary
        })
    else:
        return jsonify({'error': 'Employee not found'}), 404


@login_required
@app.route('/update_employee/<int:emp_no>', methods=['POST'])
def update_employee(emp_no):
    data = request.get_json()
    employee = Employee.query.get(emp_no)
    if employee:
        employee.first_name = data['first_name']
        employee.last_name = data['last_name']
        # Update other fields...

        # Update department if it's different
        # Update department
        new_dept_no = data.get('dept_no')
        if new_dept_no:
            # Assuming you have a relationship set up between Employee and Dept_Emp
            current_dept_emp = Dept_Emp.query.filter_by(emp_no=emp_no).first()
            if current_dept_emp:
                current_dept_emp.dept_no = new_dept_no
            else:
                # Handle case where no current department relationship exists
                new_dept_emp = Dept_Emp(emp_no=emp_no, dept_no=new_dept_no)
                db.session.add(new_dept_emp)

        # Handle title update
        new_title = data.get('title')
        from_date = datetime.strptime(data.get('from_date'), '%Y-%m-%d').date()
        to_date = datetime.strptime(data.get('to_date'), '%Y-%m-%d').date()

        if new_title:
            # Look for an existing title with the same dates
            existing_title = Title.query.filter_by(emp_no=emp_no, from_date=from_date, to_date=to_date).first()
            if existing_title:
                existing_title.title = new_title  # Update the existing record
            else:
                # No existing title with the same dates, create a new record
                new_title_entry = Title(emp_no=emp_no, title=new_title, from_date=from_date, to_date=to_date)
                db.session.add(new_title_entry)

                # Handle salary update
        new_salary = data.get('new_salary')
        if new_salary:
            # Look for an existing salary with the same dates
            existing_salary = Salary.query.filter_by(emp_no=emp_no, from_date=from_date,
                                                     to_date=to_date).first()
            if existing_salary:
                existing_salary.salary = new_salary  # Update the existing record
            else:
                # No existing salary with the same dates, create a new record
                new_salary_entry = Salary(emp_no=emp_no, salary=new_salary, from_date=from_date,
                                          to_date=to_date)
                db.session.add(new_salary_entry)

            # Commit changes to the database
        try:
            db.session.commit()
            return jsonify({'success': 'Employee updated'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Employee not found'}), 404


@login_required
@app.route('/api/search_employees')
def search_employees():
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    # Implement search logic and paginate results
    employees = Employee.query.filter(Employee.first_name.ilike(f'%{query}%')).paginate(page=page, per_page=per_page,
                                                                                        error_out=False)
    return jsonify({
        'employees': [employee.to_dict() for employee in employees.items],
        'has_more': employees.has_next
    })


@app.route('/pending_approvals')
@login_required
def pending_approvals():
    pending_requests = HRRequest.query.filter_by(hire_status=0).all()
    data = [{
        'dept_no': request.dept_no,
        'first_name': request.first_name,
        'last_name': request.last_name,
        'hire_date': request.hire_date.strftime('%Y-%m-%d'),
        'manager_no': request.manager_no,
        'title': request.title,
        'salary': request.salary,
        'req_type': request.req_type
    } for request in pending_requests]

    return jsonify(data)


@app.route('/approve_employee', methods=['POST'])
def approve_employee():
    data = request.get_json()

    # Check if the request exists
    hr_request = HRRequest.query.filter_by(first_name=data['first_name'], last_name=data['last_name'],
                                           hire_status=0).first()
    if hr_request is None:
        return jsonify({'error': 'Request not found'}), 404

    # Update hire_status in hr_request
    hr_request.hire_status = 1

    if hr_request.req_type == "newhire":

        # Generate a unique employee number
        while True:
            emp_no = random.randint(600000, 999999)  # Adjust range as per your ID scheme
            existing_employee = Employee.query.filter_by(emp_no=emp_no).first()
            if not existing_employee:
                break

        # Create new employee
        new_employee = Employee(
            emp_no=emp_no,
            birth_date=datetime(datetime.now().year - 24, 1, 1),  # Adjust date as needed
            first_name=data['first_name'],
            last_name=data['last_name'],
            gender='M',  # Adjust gender as needed
            hire_date=datetime.now().strftime('%Y-%m-%d')
        )
        db.session.add(new_employee)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

        # Create dept_emp entry
        new_dept_emp = Dept_Emp(
            emp_no=emp_no,
            dept_no=data['dept_no'],
            from_date=datetime.now().strftime('%Y-%m-%d'),
            to_date=datetime(datetime.now().year + 2, 1, 1).strftime('%Y-%m-%d')  # Set to_date as per your logic
        )
        db.session.add(new_dept_emp)

        new_salary = Salary(
            emp_no=emp_no,
            salary=data['salary'],
            from_date=datetime.now().strftime('%Y-%m-%d'),
            to_date=datetime(datetime.now().year + 2, 1, 1).strftime('%Y-%m-%d')  # Set to_date as per your logic
        )
        db.session.add(new_salary)

    elif hr_request.req_type == 'terminate':
        # Logic for terminate
        # Find employee number from first and last name
        employee = Employee.query.filter_by(first_name=data['first_name'], last_name=data['last_name']).first()
        if employee:
            # Delete the specific dept_emp entry for this employee
            Dept_Emp.query.filter_by(emp_no=employee.emp_no, dept_no=data['dept_no']).delete()
            # Also, delete the employee record
            Employee.query.filter_by(emp_no=employee.emp_no).delete()

    elif hr_request.req_type == 'promote':
        employee = Employee.query.filter_by(first_name=data['first_name'], last_name=data['last_name']).first()

        if employee:
            # Update salary and title
            Salary.query.filter_by(emp_no=employee.emp_no).update({'salary': data['salary']})
            Title.query.filter_by(emp_no=employee.emp_no).update({'title': data['title']})

    try:
        db.session.commit()
        return jsonify({'message': f'Employee {hr_request.req_type} request processed successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/decline_employee', methods=['PUT', "POST", "DELETE"])
def decline_employee():
    data = request.get_json()

    hr_request = HRRequest.query.filter_by(first_name=data['first_name'], last_name=data['last_name'],
                                           hire_status=0).first()
    if hr_request is None:
        return jsonify({'error': 'Request not found'}), 404

    # Update hire_status to 2 (declined)
    hr_request.hire_status = 2

    try:
        db.session.commit()
        return jsonify({'message': 'Employee decline processed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/promote_employee', methods=['POST'])
def promote_employee():
    data = request.json
    new_title = data.get('title')
    dept_no = data.get('dept_no')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    hire_date = data.get('hire_date')
    manager_no = data.get('manager_no')
    salary = data.get('salary')

    try:
        # Create a new HRRequest object
        hr_request = HRRequest(
            dept_no=dept_no,  # Replace with actual data
            first_name=first_name,  # Replace with actual data
            last_name=last_name,  # Replace with actual data
            hire_date=hire_date,  # Replace with actual data
            manager_no=manager_no,  # Replace with actual data
            title=new_title,
            salary=salary,  # Replace with actual data
            req_type='promote',
            hire_status=0
        )
        db.session.add(hr_request)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'success', 'message': 'Promotion request sent to HR'})


@app.route('/terminate_employee', methods=['POST'])
@login_required
def terminate_employee():
    data = request.get_json()
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    dept_no = data.get('dept_no')
    mgr_no = data.get('mgr_no')

    emp_entry = Employee.query.filter_by(first_name=first_name, last_name=last_name).first()
    if emp_entry is None:
        return jsonify({'error': 'Request not found'}), 404

    emp_no = emp_entry.emp_no
    title_entry = Title.query.filter_by(emp_no=emp_no).first()
    title = "Unknown"

    if title_entry is not None:
        title = title_entry.title

    try:
        # Create a new HRRequest object for termination
        hr_request = HRRequest(
            dept_no=dept_no,
            first_name=first_name,
            last_name=last_name,  # Replace with actual data
            hire_status=0,  # Replace with actual data
            salary=50000,
            hire_date=datetime.now(),
            manager_no=mgr_no,
            title=title,
            req_type='terminate'
        )
        db.session.add(hr_request)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'success', 'message': 'Termination request sent to HR'})


@app.route('/managers')
@login_required
def managers():
    return render_template('managers.html')

@app.route('/get_employees')
def get_employees():
    dept_no = request.args.get('dept_no')

    if not dept_no:
        return jsonify({'error': 'Department number is required'}), 400

    employees = db.session.query(Employee.emp_no, Employee.first_name, Employee.last_name)\
                          .join(Dept_Emp, Dept_Emp.emp_no == Employee.emp_no)\
                          .filter(Dept_Emp.dept_no == dept_no).all()

    employee_list = [{'id': emp.emp_no, 'name': f"{emp.first_name} {emp.last_name}"} for emp in employees]
    return jsonify(employee_list)

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json()
    deadline = data['deadline']
    if deadline:
        deadline = datetime.strptime(deadline, '%Y-%m-%d')
    else:
        deadline = None  # Handle the case where deadline is not provided

    new_task = ManagerRequest(
        task_name=data['taskName'],
        description=data['description'],
        assignee=data['assignee'],
        deadline=deadline,  # Use the processed deadline
        manager_no=data['managerNo'],
        task_status=data.get('task_status', 0)  # Assuming a default status
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task added successfully'}), 200

@app.route('/update_manager_request/<int:task_id>', methods=['POST'])
def update_manager_request(task_id):
    data = request.get_json()
    task_status = data.get('status')

    # Logic to update the task status in your database
    # Example:
    task = ManagerRequest.query.get(task_id)
    if task:
        task.task_status = task_status
        db.session.commit()
        return jsonify({'message': 'Task status updated'}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/departments/list')
@login_required
def departments_list():
    departments = Department.query.all()
    department_list = [{'dept_no': dept.dept_no, 'dept_name': dept.dept_name} for dept in departments]
    return jsonify(department_list)


@app.route('/departments')
@login_required
def departments():
    # Subquery to get the latest dept_manager entry for each department
    latest_dept_managers_subquery = db.session.query(
        Dept_Manager.dept_no,
        func.max(Dept_Manager.from_date).label('latest_from_date')
    ).group_by(Dept_Manager.dept_no).subquery()

    # Join the subquery with Department, Dept_Manager, and Employee
    departments = db.session.query(
        Department.dept_no,
        Department.dept_name,
        Dept_Manager.emp_no,
        Employee.first_name,
        Employee.last_name
    ).join(latest_dept_managers_subquery, Department.dept_no == latest_dept_managers_subquery.c.dept_no) \
        .join(Dept_Manager, (Dept_Manager.dept_no == latest_dept_managers_subquery.c.dept_no) & (
            Dept_Manager.from_date == latest_dept_managers_subquery.c.latest_from_date)) \
        .join(Employee, Dept_Manager.emp_no == Employee.emp_no) \
        .filter(Dept_Manager.to_date > datetime.now()) \
        .all()

    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('partials/_departments_table.html', departments=departments)

    return render_template('departments.html', departments=departments)


from flask import request, redirect, url_for, flash
from models import db, Department, Dept_Manager


def generate_unique_dept_no(length=3):
    while True:
        # Generate a random string
        dept_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

        # Check if this dept_no already exists in the database
        existing_dept = Department.query.filter_by(dept_no="d" + dept_no).first()
        if not existing_dept:
            return "d" + dept_no  # Unique dept_no found


@login_required
@app.route('/add_department', methods=['POST'])
def add_department():
    data = request.get_json()
    dept_name = data.get('deptName')
    dept_description = data.get('deptDescription')  # Modify as per your model
    manager_emp_no = data.get('empNo')

    # Generate a unique department number
    unique_dept_no = generate_unique_dept_no()
    print(unique_dept_no)

    # Create a new department
    new_department = Department(dept_no=unique_dept_no, dept_name=dept_name)  # Modify as per your model
    db.session.add(new_department)
    db.session.commit()

    # Assign manager to the new department
    new_dept_manager = Dept_Manager(emp_no=manager_emp_no, dept_no=new_department.dept_no, from_date=datetime.now(),
                                    to_date=datetime(datetime.now().year + 1, 1, 1))  # Modify as per your model
    db.session.add(new_dept_manager)
    db.session.commit()

    flash('New department added successfully.')
    return redirect(url_for('departments'))


@login_required
@app.route('/department_manager_history/<dept_no>', methods=['GET'])
def department_manager_history(dept_no):
    manager_history = db.session.query(
        Dept_Manager.emp_no,
        Employee.first_name,
        Employee.last_name,
        Dept_Manager.from_date,
        Dept_Manager.to_date
    ).join(Employee, Dept_Manager.emp_no == Employee.emp_no) \
        .filter(Dept_Manager.dept_no == dept_no) \
        .order_by(Dept_Manager.from_date).all()

    history_data = [{
        'emp_no': mh.emp_no,
        'name': f"{mh.first_name} {mh.last_name}",
        'from_date': mh.from_date.strftime('%Y-%m-%d'),
        'to_date': mh.to_date.strftime('%Y-%m-%d')
    } for mh in manager_history]
    print(history_data)
    return jsonify(history_data)


@login_required
@app.route('/update_department_manager', methods=['POST'])
def update_department_manager():
    data = request.get_json()
    emp_no = data.get('emp_no')
    dept_no = data.get('dept_no')
    from_date = datetime.strptime(data.get('from_date'), '%Y-%m-%d').date()
    to_date = datetime.strptime(data.get('to_date'), '%Y-%m-%d').date()

    # Check for existing dept_manager entry
    existing_dept_manager = Dept_Manager.query.filter_by(dept_no=dept_no, from_date=from_date,
                                                         to_date=to_date).first()

    if existing_dept_manager:
        # Update existing entry
        existing_dept_manager.emp_no = emp_no  # This might be redundant
    else:
        # Create new entry
        new_dept_manager = Dept_Manager(emp_no=emp_no, dept_no=dept_no, from_date=from_date, to_date=to_date)
        db.session.add(new_dept_manager)

    # Check for existing dept_emp entry
    existing_dept_emp = Dept_Emp.query.filter_by(dept_no=dept_no, from_date=from_date,
                                                 to_date=to_date).first()

    if existing_dept_emp:
        # Update existing entry
        existing_dept_emp.emp_no = emp_no  # This might be redundant
    else:
        # Create new entry
        new_dept_emp = Dept_Emp(emp_no=emp_no, dept_no=dept_no, from_date=from_date, to_date=to_date)
        db.session.add(new_dept_emp)

    # Commit the changes to the database
    try:
        db.session.commit()
        return jsonify({'message': 'Department manager updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Flask route example
@app.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.get_json()

    try:
        # Start a database transaction
        db.session.begin()

        # Generate a unique employee number
        while True:
            emp_no = random.randint(600000, 999999)  # Adjust range as per your ID scheme
            if not Employee.query.filter_by(emp_no=emp_no).first():
                break

        # Create new employee
        new_employee = Employee(
            emp_no=emp_no,
            birth_date=datetime(datetime.now().year - 24, 1, 1),  # Adjust date as needed
            first_name=data['first_name'],
            last_name=data['last_name'],
            gender='M',  # Adjust gender as needed
            hire_date=datetime.now().strftime('%Y-%m-%d')
        )
        db.session.add(new_employee)

        # Commit the employee record to ensure it's in the database before proceeding
        db.session.commit()

        # Now that the employee is committed, add entries to dept_emp and salary
        new_dept_emp = Dept_Emp(
            emp_no=emp_no,
            dept_no=data['dept_no'],
            from_date=datetime.now().strftime('%Y-%m-%d'),
            to_date=datetime(datetime.now().year + 2, 1, 1).strftime('%Y-%m-%d')
        )
        db.session.add(new_dept_emp)

        new_salary = Salary(
            emp_no=emp_no,
            salary=data['salary'],
            from_date=datetime.now().strftime('%Y-%m-%d'),
            to_date=datetime(datetime.now().year + 2, 1, 1).strftime('%Y-%m-%d')
        )
        db.session.add(new_salary)

        # Commit the remaining changes
        db.session.commit()
        return jsonify({'message': 'Employee added successfully'}), 200

    except SQLAlchemyError as e:
        # Roll back the transaction in case of an error
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@login_required
@app.route('/delete/department/<dept_no>', methods=['DELETE'])
def delete_department(dept_no):
    # Delete related records in dept_manager and dept_emp
    Dept_Manager.query.filter_by(dept_no=dept_no).delete()
    Dept_Emp.query.filter_by(dept_no=dept_no).delete()

    # Now delete the department
    department = Department.query.get(dept_no)
    if department:
        db.session.delete(department)
        db.session.commit()
        return "Department deleted successfully"
    else:
        return "Department not found"


@app.route('/department_histogram')
@login_required
def department_histogram():
    # SQL query to count the number of employees in each department
    department_counts = db.session.query(
        Department.dept_name,
        func.count(Dept_Emp.emp_no).label('employee_count')
    ).join(Dept_Emp, Department.dept_no == Dept_Emp.dept_no) \
        .group_by(Department.dept_name) \
        .all()

    # Prepare data for the histogram
    dept_names = [dept[0] for dept in department_counts]
    emp_counts = [dept[1] for dept in department_counts]

    return jsonify(department_names=dept_names, employee_counts=emp_counts)


@app.route('/salary_ranges_pie_chart')
@login_required
def salary_ranges_pie_chart():
    # Define your salary ranges
    ranges = [(0, 30000), (30000, 60000), (60000, 90000), (90000, 120000), (120000, 300000)]
    range_labels = ["0-30k", "30k-60k", "60k-90k", "90-120k", ">120k"]
    counts = []

    for salary_range in ranges:
        count = db.session.query(func.count(Salary.emp_no)).filter(
            Salary.salary >= salary_range[0],
            Salary.salary < salary_range[1]
        ).scalar()
        counts.append(count)

    return jsonify(labels=range_labels, data=counts)


@app.route('/add_hr_request', methods=['POST'])
@login_required
def add_hr_request():
    data = request.get_json()
    try:
        new_request = HRRequest(
            dept_no=data['dept_no'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            hire_date=datetime.strptime(data['hire_date'], '%Y-%m-%d').date(),
            manager_no=data['manager_no'],
            title=data['title'],
            salary=50000,
            hire_status=data['hire_status'],
            req_type=data['req_type']
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'New hire request added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

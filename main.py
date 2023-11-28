from datetime import datetime

from flask import Flask, request, jsonify
from sqlalchemy import func, desc
from sqlalchemy.orm import aliased

from models import db, HRUser, Title, Salary, Dept_Manager
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/employees'
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
    pass

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
    user = HRUser.query.get(int(user_id))
    if user:
        user_model = User()
        user_model.id = user.id
        return user_model
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    session['server_start_identifier'] = app.config['SERVER_START_IDENTIFIER']
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = HRUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            user_model = User()
            user_model.id = user.id
            login_user(user_model)
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
                mobile_number=mobile_number
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
@login_required
def dashboard():
    user = HRUser.query.get(current_user.id)
    return render_template('dashboard.html', first_name=user.first_name)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# @app.before_first_request
# def clear_session_on_restart():
#     if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
#         with app.app_context():
#             session.clear()



@app.route('/employees')
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
        return render_template('partials/_employees_table_body.html', employees=paginated_employees.items, pagination=paginated_employees, only_managers_state='true' if only_managers else 'false')

    return render_template('employees.html', employees=paginated_employees.items, pagination=paginated_employees, only_managers_state='true' if only_managers else 'false')
# from sqlalchemy import desc, func

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
    employees = Employee.query.filter(Employee.first_name.ilike(f'%{query}%')).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'employees': [employee.to_dict() for employee in employees.items],
        'has_more': employees.has_next
    })


@app.route('/managers')
@login_required
def managers():
    return render_template('managers.html')


@app.route('/departments/list')
@login_required
def departments_list():
    departments = Department.query.all()
    department_list = [{'dept_no': dept.dept_no, 'dept_name': dept.dept_name} for dept in departments]
    return jsonify(department_list)


@app.route('/departments')
@login_required
def departments():
    departments = db.session.query(
        Department.dept_no,
        Department.dept_name,
        Dept_Manager.emp_no,
        Employee.first_name,
        Employee.last_name
    ).join(Dept_Manager, Department.dept_no == Dept_Manager.dept_no) \
     .join(Employee, Dept_Manager.emp_no == Employee.emp_no) \
     .filter(Dept_Manager.to_date > datetime.now()).all()  # Assuming 'to_date' is used to determine current managers

    return render_template('departments.html', departments=departments)

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
    existing_dept_manager = Dept_Manager.query.filter_by(emp_no=emp_no, dept_no=dept_no, from_date=from_date,
                                                        to_date=to_date).first()

    if existing_dept_manager:
        # Update existing entry
        existing_dept_manager.emp_no = emp_no  # This might be redundant
    else:
        # Create new entry
        new_dept_manager = Dept_Manager(emp_no=emp_no, dept_no=dept_no, from_date=from_date, to_date=to_date)
        db.session.add(new_dept_manager)

    # Check for existing dept_emp entry
    existing_dept_emp = Dept_Emp.query.filter_by(emp_no=emp_no, dept_no=dept_no, from_date=from_date,
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


if __name__ == '__main__':
    app.run(debug=True)
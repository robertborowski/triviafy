# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -note: any pages related to authentication will be in this auth.py file
# -@login_required   # this decorator says that url cannot be accessed unless the user is logged in. 
# -@login_required: <-- This decorator will bring a user to __init__ code: [login_manager.login_view = 'auth.candidates_login_page_function'] if they hit a page that requires login and they are not logged in.
# -use code: <methods=['GET', 'POST']> when you want the user to interact with the page through forms/checkbox/textbox/radio/etc.
# ------------------------ info about this file end ------------------------


# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import CandidatesUserObj
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
# ------------------------ imports end ------------------------


# ------------------------ function start ------------------------
auth = Blueprint('auth', __name__)
# ------------------------ function end ------------------------


# ------------------------ before page variables start ------------------------
cache_busting_output = create_uuid_function('css_')
# ------------------------ before page variables end ------------------------


# ------------------------ individual route start ------------------------
@auth.route('/candidates/login', methods=['GET', 'POST'])
def candidates_login_page_function():
  localhost_print_function('=========================================== candidates_login_page_function START ===========================================')
  # ------------------------ post request sent start ------------------------
  email = request.form.get('email')
  password = request.form.get('password')
  # ------------------------ post request sent end ------------------------
  
  user = CandidatesUserObj.query.filter_by(email=email).first()
  if user:
    if check_password_hash(user.password, password):
      flash('Logged in successfully!', category='success')
      login_user(user, remember=True)
      return redirect(url_for('views.dashboard_test_login_page_function'))
    else:
      flash('Incorrect password, try again.', category='error')
  else:
    flash('Email does not exist.', category='error')

  localhost_print_function('=========================================== candidates_login_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/login_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------


# ------------------------ individual route start ------------------------
@auth.route('/candidates/logout')
@login_required
def candidates_logout_function():
  localhost_print_function('=========================================== candidates_logout_function START ===========================================')
  logout_user()
  localhost_print_function('=========================================== candidates_logout_function END ===========================================')
  return redirect(url_for('auth.candidates_login_page_function'))
# ------------------------ individual route end ------------------------


# ------------------------ individual route start ------------------------
@auth.route('/candidates/signup', methods=['GET', 'POST'])
def candidates_signup_function():
  localhost_print_function('=========================================== candidates_signup_function START ===========================================')
  if request.method == 'POST':
    # ------------------------ 2. added logic for passing along email from one page to next start ------------------------
    user_input_email = request.form.get('user_input_email')
    if user_input_email != None:
      localhost_print_function('user is being redirected to full sign up page')
      localhost_print_function('=========================================== candidates_signup_function END ===========================================')
      return render_template('candidates_page_templates/not_logged_in_page_templates/create_account_templates/index.html', user=current_user)
    # ------------------------ 2. added logic for passing along email from one page to next end ------------------------
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    companyName = request.form.get('companyName')
    departmentName = request.form.get('departmentName')

    user = CandidatesUserObj.query.filter_by(email=email).first()
    if user:
      flash('Email already exists.', category='error')
    elif len(email) < 4:
      flash('Email must be greater than 3 characters.', category='error')
    elif len(firstName) < 2:
      flash('First name must be greater than 1 character.', category='error')
    elif password1 != password2:
      flash('Passwords don\'t match.', category='error')
    elif len(password1) < 7:
      flash('Password must be at least 7 characters.', category='error')
    else:
      new_user = CandidatesUserObj(
        email=email,
        password=generate_password_hash(password1, method="sha256"),
        first_name = firstName,
        last_name = lastName,
        company_name = companyName,
        department_name = departmentName
      )
      db.session.add(new_user)
      db.session.commit()
      flash('Account created!', category='success')
      login_user(new_user, remember=True)
      localhost_print_function('=========================================== candidates_signup_function END ===========================================')
      return redirect(url_for('views.dashboard_test_login_page_function'))

  localhost_print_function('=========================================== candidates_signup_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/create_account_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------
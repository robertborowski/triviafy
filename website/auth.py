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
from website.backend.user_inputs import sanitize_email_function
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
  if request.method == 'POST':
    # ------------------------ post method hit #1 - regular login start ------------------------
    # ------------------------ post request sent start ------------------------
    ui_email = request.form.get('login_page_ui_email')
    ui_password = request.form.get('login_page_ui_password')
    # ------------------------ post request sent end ------------------------
    # ============================================================================================================
    # ============================================================================================================
    # ============================================================================================================
    # ------------------------ Sanitize: Here you have to run backend checks on all the user inputs/sanitize start ------------------------
    # ------------------------ Sanitize: Here you have to run backend checks on all the user inputs/sanitize end ------------------------
    # ============================================================================================================
    # ============================================================================================================
    # ============================================================================================================
    user = CandidatesUserObj.query.filter_by(email=ui_email).first()
    if user:
      if check_password_hash(user.password, ui_password):
        flash('Logged in successfully!', category='success')
        # ------------------------ keep user logged in start ------------------------
        login_user(user, remember=True)
        # ============================================================================================================
        # ============================================================================================================
        # ============================================================================================================
        # ------------------------ add redis code here start ------------------------
        # ------------------------ add redis code here end ------------------------
        # ============================================================================================================
        # ============================================================================================================
        # ============================================================================================================
        # ------------------------ keep user logged in end ------------------------
        return redirect(url_for('views.dashboard_test_login_page_function'))
      else:
        flash('Incorrect email/password, try again.', category='error')
    else:
      flash('Incorrect email/password, try again.', category='error')
    # ------------------------ post method hit #1 - regular login end ------------------------

  localhost_print_function('=========================================== candidates_login_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/login_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------


# ------------------------ individual route start ------------------------
@auth.route('/candidates/logout')
@login_required
def candidates_logout_function():
  localhost_print_function('=========================================== candidates_logout_function START ===========================================')
  logout_user()
  # ============================================================================================================
  # ============================================================================================================
  # ============================================================================================================
  # ------------------------ add redis code here start ------------------------
  # ------------------------ add redis code here end ------------------------
  # ============================================================================================================
  # ============================================================================================================
  # ============================================================================================================
  localhost_print_function('=========================================== candidates_logout_function END ===========================================')
  return redirect(url_for('auth.candidates_login_page_function'))
# ------------------------ individual route end ------------------------


# ------------------------ individual route start ------------------------
@auth.route('/candidates/signup', methods=['GET', 'POST'])
def candidates_signup_function():
  localhost_print_function('=========================================== candidates_signup_function START ===========================================')
  if request.method == 'POST':
    # ------------------------ post method hit #1 - quick sign up start ------------------------
    ui_email = request.form.get('various_pages1_ui_email')
    if ui_email != None:
      # ============================================================================================================
      # ============================================================================================================
      # ============================================================================================================
      # ------------------------ Sanitize: Here you have to run backend checks on all the user inputs/sanitize start ------------------------
      # ------------------------ Sanitize: Here you have to run backend checks on all the user inputs/sanitize end ------------------------
      # ============================================================================================================
      # ============================================================================================================
      # ============================================================================================================
      localhost_print_function('user is being redirected to full sign up page')
      localhost_print_function('=========================================== candidates_signup_function END ===========================================')
      return render_template('candidates_page_templates/not_logged_in_page_templates/create_account_templates/index.html', user=current_user, redirect_var_email = ui_email)
    # ------------------------ post method hit #1 - quick sign up end ------------------------
    # ------------------------ post method hit #2 - full sign up start ------------------------
    ui_email = request.form.get('create_account_page_ui_email')
    ui_password = request.form.get('create_account_page_ui_password')
    ui_password_confirmed = request.form.get('create_account_page_ui_password_confirmed')
    ui_first_name = request.form.get('create_account_page_ui_first_name')
    ui_last_name = request.form.get('create_account_page_ui_last_name')
    ui_company_name = request.form.get('create_account_page_ui_company_name')
    ui_department_name = request.form.get('create_account_page_ui_department_name')
    # ============================================================================================================
    # ============================================================================================================
    # ============================================================================================================
    # ------------------------ Sanitize: Here you have to run backend checks on all the user inputs/sanitize start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email)
    # ------------------------ Sanitize: Here you have to run backend checks on all the user inputs/sanitize end ------------------------
    # ============================================================================================================
    # ============================================================================================================
    # ============================================================================================================
    user = CandidatesUserObj.query.filter_by(email=ui_email).first()
    if user:
      flash('Email already exists.', category='error')
    elif len(ui_email) < 4:
      flash('Email must be greater than 3 characters.', category='error')
    elif len(ui_first_name) < 2:
      flash('First name must be greater than 1 character.', category='error')
    elif ui_password != ui_password_confirmed:
      flash('Passwords don\'t match.', category='error')
    elif len(ui_password) < 7:
      flash('Password must be at least 7 characters.', category='error')
    else:
      # ------------------------ create new user in db start ------------------------
      new_user = CandidatesUserObj(
        email=ui_email,
        password=generate_password_hash(ui_password, method="sha256"),
        first_name = ui_first_name,
        last_name = ui_last_name,
        company_name = ui_company_name,
        department_name = ui_department_name
      )
      db.session.add(new_user)
      db.session.commit()
      flash('Account created!', category='success')
      # ------------------------ create new user in db end ------------------------
      # ------------------------ keep user logged in start ------------------------
      login_user(new_user, remember=True)
      # ============================================================================================================
      # ============================================================================================================
      # ============================================================================================================
      # ------------------------ add redis code here start ------------------------
      # ------------------------ add redis code here end ------------------------
      # ============================================================================================================
      # ============================================================================================================
      # ============================================================================================================
      # ------------------------ keep user logged in end ------------------------
      localhost_print_function('=========================================== candidates_signup_function END ===========================================')
      return redirect(url_for('views.dashboard_test_login_page_function'))
    # ------------------------ post method hit #2 - full sign up end ------------------------

  localhost_print_function('=========================================== candidates_signup_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/create_account_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------
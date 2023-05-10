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
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from website.backend.candidates.user_inputs import sanitize_email_function, sanitize_password_function
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website.backend.candidates.send_emails import send_email_template_function
import os
from website.backend.candidates.user_inputs import alert_message_default_function_v2
from .models import UserObj, EmailCollectObj, EmailScrapedObj
from website.backend.candidates.pull_create_logic import pull_create_group_id_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
employees_auth = Blueprint('employees_auth', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@employees_auth.route('/employees/signup', methods=['GET', 'POST'])
@employees_auth.route('/employees/signup/', methods=['GET', 'POST'])
@employees_auth.route('/employees/signup/<url_redirect_code>', methods=['GET', 'POST'])
def employees_signup_function(url_redirect_code=None):
  # ------------------------ redirect codes start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  # ------------------------ redirect codes end ------------------------
  if request.method == 'POST':
    # ------------------------ post method hit #1 - quick sign up start ------------------------
    ui_email = request.form.get('uiEmailVarious')
    if ui_email != None:
      # ------------------------ sanitize/check user input email start ------------------------
      ui_email_cleaned = sanitize_email_function(ui_email, 'true')
      if ui_email_cleaned == False:
        return redirect(url_for('employees_auth.employees_signup_function', url_redirect_code='e1'))
      # ------------------------ sanitize/check user input email end ------------------------
      # ------------------------ check if email already exists in db start ------------------------
      email_exists = EmailCollectObj.query.filter_by(email=ui_email).first()
      # ------------------------ check if email already exists in db end ------------------------
      # ------------------------ create new signup in db start ------------------------
      if email_exists == None or email_exists == []:
        new_row = EmailCollectObj(
          id=create_uuid_function('collect_email_'),
          created_timestamp=create_timestamp_function(),
          email=ui_email.lower(),
          source='employees'
        )
        db.session.add(new_row)
        db.session.commit()
      # ------------------------ create new signup in db end ------------------------
      return render_template('employees/exterior/signup/index.html', alert_message_dict_to_html=alert_message_dict, redirect_var_email=ui_email)
    # ------------------------ post method hit #1 - quick sign up end ------------------------
    # ------------------------ post method hit #2 - full sign up start ------------------------
    ui_email = request.form.get('uiEmail')
    ui_password = request.form.get('uiPassword')
    # ------------------------ sanitize/check user inputs start ------------------------
    # ------------------------ sanitize/check user input email start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email, 'true')
    if ui_email_cleaned == False:
      return redirect(url_for('employees_auth.employees_signup_function', url_redirect_code='e1'))
    # ------------------------ sanitize/check user input email end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_cleaned = sanitize_password_function(ui_password)
    if ui_password_cleaned == False:
      return redirect(url_for('employees_auth.employees_signup_function', url_redirect_code='e2'))
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ sanitize/check user inputs end ------------------------
    # ------------------------ check if user email already exists in db start ------------------------
    user_exists = UserObj.query.filter_by(email=ui_email).first()
    if user_exists != None and user_exists != []:
      return redirect(url_for('employees_auth.employees_signup_function', url_redirect_code='e3'))
    # ------------------------ check if user email already exists in db start ------------------------
    else:
      # ------------------------ infer company name start ------------------------
      email_arr1 = ui_email.split('@')
      company_name_from_email = email_arr1[1].lower()
      # ------------------------ infer company name end ------------------------
      # ------------------------ create new user in db start ------------------------
      new_row = UserObj(
        id=create_uuid_function('user_'),
        created_timestamp=create_timestamp_function(),
        email=ui_email.lower(),
        password=generate_password_hash(ui_password, method="sha256"),
        company_name = company_name_from_email,
        verified_email = False
      )
      db.session.add(new_row)
      # ------------------------ remove from landing page collected start ------------------------
      try:
        EmailCollectObj.query.filter_by(email=ui_email.lower()).delete()
      except:
        pass
      # ------------------------ remove from landing page collected end ------------------------
      # ------------------------ remove from scraped start ------------------------
      try:
        EmailScrapedObj.query.filter_by(email=ui_email.lower()).delete()
      except:
        pass
      # ------------------------ remove from scraped end ------------------------
      db.session.commit()
      # ------------------------ create new user in db end ------------------------
      # ------------------------ keep user logged in start ------------------------
      login_user(new_row, remember=True)
      # ------------------------ keep user logged in end ------------------------
      # ------------------------ pull/create + assign group id start ------------------------
      if current_user.group_id == None or current_user.group_id == '':
        current_user.group_id = pull_create_group_id_function(current_user)
        db.session.commit()
      # ------------------------ pull/create + assign group id end ------------------------
      # ------------------------ email self start ------------------------
      try:
        output_to_email = os.environ.get('TRIVIAFY_NOTIFICATIONS_EMAIL')
        output_subject = f'Triviafy Employees - Signup - {ui_email}'
        output_body = f"Hi there,\n\nNew user signed up: {ui_email} \n\nBest,\nTriviafy"
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self end ------------------------
      return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
    # ------------------------ post method hit #2 - full sign up end ------------------------
  return render_template('employees/exterior/signup/index.html', alert_message_dict_to_html=alert_message_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_auth.route('/employees/login', methods=['GET', 'POST'])
@employees_auth.route('/employees/login/', methods=['GET', 'POST'])
@employees_auth.route('/employees/login/<url_redirect_code>', methods=['GET', 'POST'])
def employees_login_page_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_login_page_function start ------------------------ ')
  # ------------------------ redirect codes start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  # ------------------------ redirect codes end ------------------------
  # ------------------------ auto sign in with cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    try:
      user_id_from_redis = redis_connection.get(get_cookie_value_from_browser).decode('utf-8')
      if user_id_from_redis != None:
        user = UserObj.query.filter_by(id=user_id_from_redis).first()
        # ------------------------ keep user logged in start ------------------------
        login_user(user, remember=True)
        # ------------------------ keep user logged in end ------------------------
        localhost_print_function('redirecting to logged in page')
        return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
    except:
      pass
  # ------------------------ auto sign in with cookie end ------------------------
  if request.method == 'POST':
    # ------------------------ post method hit #1 - regular login start ------------------------
    # ------------------------ post request sent start ------------------------
    ui_email = request.form.get('uiEmail')
    ui_password = request.form.get('uiPassword')
    # ------------------------ post request sent end ------------------------
    # ------------------------ sanitize/check user input email start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email)
    if ui_email_cleaned == False:
      localhost_print_function(' ------------------------ employees_login_page_function end ------------------------ ')
      return redirect(url_for('employees_auth.employees_login_page_function', url_redirect_code='e1'))
    # ------------------------ sanitize/check user input email end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_cleaned = sanitize_password_function(ui_password)
    if ui_password_cleaned == False:
      return redirect(url_for('employees_auth.employees_login_page_function', url_redirect_code='e2'))
    # ------------------------ sanitize/check user input password end ------------------------
    user = UserObj.query.filter_by(email=ui_email).first()
    if user:
      if check_password_hash(user.password, ui_password):
        # ------------------------ keep user logged in start ------------------------
        login_user(user, remember=True)
        # ------------------------ keep user logged in end ------------------------
        return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
      else:
        return redirect(url_for('employees_auth.employees_login_page_function', url_redirect_code='e4'))
    else:
      return redirect(url_for('employees_auth.employees_login_page_function', url_redirect_code='e4'))
    # ------------------------ post method hit #1 - regular login end ------------------------
  localhost_print_function(' ------------------------ employees_login_page_function end ------------------------ ')
  return render_template('employees/exterior/login/index.html', alert_message_dict_to_html=alert_message_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_auth.route('/logout')
@employees_auth.route('/logout/')
@employees_auth.route('/employees/logout')
@employees_auth.route('/employees/logout/')
@login_required
def employees_logout_function():
  localhost_print_function(' ------------------------ employees_logout_function start ------------------------ ')
  logout_user()
  # ------------------------ auto sign in with cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  # ------------------------ auto sign in with cookie end ------------------------
  if get_cookie_value_from_browser != None:
    try:
      redis_connection.delete(get_cookie_value_from_browser)
    except:
      pass
  # ------------------------ auto sign in with cookie end ------------------------
  localhost_print_function(' ------------------------ employees_logout_function end ------------------------ ')
  return redirect(url_for('employees_auth.employees_login_page_function'))
# ------------------------ individual route end ------------------------
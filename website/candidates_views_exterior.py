# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -Note: any pages related to authentication will not be in this file, they will be routed in the auth.py file.
# -@login_required   # this decorator says that url cannot be accessed unless the user is logged in. 
# -@login_required: <-- This decorator will bring a user to __init__ code: [login_manager.login_view = 'auth.candidates_login_page_function'] if they hit a page that requires login and they are not logged in.
# -use code: <methods=['GET', 'POST']> when you want the user to interact with the page through forms/checkbox/textbox/radio/etc.
# ------------------------ info about this file end ------------------------

# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from website.backend.candidates.redis import redis_connect_to_database_function
from website.models import UserObj
from website import db
from website.backend.candidates.user_inputs import sanitize_email_function, sanitize_password_function
from website.backend.candidates.send_emails import send_email_template_function
from werkzeug.security import generate_password_hash
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
candidates_views_exterior = Blueprint('candidates_views_exterior', __name__)
# ------------------------ function end ------------------------
# ------------------------ before page variables start ------------------------
cache_busting_output = create_uuid_function('css_')
# ------------------------ before page variables end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ routes not logged in start ------------------------
# ------------------------ individual route start ------------------------
@candidates_views_exterior.route('/')
def products_page_function():
  localhost_print_function(' ------------------------ products_page_function START ------------------------ ')
  localhost_print_function(' ------------------------ products_page_function END ------------------------ ')
  return render_template('candidates/exterior/landing/index.html', user=current_user)
  # return render_template('products/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_exterior.route('/candidates')
def candidates_landing_index_page_function():
  localhost_print_function(' ------------------------ candidates_landing_index_page_function START ------------------------ ')
  localhost_print_function(' ------------------------ candidates_landing_index_page_function END ------------------------ ')
  return render_template('candidates/exterior/landing/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_exterior.route('/candidates/about')
def candidates_about_page_function():
  localhost_print_function(' ------------------------ candidates_about_page_function START ------------------------ ')  
  localhost_print_function(' ------------------------ candidates_about_page_function END ------------------------ ')
  return render_template('candidates/exterior/about/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_exterior.route('/candidates/faq')
def candidates_faq_page_function():
  localhost_print_function(' ------------------------ candidates_faq_page_function START ------------------------ ')
  localhost_print_function(' ------------------------ candidates_faq_page_function END ------------------------ ')
  return render_template('candidates/exterior/faq/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_exterior.route('/candidates/library')
def candidates_test_library_page_function():
  localhost_print_function(' ------------------------ candidates_test_library_page_function START ------------------------ ')
  localhost_print_function(' ------------------------ candidates_test_library_page_function END ------------------------ ')
  return render_template('candidates/exterior/test_library/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_exterior.route('/candidates/pricing')
def candidates_pricing_page_function():
  localhost_print_function(' ------------------------ candidates_pricing_page_function START ------------------------ ')
  localhost_print_function(' ------------------------ candidates_pricing_page_function END ------------------------ ')
  return render_template('candidates/exterior/pricing/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_exterior.route('/404')
def error_page_function():
  localhost_print_function(' ------------------------ error_page_function START ------------------------ ')
  localhost_print_function(' ------------------------ error_page_function END ------------------------ ')
  return render_template('candidates/exterior/error_404/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_exterior.route('/candidates/reset', methods=['GET', 'POST'])
def candidates_forgot_password_page_function():
  localhost_print_function(' ------------------------ candidates_forgot_password_page_function START ------------------------ ')  
  forgot_password_error_statement = ''
  if request.method == 'POST':
    # ------------------------ post request sent start ------------------------
    ui_email = request.form.get('forgot_password_page_ui_email')
    # ------------------------ post request sent end ------------------------
    # ------------------------ sanitize/check user input email start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email)
    if ui_email_cleaned == False:
      forgot_password_error_statement = 'Please enter a valid work email.'
    # ------------------------ sanitize/check user input email end ------------------------
    # ------------------------ check if user email exists in db start ------------------------
    user_exists = UserObj.query.filter_by(email=ui_email).first()
    if user_exists:
      forgot_password_error_statement = 'Password reset link sent to email.'
      # ------------------------ send email with token url start ------------------------
      serializer_token_obj = UserObj.get_reset_token_function(self=user_exists)
      output_email = ui_email
      output_subject_line = 'Password Reset - Triviafy'
      output_message_content = f"To reset your password, visit the following link: https://triviafy.com/candidates/reset/{serializer_token_obj} \n\nThis link will expire after 30 minutes.\nIf you did not make this request then simply ignore this email and no changes will be made."
      send_email_template_function(output_email, output_subject_line, output_message_content)
      # ------------------------ send email with token url end ------------------------
    else:
      forgot_password_error_statement = 'Password reset link sent to email.'
      pass
    # ------------------------ check if user email exists in db end ------------------------
  localhost_print_function(' ------------------------ candidates_forgot_password_page_function END ------------------------ ')
  return render_template('candidates/exterior/forgot_password/index.html', user=current_user, error_message_to_html = forgot_password_error_statement)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_exterior.route('/candidates/reset/<token>', methods=['GET', 'POST'])
def candidates_reset_forgot_password_page_function(token):
  localhost_print_function(' ------------------------ candidates_reset_forgot_password_page_function START ------------------------ ')
  # if current_user.is_authenticated == False:
  #   return redirect(url_for('candidates_views_interior.login_dashboard_page_function'))
  reset_password_error_statement = ''
  user_obj_from_token = UserObj.verify_reset_token_function(token)
  if user_obj_from_token is None:
    reset_password_error_statement = 'That is an invalid or expired token'
    localhost_print_function(' ------------------------ candidates_reset_forgot_password_page_function END ------------------------ ')
    return render_template('candidates/exterior/forgot_password/index.html', user=current_user, error_message_to_html = reset_password_error_statement)
  if request.method == 'POST':
    reset_password_error_statement = ''
    # ------------------------ get inputs from form start ------------------------
    ui_password = request.form.get('reset_forgot_password_page_ui_password')
    ui_password_confirmed = request.form.get('reset_forgot_password_page_ui_password_confirmed')
    # ------------------------ get inputs from form end ------------------------
    # ------------------------ check match start ------------------------
    if ui_password != ui_password_confirmed:
      reset_password_error_statement = 'Passwords do not match.'
    # ------------------------ check match end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_cleaned = sanitize_password_function(ui_password)
    if ui_password_cleaned == False:
      reset_password_error_statement = 'Password is not valid.'
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_confirmed_cleaned = sanitize_password_function(ui_password_confirmed)
    if ui_password_confirmed_cleaned == False:
      reset_password_error_statement = 'Password is not valid.'
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ update db start ------------------------
    if reset_password_error_statement == '':
      user_obj_from_token.password = generate_password_hash(ui_password, method="sha256")
      db.session.commit()
      return redirect(url_for('candidates_views_interior.login_dashboard_page_function'))
    # ------------------------ update db end ------------------------
  localhost_print_function(' ------------------------ candidates_reset_forgot_password_page_function END ------------------------ ')
  return render_template('candidates/exterior/forgot_password/reset_forgot_password/index.html', user=current_user, error_message_to_html = reset_password_error_statement)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_exterior.route('/candidates/blog', methods=['GET', 'POST'])
def candidates_blog_page_function():
  localhost_print_function(' ------------------------ candidates_blog_page_function START ------------------------ ')
  localhost_print_function(' ------------------------ candidates_blog_page_function END ------------------------ ')
  return render_template('candidates/exterior/blog/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_exterior.route('/candidates/blog/<i_blog_post_number>', methods=['GET', 'POST'])
def candidates_i_blog_page_function(i_blog_post_number):
  localhost_print_function(' ------------------------ candidates_i_blog_page_function START ------------------------ ')
  current_blog_post_num = i_blog_post_number
  current_blog_post_num_full_string = f'candidates/exterior/blog/i_blog/i_{current_blog_post_num}.html'
  localhost_print_function(' ------------------------ candidates_i_blog_page_function END ------------------------ ')
  return render_template(current_blog_post_num_full_string)
# ------------------------ individual route end ------------------------
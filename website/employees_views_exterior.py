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
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from website.backend.candidates.redis import redis_connect_to_database_function
from website.models import ActivityACreatedQuestionsObj, ZDontDeleteTableObj, UserObj
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function, categories_tuple_function
from website.backend.candidates.user_inputs import alert_message_default_function_v2, sanitize_email_function, sanitize_password_function
from website.backend.candidates.send_emails import send_email_template_function
from website import db
from werkzeug.security import generate_password_hash
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
employees_views_exterior = Blueprint('employees_views_exterior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/')
@employees_views_exterior.route('/employees')
@employees_views_exterior.route('/employees/')
def landing_page_function():
  localhost_print_function(' ------------------------ landing_page_function START ------------------------ ')
  localhost_print_function(' ------------------------ landing_page_function END ------------------------ ')
  return render_template('employees/exterior/landing/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees/about')
@employees_views_exterior.route('/employees/about/')
def employees_about_function():
  localhost_print_function(' ------------------------ employees_about_function START ------------------------ ')
  localhost_print_function(' ------------------------ employees_about_function END ------------------------ ')
  return render_template('employees/exterior/about/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees/faq')
@employees_views_exterior.route('/employees/faq/')
def employees_faq_function():
  localhost_print_function(' ------------------------ employees_faq_function start ------------------------ ')
  localhost_print_function(' ------------------------ employees_faq_function end ------------------------ ')
  return render_template('employees/exterior/faq/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees/pricing')
@employees_views_exterior.route('/employees/pricing/')
def employees_pricing_function():
  localhost_print_function(' ------------------------ employees_pricing_function start ------------------------ ')
  localhost_print_function(' ------------------------ employees_pricing_function end ------------------------ ')
  return render_template('employees/exterior/pricing/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees/privacy')
@employees_views_exterior.route('/employees/privacy/')
def employees_privacy_function():
  localhost_print_function(' ------------------------ employees_privacy_function start ------------------------ ')
  localhost_print_function(' ------------------------ employees_privacy_function end ------------------------ ')
  return render_template('employees/exterior/privacy/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees/tos')
@employees_views_exterior.route('/employees/tos/')
def employees_tos_function():
  localhost_print_function(' ------------------------ employees_tos_function start ------------------------ ')
  localhost_print_function(' ------------------------ employees_tos_function end ------------------------ ')
  return render_template('employees/exterior/tos/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees/blog', methods=['GET', 'POST'])
@employees_views_exterior.route('/employees/blog/', methods=['GET', 'POST'])
def employees_blog_page_function():
  localhost_print_function(' ------------------------ employees_blog_page_function START ------------------------ ')
  localhost_print_function(' ------------------------ employees_blog_page_function END ------------------------ ')
  return render_template('employees/exterior/blog/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees/blog/<i_blog_post_number>', methods=['GET', 'POST'])
@employees_views_exterior.route('/employees/blog/<i_blog_post_number>/', methods=['GET', 'POST'])
def employees_i_blog_page_function(i_blog_post_number='0001'):
  localhost_print_function(' ------------------------ employees_i_blog_page_function start ------------------------ ')
  current_blog_post_num = i_blog_post_number
  current_blog_post_num_full_string = f'employees/exterior/blog/i_blog/i_{current_blog_post_num}.html'
  localhost_print_function(' ------------------------ employees_i_blog_page_function end ------------------------ ')
  return render_template(current_blog_post_num_full_string)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/example', methods=['GET', 'POST'])
@employees_views_exterior.route('/example/', methods=['GET', 'POST'])
@employees_views_exterior.route('/example/<url_question_number>', methods=['GET', 'POST'])
@employees_views_exterior.route('/example/<url_question_number>/', methods=['GET', 'POST'])
def employees_example_page_function(url_redirect_code=None, url_question_number='1'):
  localhost_print_function(' ------------------------ employees_example_page_function start ------------------------ ')
  # ------------------------ redirect codes start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  # ------------------------ redirect codes end ------------------------
  # ------------------------ pull test start ------------------------
  db_test_obj = ZDontDeleteTableObj.query.filter_by(id='employees_example_do_not_delete_01').first()
  db_test_obj = arr_of_dict_all_columns_single_item_function(db_test_obj)
  total_questions = int(db_test_obj['total_questions'])
  try:
    if int(url_question_number) < 1 or int(url_question_number) > total_questions:
      return redirect(url_for('employees_views_exterior.employees_example_page_function', url_question_number='1'))
  except:
    return redirect(url_for('employees_views_exterior.employees_example_page_function', url_question_number='1'))
  question_ids_str = db_test_obj['question_ids_arr']
  question_ids_arr = question_ids_str.split(',')
  desired_question_str = question_ids_arr[int(url_question_number)-1]
  # ------------------------ pull test end ------------------------
  # ------------------------ pull question start ------------------------
  db_question_obj = ActivityACreatedQuestionsObj.query.filter_by(id=desired_question_str).first()
  db_question_obj = arr_of_dict_all_columns_single_item_function(db_question_obj)
  db_question_obj['categories'] = categories_tuple_function(db_question_obj['categories'])
  # ------------------------ pull question end ------------------------
  # ------------------------ previous next current start ------------------------
  previous_question_number = str(int(url_question_number) - 1)
  current_question_number = str(url_question_number)
  next_question_number = str(int(url_question_number) + 1)
  if int(url_question_number) == total_questions:
    next_question_number = 'submit'
  # ------------------------ previous next current end ------------------------
  # ------------------------ check if contains img start ------------------------
  contains_img = False
  if 'amazonaws.com' in db_question_obj['aws_image_url']:
    contains_img = True
  # ------------------------ check if contains img end ------------------------
  localhost_print_function(' ------------------------ employees_example_page_function end ------------------------ ')
  return render_template('employees/exterior/example_test/index.html', db_question_obj_to_html=db_question_obj, previous_question_number_to_html=previous_question_number, current_question_number_to_html=current_question_number, next_question_number_to_html=next_question_number, alert_message_dict_to_html=alert_message_dict, contains_img_to_html=contains_img)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees/reset', methods=['GET', 'POST'])
def employees_forgot_password_page_function():
  localhost_print_function(' ------------------------ employees_forgot_password_page_function START ------------------------ ')  
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
      output_message_content = f"To reset your password, visit the following link: https://triviafy.com/employees/reset/{serializer_token_obj} \n\nThis link will expire after 30 minutes.\nIf you did not make this request then simply ignore this email and no changes will be made."
      send_email_template_function(output_email, output_subject_line, output_message_content)
      # ------------------------ send email with token url end ------------------------
    else:
      forgot_password_error_statement = 'Password reset link sent to email.'
      pass
    # ------------------------ check if user email exists in db end ------------------------
  localhost_print_function(' ------------------------ employees_forgot_password_page_function END ------------------------ ')
  return render_template('employees/exterior/forgot_password/index.html', user=current_user, error_message_to_html = forgot_password_error_statement)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees/reset/<token>', methods=['GET', 'POST'])
def employees_reset_forgot_password_page_function(token):
  localhost_print_function(' ------------------------ employees_reset_forgot_password_page_function START ------------------------ ')
  reset_password_error_statement = ''
  user_obj_from_token = UserObj.verify_reset_token_function(token)
  if user_obj_from_token is None:
    reset_password_error_statement = 'That is an invalid or expired token'
    localhost_print_function(' ------------------------ employees_reset_forgot_password_page_function END ------------------------ ')
    return render_template('employees/exterior/forgot_password/index.html', user=current_user, error_message_to_html = reset_password_error_statement)
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
      return redirect(url_for('employees_auth.employees_login_page_function', url_redirect_code='s6'))
    # ------------------------ update db end ------------------------
  localhost_print_function(' ------------------------ employees_reset_forgot_password_page_function END ------------------------ ')
  return render_template('employees/exterior/forgot_password/reset_forgot_password/index.html', user=current_user, error_message_to_html = reset_password_error_statement)
# ------------------------ individual route end ------------------------
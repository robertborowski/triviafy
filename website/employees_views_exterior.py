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
from website.models import ActivityACreatedQuestionsObj, UserObj, BlogObj
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function, categories_tuple_function
from website.backend.candidates.user_inputs import alert_message_default_function_v2, sanitize_email_function, sanitize_password_function
from website.backend.candidates.send_emails import send_email_template_function
from website import db
from werkzeug.security import generate_password_hash
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
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
  return render_template('employees/exterior/landing/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/about')
@employees_views_exterior.route('/about/')
def employees_about_function():
  return render_template('employees/exterior/about/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/faq')
@employees_views_exterior.route('/faq/')
def employees_faq_function():
  return render_template('employees/exterior/faq/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/pricing')
@employees_views_exterior.route('/pricing/')
def employees_pricing_function():
  return render_template('employees/exterior/pricing/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/privacy')
@employees_views_exterior.route('/privacy/')
def employees_privacy_function():
  return render_template('employees/exterior/privacy/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/terms')
@employees_views_exterior.route('/terms/')
def terms_function():
  return render_template('employees/exterior/tos/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/blog', methods=['GET', 'POST'])
@employees_views_exterior.route('/blog/', methods=['GET', 'POST'])
def employees_blog_page_function():
  page_dict = {}
  master_arr_of_dicts = []
  blog_obj = BlogObj.query.order_by(BlogObj.created_timestamp.desc()).all()
  for i_obj in blog_obj:
    i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
    i_dict['title'] = i_dict['title'][:50] + '...'
    i_dict['details'] = i_dict['details'][:100] + '...'
    master_arr_of_dicts.append(i_dict)
  page_dict['master_arr_of_dicts'] = master_arr_of_dicts
  return render_template('employees/exterior/blog/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/blog/<i_blog_post_id>', methods=['GET', 'POST'])
@employees_views_exterior.route('/blog/<i_blog_post_id>/', methods=['GET', 'POST'])
def employees_i_blog_page_function(i_blog_post_id=None):
  if i_blog_post_id == None or i_blog_post_id == '':
    return redirect(url_for('employees_views_exterior.employees_blog_page_function'))
  try:
    blog_obj = BlogObj.query.filter_by(id=i_blog_post_id).first()
    if blog_obj == None or blog_obj == '':
      return redirect(url_for('employees_views_exterior.employees_blog_page_function'))
  except:
    return redirect(url_for('employees_views_exterior.employees_blog_page_function'))
  current_blog_post_num_full_string = f'employees/exterior/blog/blogs_by_id/{i_blog_post_id}.html'
  return render_template(current_blog_post_num_full_string)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/example/<url_activity_type>', methods=['GET', 'POST'])
@employees_views_exterior.route('/example/<url_activity_type>/<url_activity_code>', methods=['GET', 'POST'])
@employees_views_exterior.route('/example/<url_activity_type>/<url_activity_code>/', methods=['GET', 'POST'])
@employees_views_exterior.route('/example/<url_activity_type>/<url_activity_code>/<url_question_number>', methods=['GET', 'POST'])
@employees_views_exterior.route('/example/<url_activity_type>/<url_activity_code>/<url_question_number>/', methods=['GET', 'POST'])
def employees_example_function(url_redirect_code=None, url_activity_type=None, url_activity_code=None, url_question_number=None):
  # ------------------------ redirect codes start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ redirect codes end ------------------------
  # ------------------------ url variables start ------------------------
  if url_question_number == None:
    url_question_number = '1'
  if url_activity_type == None or url_activity_code == None:
    return redirect(url_for('employees_views_exterior.landing_page_function'))
  # ------------------------ url variables end ------------------------
  # ------------------------ assign variables start ------------------------
  page_dict['url_activity_type'] = url_activity_type
  page_dict['url_activity_code'] = url_activity_code
  page_dict['url_question_number'] = url_question_number
  # ------------------------ assign variables end ------------------------
  # ------------------------ pull activity examples start ------------------------
  result_arr_of_dicts = None
  if url_activity_type == 'activity_type_a':
    if url_activity_code == 'trivia':
      result_arr_of_dicts = select_general_function('select_sample_trivia')
    elif url_activity_code == 'picture_quiz':
      result_arr_of_dicts = select_general_function('select_sample_picture_quiz')
  if url_activity_type == 'activity_type_b':
    if url_activity_code == 'icebreakers':
      result_arr_of_dicts = select_general_function('select_sample_icebreakers')
  page_dict['result_arr_of_dicts'] = result_arr_of_dicts
  page_dict['test_total_questions'] = len(result_arr_of_dicts)
  page_dict['test_total_questions_arr'] = ['1','2','3','4','5']
  # ------------------------ pull activity examples end ------------------------
  # ------------------------ previous next current start ------------------------
  page_dict['previous_question_number'] = str(int(url_question_number) - 1)
  page_dict['current_question_number'] = str(url_question_number)
  page_dict['next_question_number'] = str(int(url_question_number) + 1)
  if int(url_question_number) == len(result_arr_of_dicts):
    page_dict['next_question_number'] = 'submit'
  # ------------------------ previous next current end ------------------------
  # ------------------------ current question details start ------------------------
  page_dict['db_question_dict'] = result_arr_of_dicts[int(url_question_number)-1]
  if url_activity_type == 'activity_type_a':
    page_dict['db_question_dict']['categories'] = categories_tuple_function(page_dict['db_question_dict']['categories'])
    page_dict['db_question_dict']['desired_question_type'] = 'Multiple choice'
  # ------------------------ current question details end ------------------------
  localhost_print_function(' ------------- 100-example start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-example end ------------- ')
  if url_activity_type == 'activity_type_a':
    return render_template('employees/exterior/example_test/activity_type_a/index.html', page_dict_to_html=page_dict)
  if url_activity_type == 'activity_type_b':
    return render_template('employees/exterior/example_test/activity_type_b/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/reset', methods=['GET', 'POST'])
def employees_forgot_password_page_function():
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
      output_message_content = f"To reset your password, visit the following link: https://triviafy.com/reset/{serializer_token_obj} \n\nThis link will expire after 30 minutes.\nIf you did not make this request then simply ignore this email and no changes will be made."
      send_email_template_function(output_email, output_subject_line, output_message_content)
      # ------------------------ send email with token url end ------------------------
    else:
      forgot_password_error_statement = 'Password reset link sent to email.'
      pass
    # ------------------------ check if user email exists in db end ------------------------
  return render_template('employees/exterior/forgot_password/index.html', user=current_user, error_message_to_html = forgot_password_error_statement)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/reset/<token>', methods=['GET', 'POST'])
def employees_reset_forgot_password_page_function(token):
  reset_password_error_statement = ''
  user_obj_from_token = UserObj.verify_reset_token_function(token)
  if user_obj_from_token is None:
    reset_password_error_statement = 'That is an invalid or expired token'
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
  return render_template('employees/exterior/forgot_password/reset_forgot_password/index.html', user=current_user, error_message_to_html = reset_password_error_statement)
# ------------------------ individual route end ------------------------
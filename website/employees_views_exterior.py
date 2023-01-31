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
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from website.backend.candidates.redis import redis_connect_to_database_function
from website.models import CreatedQuestionsObj, CandidatesAssessmentsCreatedObj
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function, categories_tuple_function
from website.backend.candidates.user_inputs import alert_message_default_function_v2
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
employees_views_exterior = Blueprint('employees_views_exterior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
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
@employees_views_exterior.route('/employees/example', methods=['GET', 'POST'])
@employees_views_exterior.route('/employees/example/', methods=['GET', 'POST'])
@employees_views_exterior.route('/employees/example/<url_question_number>', methods=['GET', 'POST'])
@employees_views_exterior.route('/employees/example/<url_question_number>/', methods=['GET', 'POST'])
def employees_example_page_function(url_redirect_code=None, url_question_number='1'):
  localhost_print_function(' ------------------------ employees_example_page_function start ------------------------ ')
  # ------------------------ redirect codes start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  # ------------------------ redirect codes end ------------------------
  # ------------------------ pull test start ------------------------
  db_test_obj = CandidatesAssessmentsCreatedObj.query.filter_by(id='employees_example_do_not_delete_01').first()
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
  db_question_obj = CreatedQuestionsObj.query.filter_by(id=desired_question_str).first()
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
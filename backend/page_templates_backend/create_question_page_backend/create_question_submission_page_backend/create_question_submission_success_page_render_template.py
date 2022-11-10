# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_all_questions_table.select_all_questions_created_by_owner_specific_page import select_all_questions_created_by_owner_specific_page_function
from backend.db.queries.select_queries.select_queries_triviafy_all_questions_table.select_all_questions_created_by_owner_email_uuid import select_all_questions_created_by_owner_email_uuid_function
import os
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function
from backend.utils.quiz_categories_utils.datatype_change_categories_list_str_to_tuple import datatype_change_categories_list_str_to_tuple_function
import math

# -------------------------------------------------------------- App Setup
create_question_submission_success_page_render_template = Blueprint("create_question_submission_success_page_render_template", __name__, static_folder="static", template_folder="templates")
@create_question_submission_success_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@create_question_submission_success_page_render_template.route("/create/question/user/form/submit/success/<html_variable_created_question_page_number>", methods=['GET','POST'])
def create_question_submission_success_page_render_template_function(html_variable_created_question_page_number):
  localhost_print_function('=========================================== /create/question/user/form/submit/success/<html_variable_created_question_page_number> Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/create/question/user/form/submit/success/<html_variable_created_question_page_number>')
    # Redirects based on returned value - pre load checks
    if user_nested_dict == '/employees/subscription':
      return redirect('/employees/subscription', code=302)
    elif user_nested_dict == '/notifications/email/permission':
      return redirect('/notifications/email/permission', code=302)
    elif user_nested_dict == '/new/user/questionnaire':
      return redirect('/new/user/questionnaire', code=302)
    elif user_nested_dict == '/categories/edit':
      return redirect('/categories/edit', code=302)
    elif user_nested_dict == '/employees/logout':
      return redirect('/employees/logout', code=302)
    # ------------------------ Pre Load Page Checks END ------------------------


    # ------------------------ Page Company Info START ------------------------
    user_company_name = user_nested_dict['user_company_name']
    user_company_name = sanitize_page_output_company_name_function(user_company_name)
    user_channel_name = user_nested_dict['user_slack_channel_name']
    # ------------------------ Page Company Info END ------------------------
    
    # Get additional variables
    user_email = user_nested_dict['user_email']
    user_uuid = user_nested_dict['user_uuid']
    desired_page_number = int(html_variable_created_question_page_number)

  except:
    localhost_print_function('page load except error hit - /create/question/user/form/submit/success/<html_variable_created_question_page_number> Page')
    localhost_print_function('=========================================== /create/question/user/form/submit/success/<html_variable_created_question_page_number> Page END ===========================================')
    return redirect('/employees/logout', code=302)
    # return redirect('/', code=302)

  """
  # ------------------------ Check create question accesss START ------------------------
  # Get personal email
  personal_email = os.environ.get('PERSONAL_EMAIL')

  # If user does not have access to create questions then redirect to waitlist page
  if user_email != personal_email:
    localhost_print_function('redirecting to the create question wait list page!')
    localhost_print_function('=========================================== /create/question/user/form/submit/success/<html_variable_created_question_page_number> Page END ===========================================')
    return redirect('/create/question/user/waitlist', code=302)
  # ------------------------ Check create question accesss END ------------------------
  """
  
  # ------------------------ Connect DB START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ Connect DB END ------------------------
  # ------------------------ Break Down to Pages of arr dict START ------------------------
  all_question_uuids_arr = select_all_questions_created_by_owner_email_uuid_function(postgres_connection, postgres_cursor, user_uuid)    # arr
  
  # If user has not made any questions yet
  if all_question_uuids_arr == None:
    return redirect('/create/question/user/form', code=302)

  num_questions_per_page = 5
  if len(all_question_uuids_arr) <= num_questions_per_page:
    total_num_of_pages = 1
  else:
    total_num_of_pages = math.floor(len(all_question_uuids_arr) / num_questions_per_page)   # int
  
  # 404 page if user searches for page number that does not exist for them
  if desired_page_number > total_num_of_pages + 1:
    return render_template("error_404_page_templates/index.html")
  
  question_counter = 0    # int
  current_page_num = 1    # int
  pages_questions_dict = {}    # dict
  pages_questions_dict[1] = None
  current_question_id_arr = []    # arr
  for i in all_question_uuids_arr:
    if question_counter >= num_questions_per_page:
      pages_questions_dict[current_page_num] = current_question_id_arr
      current_question_id_arr = []
      question_counter = 0
      current_page_num += 1
      pages_questions_dict[current_page_num] = None
    question_counter += 1
    question_uuid = i[0]    # str
    current_question_id_arr.append(question_uuid)
    if current_page_num > total_num_of_pages:
      pages_questions_dict[current_page_num] = current_question_id_arr
    elif current_page_num == total_num_of_pages:
      pages_questions_dict[current_page_num] = current_question_id_arr
  # ------------------------ Break Down to Pages of arr dict END ------------------------
  # ------------------------ Specify Exact Page START ------------------------
  selected_page_question_uuid_arr = pages_questions_dict[desired_page_number]
  len_selected_page_question_uuid_arr = len(selected_page_question_uuid_arr)
  selected_page_question_uuid_str = ''
  for i in range(len(selected_page_question_uuid_arr)):
    if i == len_selected_page_question_uuid_arr - 1:
      selected_page_question_uuid_str += f"'{selected_page_question_uuid_arr[i]}'"
    else:
      selected_page_question_uuid_str += f"'{selected_page_question_uuid_arr[i]}'" + ", "
  # ------------------------ Specify Exact Page END ------------------------
  # ------------------------ Pull created questions from user START ------------------------
  # Pull created question info from db
  user_all_questions_submitted_dict = select_all_questions_created_by_owner_specific_page_function(postgres_connection, postgres_cursor, user_uuid, selected_page_question_uuid_str)
  # ------------------------ Pull created questions from user END ------------------------
  # ------------------------ Close DB START ------------------------
  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Close DB END ------------------------


  for i in user_all_questions_submitted_dict:
    # ------------------------ CSS fix for category colors START ------------------------
    # Create and append category colors for end user css
    categories_arr_to_html = datatype_change_categories_list_str_to_tuple_function(i['question_categories_list'])
    i['question_categories_list_arr'] = categories_arr_to_html
    # ------------------------ CSS fix for category colors END ------------------------
  
  
  # ------------------------ Add page logic for HTML/CSS START ------------------------
  # Page number presentation logic
  total_num_of_pages_fix = total_num_of_pages + 1
  if desired_page_number == 1 and total_num_of_pages_fix == 1:
    page_previous_number = ''
    page_next_number = ''
  if desired_page_number == 1 and total_num_of_pages == 1:
    page_previous_number = ''
    page_next_number = ''
  elif desired_page_number == 1 or total_num_of_pages_fix == 1:
    page_previous_number = ''
    page_next_number = desired_page_number + 1
  elif desired_page_number == total_num_of_pages_fix:
    page_previous_number = desired_page_number - 1
    page_next_number = ''
  else:
    page_previous_number = desired_page_number - 1
    page_next_number = desired_page_number + 1
  # Append to arr for html
  created_question_page_numbers_arr = []
  created_question_page_numbers_arr.append(page_previous_number)
  created_question_page_numbers_arr.append(desired_page_number)
  created_question_page_numbers_arr.append(page_next_number)
  # ------------------------ Add page logic for HTML/CSS END ------------------------

  
  localhost_print_function('=========================================== /create/question/user/form/submit/success/<html_variable_created_question_page_number> Page END ===========================================')
  return render_template('employee_engagement_page_templates/create_question_page_templates/create_question_submission_page_templates/create_question_submission_success.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          user_email_to_html = user_email,
                          user_all_submitted_questions_html = user_all_questions_submitted_dict,
                          free_trial_ends_info_to_html = free_trial_ends_info,
                          created_question_page_numbers_arr_to_html = created_question_page_numbers_arr,
                          page_title_to_html = 'Submitted Questions')



# ------------------------ After - Do Not Cache Image URL START ------------------------
# No caching at all for API endpoints.
@create_question_submission_success_page_render_template.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
# ------------------------ After - Do Not Cache Image URL END ------------------------
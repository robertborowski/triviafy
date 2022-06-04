# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_all_questions_table.select_all_questions_created_by_owner_email import select_all_questions_created_by_owner_email_function
import os
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
create_question_submission_success_page_render_template = Blueprint("create_question_submission_success_page_render_template", __name__, static_folder="static", template_folder="templates")
@create_question_submission_success_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@create_question_submission_success_page_render_template.route("/create/question/user/form/submit/success", methods=['GET','POST'])
def create_question_submission_success_page_render_template_function():
  localhost_print_function('=========================================== /create/question/user/form/submit/success Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/create/question/user/form/submit/success')
    # Redirects based on returned value - pre load checks
    if user_nested_dict == '/subscription':
      return redirect('/subscription', code=302)
    elif user_nested_dict == '/notifications/email/permission':
      return redirect('/notifications/email/permission', code=302)
    elif user_nested_dict == '/new/user/questionnaire':
      return redirect('/new/user/questionnaire', code=302)
    elif user_nested_dict == '/logout':
      return redirect('/logout', code=302)
    # ------------------------ Pre Load Page Checks END ------------------------


    # ------------------------ Page Company Info START ------------------------
    user_company_name = user_nested_dict['user_company_name']
    user_company_name = sanitize_page_output_company_name_function(user_company_name)
    user_channel_name = user_nested_dict['slack_channel_name']
    # ------------------------ Page Company Info END ------------------------
    
    # Get additional variables
    user_email = user_nested_dict['user_email']
    user_uuid = user_nested_dict['user_uuid']

  except:
    localhost_print_function('page load except error hit - /create/question/user/form/submit/success Page')
    localhost_print_function('=========================================== /create/question/user/form/submit/success Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)

  """
  # ------------------------ Check create question accesss START ------------------------
  # Get personal email
  personal_email = os.environ.get('PERSONAL_EMAIL')

  # If user does not have access to create questions then redirect to waitlist page
  if user_email != personal_email:
    localhost_print_function('redirecting to the create question wait list page!')
    localhost_print_function('=========================================== /create/question/user/form/submit/success Page END ===========================================')
    return redirect('/create/question/user/waitlist', code=302)
  # ------------------------ Check create question accesss END ------------------------
  """
  
  # ------------------------ Pull created questions from user START ------------------------
  # Pull all questions submitted by this user
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()

  # Pull info from db
  user_all_questions_submitted_dict = select_all_questions_created_by_owner_email_function(postgres_connection, postgres_cursor, user_uuid)

  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Pull created questions from user END ------------------------


  # ------------------------ CSS fix for category colors START ------------------------
  for i in user_all_questions_submitted_dict:
    categories_str = i['question_categories_list']
    categories_str_fixed = categories_str.replace(', ',',')
    categories_arr = categories_str_fixed.split(',')
    categories_arr_to_html = []
    for category in categories_arr:
      category_lower = category.lower()
      category_replace_space = category_lower.replace(' ','_')
      categories_arr_to_html.append((category, category_replace_space))
    i['question_categories_list_arr'] = categories_arr_to_html
  # ------------------------ CSS fix for category colors END ------------------------

  
  localhost_print_function('=========================================== /create/question/user/form/submit/success Page END ===========================================')
  return render_template('create_question_page_templates/create_question_submission_page_templates/create_question_submission_success.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          user_email_to_html = user_email,
                          user_all_submitted_questions_html = user_all_questions_submitted_dict,
                          free_trial_ends_info_to_html = free_trial_ends_info)



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
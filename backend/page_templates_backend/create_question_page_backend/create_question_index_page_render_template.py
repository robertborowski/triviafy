# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
import os
from datetime import date
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_all_questions_table.select_triviafy_all_questions_table_created_team_channel_combo import select_triviafy_all_questions_table_created_team_channel_combo_function

# -------------------------------------------------------------- App Setup
create_question_index_page_render_template = Blueprint("create_question_index_page_render_template", __name__, static_folder="static", template_folder="templates")
@create_question_index_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@create_question_index_page_render_template.route("/create/question/user/form", methods=['GET','POST'])
def create_question_index_page_render_template_function():
  localhost_print_function('=========================================== /create/question/user/form Page START ===========================================')
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/create/question/user/form')
    # Redirects based on returned value - pre load checks
    if user_nested_dict == '/subscription':
      return redirect('/subscription', code=302)
    elif user_nested_dict == '/notifications/email/permission':
      return redirect('/notifications/email/permission', code=302)
    elif user_nested_dict == '/new/user/questionnaire':
      return redirect('/new/user/questionnaire', code=302)
    elif user_nested_dict == '/categories/edit':
      return redirect('/categories/edit', code=302)
    elif user_nested_dict == '/logout':
      return redirect('/logout', code=302)
    # ------------------------ Pre Load Page Checks END ------------------------

    
    # ------------------------ Page Company Info START ------------------------
    user_company_name = user_nested_dict['user_company_name']
    user_company_name = sanitize_page_output_company_name_function(user_company_name)
    user_channel_name = user_nested_dict['user_slack_channel_name']
    # ------------------------ Page Company Info END ------------------------
    
    # Get additional variables
    user_email = user_nested_dict['user_email']
    question_author_team_id = user_nested_dict['user_slack_workspace_team_id']
    question_author_channel_id = user_nested_dict['user_slack_channel_id']


    # ------------------------ Get Today's Date Information START ------------------------
    # Today's date
    today_date = date.today()
    today_date_split_arr = str(today_date).split('-')
    # Separate Today's date into year month and day
    today_date_year = today_date_split_arr[0]
    today_date_month = today_date_split_arr[1]
    # ------------------------ Get Today's Date Information END ------------------------


    # ------------------------ Check Team Channel Combo Count START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()

    # Build in Check here!
    num_of_questions_created_team_channel_combo = select_triviafy_all_questions_table_created_team_channel_combo_function(postgres_connection, postgres_cursor, question_author_team_id, question_author_channel_id, today_date_year, today_date_month)
    
    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Check Team Channel Combo Count END ------------------------


    # ------------------------ Redirect If Too Many Questions START ------------------------
    # This is a variable in TWO .py files
    limit_amount = 50
    if num_of_questions_created_team_channel_combo >= limit_amount:
      localhost_print_function('redirecting to the create question wait list page!')
      localhost_print_function('=========================================== /create/question/user/form Page END ===========================================')
      return redirect('/create/question/limit', code=302)
    # ------------------------ Redirect If Too Many Questions END ------------------------

  except:
    localhost_print_function('page load except error hit - /create/question/user/form Page')
    localhost_print_function('=========================================== /create/question/user/form Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)
  
  """
  # ------------------------ Check create question accesss START ------------------------
  # Get personal email
  personal_email = os.environ.get('PERSONAL_EMAIL')

  # If user does not have access to create questions then redirect to waitlist page
  if user_email != personal_email:
    localhost_print_function('redirecting to the create question wait list page!')
    localhost_print_function('=========================================== /create/question/user/form Page END ===========================================')
    return redirect('/create/question/user/waitlist', code=302)
  # ------------------------ Check create question accesss END ------------------------
  """
  
  localhost_print_function('=========================================== /create/question/user/form Page END ===========================================')
  return render_template('create_question_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          user_email_to_html = user_email,
                          free_trial_ends_info_to_html = free_trial_ends_info,
                          page_title_to_html = 'Create Question')
# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.insert_queries.insert_queries_triviafy_quiz_feedback_responses_table.insert_triviafy_quiz_feedback_responses_table import insert_triviafy_quiz_feedback_responses_table_function
from backend.utils.sanitize_user_inputs.sanitize_feedback_user import sanitize_feedback_user_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
quiz_feedback_processing = Blueprint("quiz_feedback_processing", __name__, static_folder="static", template_folder="templates")
@quiz_feedback_processing.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@quiz_feedback_processing.route("/quiz/team/feedback/processing", methods=['GET','POST'])
def quiz_feedback_processing_function():
  localhost_print_function('=========================================== /quiz/team/feedback/processing Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/quiz/team/feedback/processing')
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
      return redirect('/employees/logout', code=302)
    # ------------------------ Pre Load Page Checks END ------------------------
    
    
    user_uuid = user_nested_dict['user_uuid']


    # ------------------------ Get Form User Input START ------------------------
    # NOTE: Need to sanitize this before production
    user_input_feedback_form = sanitize_feedback_user_function(request.form.get('user_input_quiz_feedback'))
    # ------------------------ Get Form User Input END ------------------------


    # ------------------------ Create Variables for DB START ------------------------
    user_feedback_uuid = create_uuid_function('feedbckid_')
    user_feedback_timestamp = create_timestamp_function()
    # ------------------------ Create Variables for DB END ------------------------


    # ------------------------ Upload Feedback to DB START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()
    
    # Insert feedback to DB
    output_message = insert_triviafy_quiz_feedback_responses_table_function(postgres_connection, postgres_cursor, user_feedback_uuid, user_feedback_timestamp, user_uuid, user_input_feedback_form)
    
    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Upload Feedback to DB END ------------------------

    
  except:
    localhost_print_function('page load except error hit - /quiz/team/feedback/processing Page')
    localhost_print_function('=========================================== /quiz/team/feedback/processing Page END ===========================================')
    return redirect('/employees/logout', code=302)
    # return redirect('/', code=302)

  
  localhost_print_function('=========================================== /quiz/team/feedback/processing Page END ===========================================')
  return redirect('/quiz/team/feedback/submit', code=302)
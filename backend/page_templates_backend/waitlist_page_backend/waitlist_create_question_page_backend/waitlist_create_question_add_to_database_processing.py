# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.insert_queries.insert_queries_triviafy_waitlist_create_question_table.insert_triviafy_waitlist_create_question_table import insert_triviafy_waitlist_create_question_table_function
from backend.db.queries.select_queries.select_queries_triviafy_waitlist_create_question_table.select_triviafy_waitlist_create_question_table_check_if_uuid_exists import select_triviafy_waitlist_create_question_table_check_if_uuid_exists_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
waitlist_create_question_add_to_database_processing = Blueprint("waitlist_create_question_add_to_database_processing", __name__, static_folder="static", template_folder="templates")
@waitlist_create_question_add_to_database_processing.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@waitlist_create_question_add_to_database_processing.route("/create/question/user/waitlist/processing", methods=['GET','POST'])
def waitlist_create_question_add_to_database_processing_function():
  localhost_print_function('=========================================== /create/question/user/waitlist/processing Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/create/question/user/waitlist/processing')
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

    user_email = user_nested_dict['user_email']
    user_uuid = user_nested_dict['user_uuid']

  except:
    localhost_print_function('page load except error hit - /create/question/user/waitlist/processing Page')
    localhost_print_function('=========================================== /create/question/user/waitlist/processing Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)


  # ------------------------ Check if user is already on this waitlist START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  
  if_uuid_exists = select_triviafy_waitlist_create_question_table_check_if_uuid_exists_function(postgres_connection, postgres_cursor, user_uuid)

  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)

  if if_uuid_exists == True:
    localhost_print_function('redirecting user to the confirm waitlist page')
    localhost_print_function('=========================================== /create/question/user/waitlist/processing Page END ===========================================')
    return redirect('/create/question/user/waitlist/confirm', code=302)
  # ------------------------ Check if user is already on this waitlist END ------------------------
  
  
  # ------------------------ Create additional DB variables START ------------------------
  waitlist_create_question_uuid = create_uuid_function('wait_quest_')
  waitlist_create_question_timestamp = create_timestamp_function()
  # ------------------------ Create additional DB variables END ------------------------


  # ------------------------ Add user uuid to create question waitlist database START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()

  # DB insert attempt
  insert_triviafy_waitlist_create_question_table_function(postgres_connection, postgres_cursor, waitlist_create_question_uuid, waitlist_create_question_timestamp, user_uuid)

  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Add user uuid to create question waitlist database END ------------------------

  localhost_print_function('=========================================== /create/question/user/waitlist/processing Page END ===========================================')
  localhost_print_function('redirecting user to the confirm waitlist page')
  return redirect('/create/question/user/waitlist/confirm', code=302)
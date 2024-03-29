# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_waitlist_create_question_table.select_triviafy_waitlist_create_question_table_check_if_uuid_exists import select_triviafy_waitlist_create_question_table_check_if_uuid_exists_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
waitlist_create_question_page_render_template = Blueprint("waitlist_create_question_page_render_template", __name__, static_folder="static", template_folder="templates")
@waitlist_create_question_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@waitlist_create_question_page_render_template.route("/create/question/user/waitlist", methods=['GET','POST'])
def waitlist_create_question_page_render_template_function():
  localhost_print_function('=========================================== /create/question/user/waitlist Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/create/question/user/waitlist')
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


    user_email = user_nested_dict['user_email']
    user_uuid = user_nested_dict['user_uuid']

  except:
    localhost_print_function('page load except error hit - /create/question/user/waitlist Page')
    localhost_print_function('=========================================== /create/question/user/waitlist Page END ===========================================')
    return redirect('/employees/logout', code=302)
    # return redirect('/', code=302)


  # ------------------------ Check if user is already on this waitlist START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  
  if_uuid_exists = select_triviafy_waitlist_create_question_table_check_if_uuid_exists_function(postgres_connection, postgres_cursor, user_uuid)

  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)

  if if_uuid_exists == True:
    localhost_print_function('redirecting user to the confirm waitlist')
    localhost_print_function('=========================================== /create/question/waitlist/confirm Page END ===========================================')
    return redirect('/create/question/user/waitlist/confirm', code=302)
  # ------------------------ Check if user is already on this waitlist END ------------------------

  
  localhost_print_function('=========================================== /create/question/user/waitlist Page END ===========================================')
  return render_template('employee_engagement_page_templates/waitlist_page_templates/waitlist_create_question_page_template/index.html',
                          css_cache_busting = cache_busting_output,
                          user_email_html = user_email,
                          free_trial_ends_info_to_html = free_trial_ends_info)
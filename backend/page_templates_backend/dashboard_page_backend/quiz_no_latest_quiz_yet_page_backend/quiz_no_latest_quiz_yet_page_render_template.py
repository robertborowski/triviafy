# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.latest_quiz_utils.get_latest_company_quiz_if_exists import get_latest_company_quiz_if_exists_function
from backend.db.queries.select_queries.select_queries_triviafy_company_quiz_settings_slack_table.select_company_quiz_settings import select_company_quiz_settings_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.latest_quiz_utils.get_previous_week_company_quiz_if_exists import get_previous_week_company_quiz_if_exists_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function
from backend.utils.latest_quiz_utils.check_if_today_is_greater_than_equal_to_latest_quiz_start_date_utils.check_if_today_is_greater_than_equal_to_latest_quiz_start_date import check_if_today_is_greater_than_equal_to_latest_quiz_start_date_function

# -------------------------------------------------------------- App Setup
quiz_no_latest_quiz_yet_page_render_template = Blueprint("quiz_no_latest_quiz_yet_page_render_template", __name__, static_folder="static", template_folder="templates")
@quiz_no_latest_quiz_yet_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@quiz_no_latest_quiz_yet_page_render_template.route("/dashboard/quiz/first/pending", methods=['GET','POST'])
def quiz_no_latest_quiz_yet_page_render_template_function():
  localhost_print_function('=========================================== /dashboard/quiz/first/pending Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/dashboard/quiz/first/pending')
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
    slack_workspace_team_id = user_nested_dict['user_slack_workspace_team_id']
    slack_channel_id = user_nested_dict['user_slack_channel_id']

    # ------------------------ If Latest Company Quiz Obj None START ------------------------
    # Make sure that there is no latest company quiz if someone goes to this URL
    latest_company_quiz_object = get_latest_company_quiz_if_exists_function(user_nested_dict)

    if latest_company_quiz_object != None:
      localhost_print_function('latest_company_quiz_object is != None. Redirecting to dashboard')
      localhost_print_function('=========================================== /dashboard/quiz/first/pending Page END ===========================================')
      return redirect('/dashboard', code=302)
    # ------------------------ If Latest Company Quiz Obj None END ------------------------


    # ------------------------ Check If Previous Week is None too START ------------------------
    if latest_company_quiz_object == None:
      # Check if there is a previous week quiz made
      previous_week_company_quiz_object = get_previous_week_company_quiz_if_exists_function(user_nested_dict)
      if previous_week_company_quiz_object != None:
        localhost_print_function('previous_week_company_quiz_object is != None. Redirecting to dashboard')
        localhost_print_function('=========================================== /dashboard/quiz/first/pending Page END ===========================================')
        return redirect('/dashboard', code=302)
    # ------------------------ Check if This Is Companies First Every Quiz END ------------------------
    # ------------------------ Check If Previous Week is None too END ------------------------


    # ------------------------ Get The Company Quiz Settings START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()

    # Get quiz settings from DB as arr
    quiz_settings_arr = select_company_quiz_settings_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)
    # Assign the arr values
    company_quiz_settings_last_updated_timestamp = quiz_settings_arr[1]
    company_quiz_settings_start_day = quiz_settings_arr[2]
    company_quiz_settings_start_time = quiz_settings_arr[3]
    company_quiz_settings_end_day = quiz_settings_arr[4]
    company_quiz_settings_end_time = quiz_settings_arr[5]
    company_quiz_settings_questions_per_quiz = quiz_settings_arr[6]

    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Get The Company Quiz Settings END ------------------------


    # ------------------------ Check Date Time Comparison START ------------------------
    quiz_begin_message = 'hello'
    check_if_quiz_is_open_datetime = check_if_today_is_greater_than_equal_to_latest_quiz_start_date_function(company_quiz_settings_start_day, company_quiz_settings_start_time)
    if check_if_quiz_is_open_datetime == True:
      quiz_begin_message = 'Your weekly quiz should be open within 10 minutes. No action is needed on your end.'
    else:
      quiz_begin_message = f'Your weekly quiz will open on {company_quiz_settings_start_day} at {company_quiz_settings_start_time}.'
    # ------------------------ Check Date Time Comparison END ------------------------


  except:
    localhost_print_function('page load except error hit - /dashboard/quiz/first/pending Page')
    localhost_print_function('=========================================== /dashboard/quiz/first/pending Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)


  
  localhost_print_function('=========================================== /dashboard/quiz/first/pending Page END ===========================================')
  return render_template('employee_engagement_page_templates/dashboard_page_templates/quiz_no_latest_quiz_yet_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          quiz_begin_message_to_html = quiz_begin_message,
                          free_trial_ends_info_to_html = free_trial_ends_info,
                          page_title_to_html = 'Welcome to Triviafy')
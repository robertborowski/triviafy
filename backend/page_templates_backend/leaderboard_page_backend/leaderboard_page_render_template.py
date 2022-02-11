# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_company_users import select_company_users_function
from backend.db.queries.select_queries.select_queries_joined_tables.select_total_user_quiz_wins import select_total_user_quiz_wins_function
from backend.db.queries.select_queries.select_queries_joined_tables.select_total_user_correct_quiz_answers import select_total_user_correct_quiz_answers_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.latest_quiz_utils.get_latest_company_quiz_if_exists import get_latest_company_quiz_if_exists_function
from backend.utils.datetime_utils.check_if_quiz_is_past_due_datetime import check_if_quiz_is_past_due_datetime_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
leaderboard_page_render_template = Blueprint("leaderboard_page_render_template", __name__, static_folder="static", template_folder="templates")
@leaderboard_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@leaderboard_page_render_template.route("/leaderboard", methods=['GET','POST'])
def leaderboard_page_render_template_function():
  localhost_print_function('=========================================== /leaderboard Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/leaderboard')
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
    slack_workspace_team_id = user_nested_dict['slack_team_id']
    slack_channel_id = user_nested_dict['slack_channel_id']


    # ------------------------ Get All Users From Company START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()

    # Get the UUID and Display name of all users at this company/team/channel
    company_users_arr = select_company_users_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)


    # ------------------------ Get Latest Quiz ID For Company START ------------------------
    # Dict for latest company quiz
    function_input_dict = {
      'slack_team_id' : slack_workspace_team_id,
      'slack_channel_id' : slack_channel_id 
    }
    # Check if a quiz was already made for this company
    latest_company_quiz_object = get_latest_company_quiz_if_exists_function(function_input_dict)

    if latest_company_quiz_object == None:
      # Nothing to exclude from correct answer count
      company_latest_quiz_id = ''
    # ------------------------ Get Latest Quiz ID For Company END ------------------------


    # ------------------------ Check If Quiz Is Past Due START ------------------------
    if latest_company_quiz_object != None:
      # Exclude from correct answer count
      company_latest_quiz_id = latest_company_quiz_object[0]
      quiz_end_date = latest_company_quiz_object[7].strftime('%Y-%m-%d')            # str
      quiz_end_time = latest_company_quiz_object[9]                                 # str

      quiz_is_past_due_date = check_if_quiz_is_past_due_datetime_function(quiz_end_date, quiz_end_time)

      if quiz_is_past_due_date != None:
        # Nothing to exclude from correct answer count
        company_latest_quiz_id = ''
    # ------------------------ Check If Quiz Is Past Due END ------------------------


    # Master array of dicts for the Leaderboard datatables html
    users_leaderboard_arr_of_dicts = []

    for i in company_users_arr:
      # Create empty dict to store leaderboard results
      users_leaderboard_dict = {}

      # Set variables from arr pull
      user_uuid = i[0]
      user_name = i[1].replace('_',' ')
      # Get total quiz wins for each user
      total_user_wins_arr = select_total_user_quiz_wins_function(postgres_connection, postgres_cursor, user_uuid)
      total_user_wins_int = int(total_user_wins_arr[0])
      # Get total correct answers for each user
      total_user_correct_quiz_answers_arr = select_total_user_correct_quiz_answers_function(postgres_connection, postgres_cursor, user_uuid, company_latest_quiz_id)
      total_user_correct_quiz_answers_int = int(total_user_correct_quiz_answers_arr[0])

      # Set the dictionary values for user
      users_leaderboard_dict['name'] = user_name
      users_leaderboard_dict['total_user_wins_int'] = total_user_wins_int
      users_leaderboard_dict['total_user_correct_quiz_answers_int'] = total_user_correct_quiz_answers_int

      # Append the dict to a master arr
      users_leaderboard_arr_of_dicts.append(users_leaderboard_dict)
      # ------------------------ Get All Users From Company END ------------------------

    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)


  except:
    localhost_print_function('page load except error hit - /leaderboard Page')
    localhost_print_function('=========================================== /leaderboard Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)


  
  localhost_print_function('=========================================== /leaderboard Page END ===========================================')
  return render_template('leaderboad_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          users_leaderboard_arr_of_dicts_to_html = users_leaderboard_arr_of_dicts,
                          free_trial_ends_info_to_html = free_trial_ends_info)
# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.db.queries.select_queries.select_queries_triviafy_company_quiz_settings_slack_table.select_company_quiz_settings import select_company_quiz_settings_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.sanitize_user_inputs.sanitize_edit_quiz_setting_day import sanitize_edit_quiz_setting_day_function
from backend.utils.sanitize_user_inputs.sanitize_edit_quiz_setting_time import sanitize_edit_quiz_setting_time_function
from backend.utils.sanitize_user_inputs.sanitize_edit_quiz_setting_num_questions import sanitize_edit_quiz_setting_num_questions_function
from backend.db.queries.update_queries.update_queries_triviafy_company_quiz_settings_slack_table.update_edit_quiz_settings import update_edit_quiz_settings_function
from backend.utils.quiz_settings_page_utils.convert_form_results_to_db_inputs import convert_form_results_to_db_inputs_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
edit_quiz_settings_submit_new_quiz_settings = Blueprint("edit_quiz_settings_submit_new_quiz_settings", __name__, static_folder="static", template_folder="templates")
@edit_quiz_settings_submit_new_quiz_settings.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@edit_quiz_settings_submit_new_quiz_settings.route("/quiz/team/settings/payment/admin/edit/submit/processing", methods=['GET','POST'])
def edit_quiz_settings_submit_new_quiz_settings_function():
  localhost_print_function('=========================================== /quiz/team/settings/payment/admin/edit/submit/processing Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/quiz/team/settings/payment/admin/edit/submit/processing')
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

    # Get Company name and channel name (slack ID's)
    slack_workspace_team_id = user_nested_dict['user_slack_workspace_team_id']
    slack_channel_id = user_nested_dict['user_slack_channel_id']
    

    # ------------------------ Check if user is payment admin in START ------------------------
    # See if user is payment admin. If not then they cannot edit quiz settings
    user_payment_admin_status = user_nested_dict['user_is_payment_admin_teamid_channelid']
    if user_payment_admin_status != True:
      localhost_print_function('User is not a payment admin on their team/channel ID combo')
      localhost_print_function('=========================================== /quiz/team/settings/payment/admin/edit/submit/processing Page END ===========================================')
      return redirect('/quiz/team/settings', code=302)
    # ------------------------ Check if user is payment admin in END ------------------------


    # ------------------------ Get Quiz Settings Form Inputs START ------------------------
    # Get the user form data and sanitize it in the same line
    user_form_input_quiz_start_day = sanitize_edit_quiz_setting_day_function(request.form.get('edit-quiz-start-day'))
    user_form_input_quiz_start_time = sanitize_edit_quiz_setting_time_function(request.form.get('edit-quiz-start-time'))
    user_form_input_quiz_end_day = sanitize_edit_quiz_setting_day_function(request.form.get('edit-quiz-end-day'))
    user_form_input_quiz_end_time = sanitize_edit_quiz_setting_time_function(request.form.get('edit-quiz-end-time'))
    user_form_input_quiz_num_questions = sanitize_edit_quiz_setting_num_questions_function(request.form.get('edit-quiz-num-questions'))

    # ------------------------ Invalid Inputs START ------------------------
    if user_form_input_quiz_start_day == None or user_form_input_quiz_start_time == None or user_form_input_quiz_end_day == None or user_form_input_quiz_end_time == None or user_form_input_quiz_num_questions == None:
      localhost_print_function('=========================================== /quiz/team/settings/payment/admin/edit/submit/processing Page END ===========================================')
      return redirect('/', code=302)
    # ------------------------ Invalid Inputs END ------------------------

    # Change the form input str to an int
    if user_form_input_quiz_num_questions == 'five_questions':
      user_form_input_quiz_num_questions = 5
    if user_form_input_quiz_num_questions == 'ten_questions':
      user_form_input_quiz_num_questions = 10

    # ------------------------ Form Start End Logic START ------------------------
    # Logic behind the form, End Date/Time cannot be before Start Day/Time
    quiz_settings_logic_day_dict = {
      'monday' : 1,
      'tuesday' : 2,
      'wednesday' : 3,
      'thursday' : 4,
      'friday' : 5
    }
    quiz_settings_logic_time_dict = {
      'one_am' : 1,
      'two_am' : 2,
      'three_am' : 3,
      'four_am' : 4,
      'five_am' : 5,
      'six_am' : 6,
      'seven_am' : 7,
      'eight_am' : 8,
      'nine_am' : 9,
      'ten_am' : 10,
      'eleven_am' : 11,
      'noon' : 12,
      'one_pm' : 13,
      'two_pm' : 14,
      'three_pm' : 15,
      'four_pm' : 16,
      'five_pm' : 17,
      'six_pm' : 18,
      'seven_pm' : 19,
      'eight_pm' : 20,
      'nine_pm' : 21,
      'ten_pm' : 22,
      'eleven_pm' : 23
    }

    # Check if days make sense
    quiz_start_day_index = quiz_settings_logic_day_dict[user_form_input_quiz_start_day]
    quiz_end_day_index = quiz_settings_logic_day_dict[user_form_input_quiz_end_day]
    if quiz_end_day_index < quiz_start_day_index:
      # Switch start and end day
      temp_end_day = user_form_input_quiz_end_day
      user_form_input_quiz_end_day = user_form_input_quiz_start_day
      user_form_input_quiz_start_day = temp_end_day
    
    # Check if time is the same on the same day error
    if (user_form_input_quiz_start_time == user_form_input_quiz_end_time) and (user_form_input_quiz_start_day == user_form_input_quiz_end_day):
      localhost_print_function('quiz start/end time cannot be the same on the same day')
      localhost_print_function('=========================================== /quiz/team/settings/payment/admin/edit/submit/processing Page END ===========================================')
      return redirect('/quiz/team/settings', code=302)
    
    # Check if quiz times make sense
    quiz_start_time_index = quiz_settings_logic_time_dict[user_form_input_quiz_start_time]
    quiz_end_time_index = quiz_settings_logic_time_dict[user_form_input_quiz_end_time]
    if (user_form_input_quiz_start_day == user_form_input_quiz_end_day) and (quiz_end_time_index < quiz_start_time_index):
      # Switch start and end time
      temp_end_time = user_form_input_quiz_end_time
      user_form_input_quiz_end_time = user_form_input_quiz_start_time
      user_form_input_quiz_start_time = temp_end_time
    # ------------------------ Form Start End Logic END ------------------------
    
    # ------------------------ Convert inputs to database friendly inputs START ------------------------
    converted_start_day, converted_start_time, converted_end_day, converted_end_time = convert_form_results_to_db_inputs_function(user_form_input_quiz_start_day, user_form_input_quiz_start_time, user_form_input_quiz_end_day, user_form_input_quiz_end_time)
    # ------------------------ Convert inputs to database friendly inputs END ------------------------
    # ------------------------ Get Quiz Settings Form Inputs END ------------------------


    # ------------------------ Get Current Quiz Settings DB Info START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()

    # Get quiz settings from DB as arr
    quiz_settings_arr = select_company_quiz_settings_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)
    # Assign the arr values
    uuid_company_quiz_settings = quiz_settings_arr[0]
    # ------------------------ Get Current Quiz Settings DB Info END ------------------------


    # ------------------------ Update Quiz Settings table in DB START ------------------------
    # New timestamp for edited quiz settings
    company_quiz_settings_last_updated_timestamp = create_timestamp_function()

    update_edit_quiz_settings_function(postgres_connection, postgres_cursor, company_quiz_settings_last_updated_timestamp, converted_start_day, converted_start_time, converted_end_day, converted_end_time, user_form_input_quiz_num_questions, uuid_company_quiz_settings)

    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Update Quiz Settings table in DB END ------------------------


  except:
    localhost_print_function('page load except error hit - /quiz/team/settings/payment/admin/edit/submit/processing Page')
    localhost_print_function('=========================================== /quiz/team/settings/payment/admin/edit/submit/processing Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)

  
  localhost_print_function('=========================================== /quiz/team/settings/payment/admin/edit/submit/processing Page END ===========================================')
  return redirect('/quiz/team/settings', code=302)
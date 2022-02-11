# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.latest_quiz_utils.get_latest_company_quiz_if_exists import get_latest_company_quiz_if_exists_function
from backend.utils.latest_quiz_utils.get_previous_week_company_quiz_if_exists import get_previous_week_company_quiz_if_exists_function
from backend.utils.latest_quiz_utils.supporting_make_company_latest_quiz_utils.convert_question_ids_from_string_to_arr import convert_question_ids_from_string_to_arr_function
from backend.db.queries.select_queries.select_queries_triviafy_all_questions_table.select_company_quiz_questions_individually import select_company_quiz_questions_individually_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.page_templates_backend.dashboard_page_backend.get_user_saved_quiz_question_answers import get_user_saved_quiz_question_answers_function
from backend.utils.datetime_utils.check_if_quiz_is_past_due_datetime import check_if_quiz_is_past_due_datetime_function
from backend.utils.latest_quiz_utils.check_if_latest_quiz_is_graded_utils.check_if_latest_quiz_is_graded import check_if_latest_quiz_is_graded_function
from backend.utils.latest_quiz_utils.check_if_today_is_earlier_than_latest_quiz_start_date_utils.check_if_today_is_earlier_than_latest_quiz_start_date import check_if_today_is_earlier_than_latest_quiz_start_date_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
dashboard_index_page_render_template = Blueprint("dashboard_index_page_render_template", __name__, static_folder="static", template_folder="templates")
@dashboard_index_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@dashboard_index_page_render_template.route("/dashboard", methods=['GET','POST'])
def dashboard_index_page_render_template_function():
  localhost_print_function('=========================================== /dashboard Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/dashboard')
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


    # Get user information from the nested dict
    slack_workspace_team_id = user_nested_dict['slack_team_id']
    slack_channel_id = user_nested_dict['slack_channel_id']
    user_uuid = user_nested_dict['user_uuid']


    # ------------------------ Page Company Info START ------------------------
    user_company_name = user_nested_dict['user_company_name']
    user_company_name = sanitize_page_output_company_name_function(user_company_name)
    user_channel_name = user_nested_dict['slack_channel_name']
    # ------------------------ Page Company Info END ------------------------


    # ------------------------ Check if This Is Companies First Every Quiz START ------------------------
    # Check if there is a latest quiz (made on sundays)
    latest_company_quiz_object = get_latest_company_quiz_if_exists_function(user_nested_dict)
    if latest_company_quiz_object == None:
      # Check if there is a previous week quiz made
      previous_week_company_quiz_object = get_previous_week_company_quiz_if_exists_function(user_nested_dict)
      if previous_week_company_quiz_object == None:
        # This means a company signed up after Sunday
        localhost_print_function('=========================================== /dashboard Page END ===========================================')
        localhost_print_function('redirecting to thank you first signed up page')
        return redirect('/dashboard/quiz/first/pending', code=302)
    # ------------------------ Check if This Is Companies First Every Quiz END ------------------------
    

    # ------------------------ Set Variables for Checks/Outputs START ------------------------
    if latest_company_quiz_object != None:
      # Assign the variables for the HTML inputs based on the pulled object
      uuid_quiz = latest_company_quiz_object[0]                                     # str
      quiz_timestamp_created = latest_company_quiz_object[1].strftime('%Y-%m-%d')   # str
      quiz_slack_team_id = latest_company_quiz_object[2]                            # str
      quiz_slack_channel_id = latest_company_quiz_object[3]                         # str
      quiz_start_date = latest_company_quiz_object[4].strftime('%Y-%m-%d')          # str
      quiz_start_day_of_week = latest_company_quiz_object[5]                        # str
      quiz_start_time = latest_company_quiz_object[6]                               # str
      quiz_end_date = latest_company_quiz_object[7].strftime('%Y-%m-%d')            # str
      quiz_end_day_of_week = latest_company_quiz_object[8]                          # str
      quiz_end_time = latest_company_quiz_object[9]                                 # str
      quiz_number_of_questions = latest_company_quiz_object[10]                     # int
      quiz_question_ids_str = latest_company_quiz_object[11]                        # str
      quiz_company_quiz_count = latest_company_quiz_object[12]                      # int

      # Quiz Question ID's have to be converted from 1 string to an arr
      quiz_question_ids_arr = convert_question_ids_from_string_to_arr_function(quiz_question_ids_str)   # list
    
    if latest_company_quiz_object == None:
      if previous_week_company_quiz_object != None:
        # Assign the variables for the HTML inputs based on the pulled object
        uuid_quiz = previous_week_company_quiz_object[0]                                     # str
        quiz_timestamp_created = previous_week_company_quiz_object[1].strftime('%Y-%m-%d')   # str
        quiz_slack_team_id = previous_week_company_quiz_object[2]                            # str
        quiz_slack_channel_id = previous_week_company_quiz_object[3]                         # str
        quiz_start_date = previous_week_company_quiz_object[4].strftime('%Y-%m-%d')          # str
        quiz_start_day_of_week = previous_week_company_quiz_object[5]                        # str
        quiz_start_time = previous_week_company_quiz_object[6]                               # str
        quiz_end_date = previous_week_company_quiz_object[7].strftime('%Y-%m-%d')            # str
        quiz_end_day_of_week = previous_week_company_quiz_object[8]                          # str
        quiz_end_time = previous_week_company_quiz_object[9]                                 # str
        quiz_number_of_questions = previous_week_company_quiz_object[10]                     # int
        quiz_question_ids_str = previous_week_company_quiz_object[11]                        # str
        quiz_company_quiz_count = previous_week_company_quiz_object[12]                      # int

        # Quiz Question ID's have to be converted from 1 string to an arr
        quiz_question_ids_arr = convert_question_ids_from_string_to_arr_function(quiz_question_ids_str)   # list
    # ------------------------ Set Variables for Checks/Outputs START ------------------------


    # ------------------------ Check If Quiz Is Past Due Date START ------------------------
    quiz_is_past_due_date = check_if_quiz_is_past_due_datetime_function(quiz_end_date, quiz_end_time)
    if quiz_is_past_due_date == True:
      # ------------------------ Check If Latest Quiz Is Graded START ------------------------
      latest_quiz_is_graded_check = check_if_latest_quiz_is_graded_function(slack_workspace_team_id, slack_channel_id, uuid_quiz)
      if latest_quiz_is_graded_check == True:
        localhost_print_function('=========================================== /dashboard Page END ===========================================')
        localhost_print_function('redirecting to the results page')
        return redirect('/dashboard/quiz/results', code=302)
      
      # ------------------------ Check If Latest Quiz Is Graded END ------------------------
      localhost_print_function('=========================================== /dashboard Page END ===========================================')
      localhost_print_function('redirecting to quiz past due page')
      return redirect('/dashboard/quiz/past/due', code=302)
    # ------------------------ Check If Quiz Is Past Due Date END ------------------------

    
    # ------------------------ Check If Pre Quiz Block View Date START ------------------------
    today_is_earlier_than_start_date = check_if_today_is_earlier_than_latest_quiz_start_date_function(quiz_start_day_of_week, quiz_start_time)
    if today_is_earlier_than_start_date == True:
      localhost_print_function('=========================================== /dashboard Page END ===========================================')
      localhost_print_function('redirecting to quiz not yet open page')
      return redirect('/dashboard/quiz/pre/open', code=302)
    # ------------------------ Check If Pre Quiz Block View Date END ------------------------


    # ------------------------ Pull the Quiz Questions START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()

    # Pull the quiz questions by id's found in the quiz_question_ids_arr
    quiz_questions_obj_arr_of_dicts = []
    for question_id in quiz_question_ids_arr:
      # Select query to pull the questions in the correct order
      quiz_question_dict = select_company_quiz_questions_individually_function(postgres_connection, postgres_cursor, question_id)
      quiz_questions_obj_arr_of_dicts.append(quiz_question_dict[0])


    # Add current question count to the dictionary for html
    current_count = 0
    for i in quiz_questions_obj_arr_of_dicts:
      current_count += 1
      i['quiz_question_number'] = current_count
    # ------------------------ Pull the Quiz Questions END ------------------------


    # ------------------------ Pull the Quiz User Answers If Exist START ------------------------
    user_quiz_saved_answers_dict = get_user_saved_quiz_question_answers_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id, user_uuid, uuid_quiz)

    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Pull the Quiz User Answers If Exist END ------------------------


    # ------------------------ Add User Autofill Answers to Obj START ------------------------
    user_submitted_answers = ''
    if user_quiz_saved_answers_dict != None:
      user_submitted_answers = 'Your answers have been submitted. You can update your answers and resubmit this quiz anytime before its due date/time.'
      for i in quiz_questions_obj_arr_of_dicts:
        i['users_most_recent_submitted_answer'] = user_quiz_saved_answers_dict[i['question_uuid']]
    else:
      user_submitted_answers = ''
      for i in quiz_questions_obj_arr_of_dicts:
        i['users_most_recent_submitted_answer'] = ''
    # ------------------------ Add User Autofill Answers to Obj END ------------------------


  except:
    localhost_print_function('page load except error hit - /dashboard page')
    localhost_print_function('=========================================== /dashboard Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)


  
  localhost_print_function('=========================================== /dashboard Page END ===========================================')
  return render_template('dashboard_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          user_team_latest_quiz_number_to_html = quiz_company_quiz_count,
                          quiz_end_time_to_html = quiz_end_time,
                          quiz_end_day_of_week_to_html = quiz_end_day_of_week,
                          quiz_end_date_to_html = quiz_end_date,
                          user_submitted_answers_to_html = user_submitted_answers,
                          quiz_questions_obj_arr_of_dicts_html = quiz_questions_obj_arr_of_dicts,
                          free_trial_ends_info_to_html = free_trial_ends_info)
# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.utils.latest_quiz_utils.check_if_latest_quiz_is_graded_utils.check_if_latest_quiz_is_graded import check_if_latest_quiz_is_graded_function
from backend.utils.latest_quiz_utils.get_latest_company_quiz_if_exists import get_latest_company_quiz_if_exists_function
from backend.utils.latest_quiz_utils.get_previous_week_company_quiz_if_exists import get_previous_week_company_quiz_if_exists_function
from backend.utils.latest_quiz_utils.supporting_make_company_latest_quiz_utils.convert_question_ids_from_string_to_arr import convert_question_ids_from_string_to_arr_function
from backend.utils.datetime_utils.check_if_quiz_is_past_due_datetime import check_if_quiz_is_past_due_datetime_function
from backend.utils.quiz_calculations_utils.quiz_calculate_quiz_uuid_winner import quiz_calculate_quiz_uuid_winner_function
from backend.utils.quiz_calculations_utils.quiz_winner_insert_to_db import quiz_winner_insert_to_db_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
quiz_graded_end_of_week_view_page_render_template = Blueprint("quiz_graded_end_of_week_view_page_render_template", __name__, static_folder="static", template_folder="templates")
@quiz_graded_end_of_week_view_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@quiz_graded_end_of_week_view_page_render_template.route("/dashboard/quiz/results", methods=['GET','POST'])
def quiz_graded_end_of_week_view_page_render_template_function():
  localhost_print_function('=========================================== /dashboard/quiz/results Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/dashboard/quiz/results')
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

    # ------------------------ Check if This Is Companies First Every Quiz START ------------------------
    # Check if there is a latest quiz (made on sundays)
    latest_company_quiz_object = get_latest_company_quiz_if_exists_function(user_nested_dict)
    if latest_company_quiz_object == None:
      # Check if there is a previous week quiz made
      previous_week_company_quiz_object = get_previous_week_company_quiz_if_exists_function(user_nested_dict)
      if previous_week_company_quiz_object == None:
        # This means a company signed up after Sunday
        localhost_print_function('=========================================== /dashboard/quiz/results Page END ===========================================')
        localhost_print_function('redirecting to thank you first signed up page')
        return redirect('/', code=302)
    # ------------------------ Check if This Is Companies First Every Quiz END ------------------------


    # ------------------------ Set Variables for Checks/Outputs START ------------------------
    if latest_company_quiz_object != None:
      localhost_print_function('assigning variables for the latest graded quiz this week')
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
        localhost_print_function('assigning variables for the previous graded quiz last week')
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


    # ------------------------ Double Check If Quiz Is Past Due Date START ------------------------
    quiz_is_past_due_date = check_if_quiz_is_past_due_datetime_function(quiz_end_date, quiz_end_time)
    # ------------------------ Double Check If Quiz Is Past Due Date END ------------------------
    if quiz_is_past_due_date == True:
      # ------------------------ Double Check If Quiz Is Graded START ------------------------
      latest_quiz_is_graded_check = check_if_latest_quiz_is_graded_function(slack_workspace_team_id, slack_channel_id, uuid_quiz)
      if latest_quiz_is_graded_check != True:
        localhost_print_function('Latest quiz is not yet fully graded.')
        localhost_print_function('=========================================== /dashboard/quiz/results Page END ===========================================')
        return redirect('/', code=302)
        # ------------------------ Double Check If Quiz Is Graded END ------------------------
      if latest_quiz_is_graded_check == True:
        this_weeks_winner_object = quiz_calculate_quiz_uuid_winner_function(uuid_quiz)
        
        if this_weeks_winner_object != False:
          # Insert to Quiz Winners table
          winner_user_uuid = this_weeks_winner_object[3]
          output_message = quiz_winner_insert_to_db_function(uuid_quiz, winner_user_uuid)

        if this_weeks_winner_object == False:
          localhost_print_function('result winner is false')
          no_winner_timestamp = create_timestamp_function()
          this_weeks_winner_object = [0, 'No Winner', no_winner_timestamp]

    else:
      localhost_print_function('quiz is not past due yet')
      localhost_print_function('=========================================== /dashboard/quiz/results Page END ===========================================')
      return redirect('/', code=302)

  except:
    localhost_print_function('page load except error hit - /dashboard/quiz/results Page')
    localhost_print_function('=========================================== /dashboard/quiz/results Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)


  
  localhost_print_function('=========================================== /dashboard/quiz/results Page END ===========================================')
  return render_template('employee_engagement_page_templates/dashboard_page_templates/quiz_graded_end_of_week_view_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          week_winner_display_name_to_html = this_weeks_winner_object[1].replace('_',' '),
                          week_winner_correct_answers_total_to_html = this_weeks_winner_object[0],
                          week_winner_submit_time_to_html = this_weeks_winner_object[2],
                          free_trial_ends_info_to_html = free_trial_ends_info,
                          page_title_to_html = "This Week's Winner is...")
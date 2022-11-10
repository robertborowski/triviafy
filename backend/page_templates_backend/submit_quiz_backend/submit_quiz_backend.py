  # -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.sanitize_user_inputs.sanitize_quiz_question_user_answer_text import sanitize_quiz_question_user_answer_text_function
from backend.utils.latest_quiz_utils.get_latest_company_quiz_if_exists import get_latest_company_quiz_if_exists_function
from backend.utils.latest_quiz_utils.supporting_make_company_latest_quiz_utils.convert_question_ids_from_string_to_arr import convert_question_ids_from_string_to_arr_function
from backend.page_templates_backend.submit_quiz_backend.map_question_id_user_answers_dict import map_question_id_user_answers_dict_function
from backend.page_templates_backend.submit_quiz_backend.push_update_postgres_db_with_answers import push_update_postgres_db_with_answers_function
from backend.utils.datetime_utils.check_if_quiz_is_past_due_datetime import check_if_quiz_is_past_due_datetime_function
from backend.utils.grade_user_answers_utils.grade_user_answers import grade_user_answers_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
submit_quiz_backend = Blueprint("submit_quiz_backend", __name__, static_folder="static", template_folder="templates")
@submit_quiz_backend.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@submit_quiz_backend.route("/dashboard/user/submit/quiz", methods=['GET','POST'])
def submit_quiz_backend_function():
  localhost_print_function('=========================================== /dashboard/user/submit/quiz Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/dashboard/user/submit/quiz')
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

    # ------------------------ Page Company Info START ------------------------
    user_company_name = user_nested_dict['user_company_name']
    user_company_name = sanitize_page_output_company_name_function(user_company_name)
    user_channel_name = user_nested_dict['user_slack_channel_name']
    # ------------------------ Page Company Info END ------------------------
    

    # ------------------------ Get Variables for DB Insert START ------------------------
    user_uuid = user_nested_dict['user_uuid']
    slack_workspace_team_id = user_nested_dict['user_slack_workspace_team_id']
    slack_channel_id = user_nested_dict['user_slack_channel_id']
    # ------------------------ Get Variables for DB Insert END ------------------------


    # ------------------------ Sanitize User Inputs START ------------------------
    user_answer_to_q1 = sanitize_quiz_question_user_answer_text_function(request.form.get('user_input_quiz_question_answer_1'))
    user_answer_to_q2 = sanitize_quiz_question_user_answer_text_function(request.form.get('user_input_quiz_question_answer_2'))
    user_answer_to_q3 = sanitize_quiz_question_user_answer_text_function(request.form.get('user_input_quiz_question_answer_3'))
    user_answer_to_q4 = sanitize_quiz_question_user_answer_text_function(request.form.get('user_input_quiz_question_answer_4'))
    user_answer_to_q5 = sanitize_quiz_question_user_answer_text_function(request.form.get('user_input_quiz_question_answer_5'))
    try:
      user_answer_to_q6 = sanitize_quiz_question_user_answer_text_function(request.form.get('user_input_quiz_question_answer_6'))
      user_answer_to_q7 = sanitize_quiz_question_user_answer_text_function(request.form.get('user_input_quiz_question_answer_7'))
      user_answer_to_q8 = sanitize_quiz_question_user_answer_text_function(request.form.get('user_input_quiz_question_answer_8'))
      user_answer_to_q9 = sanitize_quiz_question_user_answer_text_function(request.form.get('user_input_quiz_question_answer_9'))
      user_answer_to_q10 = sanitize_quiz_question_user_answer_text_function(request.form.get('user_input_quiz_question_answer_10'))
    except:
      user_answer_to_q6 = 'Only 5 question quiz'
      user_answer_to_q7 = 'Only 5 question quiz'
      user_answer_to_q8 = 'Only 5 question quiz'
      user_answer_to_q9 = 'Only 5 question quiz'
      user_answer_to_q10 = 'Only 5 question quiz'

    if user_answer_to_q1 == None or user_answer_to_q2 == None or user_answer_to_q3 == None or user_answer_to_q4 == None or user_answer_to_q5 == None or user_answer_to_q6 == None or user_answer_to_q7 == None or user_answer_to_q8 == None or user_answer_to_q9 == None or user_answer_to_q10 == None:
      localhost_print_function('inputs are not valid')
      localhost_print_function('=========================================== /dashboard/user/submit/quiz Page END ===========================================')
      return redirect('/dashboard', code=302)
    # ------------------------ Sanitize User Inputs END ------------------------


    # ------------------------ Get Latest Quiz Data START ------------------------
    latest_company_quiz_object = get_latest_company_quiz_if_exists_function(user_nested_dict)
    # ------------------------ If Latest Company Quiz Obj None START ------------------------
    if latest_company_quiz_object == None:
      localhost_print_function('=========================================== /dashboard Page END ===========================================')
      localhost_print_function('Note, this should be redirecting you to a building in progress page now grading.')
      return redirect('/dashboard/quiz/past/due', code=302)
    # ------------------------ If Latest Company Quiz Obj None END ------------------------    
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
    # ------------------------ Get Latest Quiz Data END ------------------------


    # ------------------------ Double Check If Quiz Is Past Due Date START ------------------------
    # In case someone tries to submit answers through postman to a quiz that has already closed
    quiz_is_past_due_date = check_if_quiz_is_past_due_datetime_function(quiz_end_date, quiz_end_time)
    if quiz_is_past_due_date == True:
      localhost_print_function('Cannot submit answers since the quiz is past due.')
      localhost_print_function('=========================================== /dashboard/quiz/past/due Page END ===========================================')
      return redirect('/', code=302)
    # ------------------------ Double Check If Quiz Is Past Due Date END ------------------------


    # ------------------------ Map Quiz User Answers to Quiz Question ID's START ------------------------
    dict_question_id_user_answers = map_question_id_user_answers_dict_function(quiz_number_of_questions, quiz_question_ids_arr, user_answer_to_q1, user_answer_to_q2, user_answer_to_q3, user_answer_to_q4, user_answer_to_q5, user_answer_to_q6, user_answer_to_q7, user_answer_to_q8, user_answer_to_q9, user_answer_to_q10)
    # ------------------------ Map Quiz User Answers to Quiz Question ID's END ------------------------


    # ------------------------ Put User Inputs Into DB START ------------------------
    output_message = push_update_postgres_db_with_answers_function(dict_question_id_user_answers, slack_workspace_team_id, slack_channel_id, user_uuid, uuid_quiz)
    localhost_print_function(output_message)
    # ------------------------ Put User Inputs Into DB END ------------------------


    # ------------------------ Grade Answers Algorithm START ------------------------
    output_message = grade_user_answers_function(uuid_quiz, user_uuid)
    localhost_print_function(output_message)
    # ------------------------ Grade Answers Algorithm END ------------------------


  except:
    localhost_print_function('page load except error hit - /dashboard/user/submit/quiz Page')
    localhost_print_function('=========================================== /dashboard/user/submit/quiz Page END ===========================================')
    return redirect('/employees/logout', code=302)
    # return redirect('/', code=302)


  
  localhost_print_function('=========================================== /dashboard/user/submit/quiz Page END ===========================================')
  return redirect('/dashboard', code=302)
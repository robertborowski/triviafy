# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_quiz_master_table.select_quiz_uuid_from_quiz_master_table import select_quiz_uuid_from_quiz_master_table_function
from datetime import datetime
from backend.utils.latest_quiz_utils.supporting_make_company_latest_quiz_utils.convert_question_ids_from_string_to_arr import convert_question_ids_from_string_to_arr_function
from backend.db.queries.select_queries.select_queries_triviafy_all_questions_table.select_triviafy_all_questions_table_question_info import select_triviafy_all_questions_table_question_info_function
from backend.db.queries.select_queries.select_queries_triviafy_quiz_answers_master_table.select_triviafy_quiz_answers_master_table_user_answer import select_triviafy_quiz_answers_master_table_user_answer_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function
from backend.utils.quiz_categories_utils.datatype_change_categories_list_str_to_tuple import datatype_change_categories_list_str_to_tuple_function

# -------------------------------------------------------------- App Setup
quiz_archive_specific_quiz_number = Blueprint("quiz_archive_specific_quiz_number", __name__, static_folder="static", template_folder="templates")
@quiz_archive_specific_quiz_number.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@quiz_archive_specific_quiz_number.route("/quiz/archive/<html_variable_quiz_number>", methods=['GET','POST'])
def quiz_archive_specific_quiz_number_function(html_variable_quiz_number):
  localhost_print_function('=========================================== /quiz/archive/<html_variable_quiz_number> Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/quiz/archive/<html_variable_quiz_number>')
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
    user_uuid = user_nested_dict['user_uuid']
    slack_workspace_team_id = user_nested_dict['slack_team_id']
    slack_channel_id = user_nested_dict['slack_channel_id']
    int_quiz_number = int(html_variable_quiz_number)


    # ------------------------ Get Info From triviafy_quiz_master_table START ------------------------
    # ------------------------ Open Connections START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()
    # ------------------------ Open Connections END ------------------------

    # From Quiz Number link selected, get Quiz UUID and Question UUID's 
    link_selected_quiz_master_table_arr = select_quiz_uuid_from_quiz_master_table_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id, int_quiz_number)
    
    # Assign Variables from DB pull
    link_selected_uuid_quiz = link_selected_quiz_master_table_arr[0]  # str
    link_selected_question_ids_str = convert_question_ids_from_string_to_arr_function(link_selected_quiz_master_table_arr[1])   # list (array)
    link_selected_company_quiz_count = link_selected_quiz_master_table_arr[8] # int
    link_selected_quiz_master_string_start = link_selected_quiz_master_table_arr[2].strftime("%Y-%m-%d") + ', ' + link_selected_quiz_master_table_arr[3] + ', ' + link_selected_quiz_master_table_arr[4]  # str
    link_selected_quiz_master_string_end = link_selected_quiz_master_table_arr[5].strftime("%Y-%m-%d") + ', ' + link_selected_quiz_master_table_arr[6] + ', ' + link_selected_quiz_master_table_arr[7]  # str
    
    # Put the pulled values into dict
    link_selected_quiz_archive_intro_dict = {
      'company_quiz_count' : link_selected_company_quiz_count,  # int
      'quiz_master_string_start' : link_selected_quiz_master_string_start,  # str
      'quiz_master_string_end' : link_selected_quiz_master_string_end   # str
    }

    # Check to make sure archive quiz number is correct
    if int_quiz_number != link_selected_company_quiz_count:
      localhost_print_function('quiz link int does not match pulled quiz int number')
      localhost_print_function('=========================================== /quiz/archive/<html_variable_quiz_number> Page END ===========================================')
      return redirect('/', code=302)
    # ------------------------ Get Info From triviafy_quiz_master_table END ------------------------


    
    # ------------------------ Get Info From triviafy_all_questions_table START ------------------------
    pull_info_all_questions_table_arr_of_dicts = []
    # If question was removed
    removed_question_ids_arr = []
    for question_id in link_selected_question_ids_str:
      pulled_item_arr_of_dict = select_triviafy_all_questions_table_question_info_function(postgres_connection, postgres_cursor, question_id)
      # If question was removed
      if pulled_item_arr_of_dict == []:
        removed_question_ids_arr.append(question_id)
        pulled_dict = {
          'question_uuid': 'questionid_removed',
          'question_categories_list': 'Question removed',
          'question_actual_question': 'Question removed',
          'question_answers_list':'Question removed',
          'question_difficulty': 'Easy',
          'question_hint_allowed': False,
          'question_hint': 'no hint',
          'question_deprecated': False,
          'question_deprecated_timestamp': None,
          'question_title': 'Question removed',
          'question_contains_image': True,
          'question_image_aws_url': 'https://triviafy-create-question-image-uploads.s3.us-east-2.amazonaws.com/_question_removed_image_for_aws_s3.png'
        }
      else:
        pulled_dict = pulled_item_arr_of_dict[0]
      pull_info_all_questions_table_arr_of_dicts.append(pulled_dict)
    # ------------------------ Get Info From triviafy_all_questions_table END ------------------------


    # ------------------------ CSS fix for category colors START ------------------------
    for i in pull_info_all_questions_table_arr_of_dicts:
      # Create and append category colors for end user css
      categories_arr_to_html = datatype_change_categories_list_str_to_tuple_function(i['question_categories_list'])
      i['question_categories_list_arr'] = categories_arr_to_html
    # ------------------------ CSS fix for category colors END ------------------------
    
    
    # ------------------------ Get Info From triviafy_quiz_answers_master_table START ------------------------
    pull_info_quiz_answers_master_table_answer_dict = {}
    pull_info_quiz_answers_master_table_result_dict = {}
    for question_id in link_selected_question_ids_str:
      # If question was removed
      if question_id in removed_question_ids_arr:
        pulled_item_arr = ['questionid_removed', 'question_removed', False]
      else:
        pulled_item_arr = select_triviafy_quiz_answers_master_table_user_answer_function(postgres_connection, postgres_cursor, question_id, user_uuid)
      pull_info_quiz_answers_master_table_answer_dict[pulled_item_arr[0]] = pulled_item_arr[1].replace("_", " ")
      pull_info_quiz_answers_master_table_result_dict[pulled_item_arr[0]] = pulled_item_arr[2]
    # ------------------------ Get Info From triviafy_quiz_answers_master_table END ------------------------


    # ------------------------ Map User Submitted Answer To Quiz Question Obj START ------------------------
    question_number_count = 1
    # Loop through array of dicts
    for dict in pull_info_all_questions_table_arr_of_dicts:
      dict['user_quiz_question_answer'] = pull_info_quiz_answers_master_table_answer_dict[dict['question_uuid']]
      dict['user_quiz_question_result'] = pull_info_quiz_answers_master_table_result_dict[dict['question_uuid']]
      dict['quiz_question_number'] = question_number_count
      question_number_count += 1
    # ------------------------ Map User Submitted Answer To Quiz Question Obj END ------------------------


    # ------------------------ Close Connections START ------------------------
    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Close Connections END ------------------------


    # ------------------------ Get Total Correct Answers START ------------------------
    total_questions_for_quiz = len(pull_info_all_questions_table_arr_of_dicts)
    total_correct_answers_for_quiz = 0
    for dict in pull_info_all_questions_table_arr_of_dicts:
      if dict['user_quiz_question_result'] == True or dict['user_quiz_question_result'] == 'True':
        total_correct_answers_for_quiz += 1
    # ------------------------ Get Total Correct Answers END ------------------------


  except:
    localhost_print_function('page load except error hit - /quiz/archive/<html_variable_quiz_number>')
    localhost_print_function('=========================================== /quiz/archive/<html_variable_quiz_number> Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)


  
  localhost_print_function('=========================================== /quiz/archive/<html_variable_quiz_number> Page END ===========================================')
  return render_template('quiz_archive_page_templates/quiz_archive_specific_version.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          link_selected_quiz_archive_intro_dict_to_html = link_selected_quiz_archive_intro_dict,
                          pull_info_all_questions_table_arr_of_dicts_to_html = pull_info_all_questions_table_arr_of_dicts,
                          total_questions_for_quiz_to_html = total_questions_for_quiz,
                          total_correct_answers_for_quiz_to_html = total_correct_answers_for_quiz,
                          free_trial_ends_info_to_html = free_trial_ends_info,
                          page_title_to_html = 'Archive Quiz')
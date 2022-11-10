# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_joined_tables.select_company_quiz_archive_all_graded_quizzes import select_company_quiz_archive_all_graded_quizzes_function
from datetime import datetime
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
quiz_archive_page_render_template = Blueprint("quiz_archive_page_render_template", __name__, static_folder="static", template_folder="templates")
@quiz_archive_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@quiz_archive_page_render_template.route("/quiz/archive", methods=['GET','POST'])
def quiz_archive_page_render_template_function():
  localhost_print_function('=========================================== /quiz/archive Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/quiz/archive')
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
    
    # Get additional variables
    slack_workspace_team_id = user_nested_dict['user_slack_workspace_team_id']
    slack_channel_id = user_nested_dict['user_slack_channel_id']


    # ------------------------ Get All Graded Quizzes For Company START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()

    company_quiz_archive_all_graded_quizzes_arr = select_company_quiz_archive_all_graded_quizzes_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)

    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Get All Graded Quizzes For Company END ------------------------


    # ------------------------ If No Quizzes Are In Archive For Company START ------------------------
    if company_quiz_archive_all_graded_quizzes_arr == None:
      localhost_print_function('There are no quiz archives for this company-team yet')
      localhost_print_function('=========================================== /quiz/archive Page END ===========================================')
      return redirect('/quiz/archive/none', code=302)
    # ------------------------ If No Quizzes Are In Archive For Company END ------------------------


    # ------------------------ Transpose Results Into Arr of Dict START ------------------------
    company_quiz_archive_all_graded_quizzes_arr_of_dicts = []

    for i in company_quiz_archive_all_graded_quizzes_arr:
      # Create Variables for the dict
      quiz_master_string_start = i[2].strftime("%Y-%m-%d") + ', ' + i[3] + ', ' + i[4]
      quiz_master_string_end = i[5].strftime("%Y-%m-%d") + ', ' + i[6] + ', ' + i[7]
      
      temp_dict = {
        # 'uuid_quiz' : i[0],
        'company_quiz_count' : i[1],
        # 'quiz_start_date' : i[2],
        # 'quiz_start_day_of_week' : i[3],
        # 'quiz_start_time' : i[4],
        'quiz_master_string_start' : quiz_master_string_start,
        # 'quiz_end_date' : i[5],
        # 'quiz_end_day_of_week' : i[6],
        # 'quiz_end_time' : i[7],
        'quiz_master_string_end' : quiz_master_string_end,
        'quiz_number_of_questions' : i[8],
        'user_display_name_winner' : i[9]
      }
      company_quiz_archive_all_graded_quizzes_arr_of_dicts.append(temp_dict)
    # ------------------------ Transpose Results Into Arr of Dict END ------------------------


  except:
    localhost_print_function('page load except error hit - /quiz/archive Page')
    localhost_print_function('=========================================== /quiz/archive Page END ===========================================')
    return redirect('/employees/logout', code=302)
    # return redirect('/', code=302)


  
  localhost_print_function('=========================================== /quiz/archive Page END ===========================================')
  return render_template('employee_engagement_page_templates/quiz_archive_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          company_quiz_archive_all_graded_quizzes_arr_of_dicts_to_html = company_quiz_archive_all_graded_quizzes_arr_of_dicts,
                          free_trial_ends_info_to_html = free_trial_ends_info,
                          page_title_to_html = 'Archive')
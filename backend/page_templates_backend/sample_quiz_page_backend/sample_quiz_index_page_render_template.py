# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_sample_questions_table.select_triviafy_sample_questions_table_all import select_triviafy_sample_questions_table_all_function
from backend.db.queries.select_queries.select_queries_triviafy_all_questions_table.select_company_quiz_questions_individually import select_company_quiz_questions_individually_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function
from backend.utils.quiz_categories_utils.datatype_change_categories_list_str_to_tuple import datatype_change_categories_list_str_to_tuple_function

# -------------------------------------------------------------- App Setup
sample_quiz_index_page_render_template = Blueprint("sample_quiz_index_page_render_template", __name__, static_folder="static", template_folder="templates")
@sample_quiz_index_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@sample_quiz_index_page_render_template.route("/sample/quiz", methods=['GET','POST'])
def sample_quiz_index_page_render_template_function():
  localhost_print_function('=========================================== /sample/quiz Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/sample/quiz')
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
    user_channel_name = user_nested_dict['user_slack_channel_name']
    # ------------------------ Page Company Info END ------------------------
    
    # Get additional variables
    slack_workspace_team_id = user_nested_dict['user_slack_workspace_team_id']
    slack_channel_id = user_nested_dict['user_slack_channel_id']


    # ------------------------ Open Connections START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()
    # ------------------------ Open Connections END ------------------------


    # ------------------------ Get Sample Question UUIDs START ------------------------
    # Get quiz settings from DB as arr
    sample_question_uuids_arr = select_triviafy_sample_questions_table_all_function(postgres_connection, postgres_cursor)
    # ------------------------ Get Quiz Settings Info END ------------------------


    # ------------------------ Get Quiz Question Arr of Dicts START ------------------------
    sample_questions_arr_of_dicts = []
    for sample_question_uuid in sample_question_uuids_arr:
      sample_question_dict = select_company_quiz_questions_individually_function(postgres_connection, postgres_cursor, sample_question_uuid)
      # Create and append category colors for end user css
      categories_arr_to_html = datatype_change_categories_list_str_to_tuple_function(sample_question_dict[0]['question_categories_list'])
      sample_question_dict[0]['question_categories_list_arr'] = categories_arr_to_html
      # Words for user html tuple End
      sample_questions_arr_of_dicts.append(sample_question_dict[0])
    # ------------------------ Get Quiz Question Arr of Dicts END ------------------------


    # ------------------------ Add Current Question Count To Dict START ------------------------
    current_count = 0
    for i in sample_questions_arr_of_dicts:
      current_count += 1
      i['quiz_question_number'] = current_count
    # ------------------------ Add Current Question Count To Dict END ------------------------


    # ------------------------ Close Connections START ------------------------
    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Close Connections END ------------------------
    
  except:
    localhost_print_function('page load except error hit - /sample/quiz Page')
    localhost_print_function('=========================================== /sample/quiz Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)

  
  localhost_print_function('=========================================== /sample/quiz Page END ===========================================')
  return render_template('sample_quiz_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          quiz_questions_obj_arr_of_dicts_html = sample_questions_arr_of_dicts,
                          free_trial_ends_info_to_html = free_trial_ends_info,
                          page_title_to_html = 'Sample Quiz')
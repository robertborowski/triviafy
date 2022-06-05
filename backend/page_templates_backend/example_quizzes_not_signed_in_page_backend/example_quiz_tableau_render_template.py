# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_all_questions_table.select_x_questions_category_tableau import select_x_questions_category_tableau_function
from backend.utils.quiz_categories_utils.datatype_change_categories_list_str_to_tuple import datatype_change_categories_list_str_to_tuple_function

# -------------------------------------------------------------- App Setup
example_quiz_tableau_render_template = Blueprint("example_quiz_tableau_render_template", __name__, static_folder="static", template_folder="templates")
@example_quiz_tableau_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@example_quiz_tableau_render_template.route("/example/tableau", methods=['GET','POST'])
def example_quiz_tableau_render_template_function():
  localhost_print_function('=========================================== /example/tableau Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  # ------------------------ Connect to Postgrest DB START ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ Connect to Postgrest DB END ------------------------


  # ------------------------ Pull the Example Quiz Questions START ------------------------
  quiz_questions_obj_arr_of_dicts = select_x_questions_category_tableau_function(postgres_connection, postgres_cursor)

  # Add current question count to the dictionary for html
  current_count = 0
  for i in quiz_questions_obj_arr_of_dicts:
    current_count += 1
    i['quiz_question_number'] = current_count
    # Create and append category colors for end user css
    categories_arr_to_html = datatype_change_categories_list_str_to_tuple_function(i['question_categories_list'])
    i['question_categories_list_arr'] = categories_arr_to_html
  # ------------------------ Pull the Example Quiz Questions END ------------------------


  # ------------------------ Close Postgrest DB START ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Close Postgrest DB END ------------------------

  localhost_print_function('=========================================== /example/tableau Page END ===========================================')
  return render_template('example_quizzes_not_signed_in_page_templates/index_tableau.html',
                          css_cache_busting = cache_busting_output,
                          quiz_questions_obj_arr_of_dicts_html = quiz_questions_obj_arr_of_dicts)
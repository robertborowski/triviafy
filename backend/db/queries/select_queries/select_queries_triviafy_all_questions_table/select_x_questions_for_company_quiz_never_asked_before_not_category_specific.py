# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error, extras
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_x_questions_for_company_quiz_never_asked_before_not_category_specific_function(postgres_connection, postgres_cursor, count_remaining_questions_needed, temp_question_id_chosen_str, slack_workspace_team_id, slack_channel_id):
  localhost_print_function('=========================================== select_x_questions_for_company_quiz_never_asked_before_not_category_specific_function START ===========================================')
  try:
    # ------------------------ Dict Cursor START ------------------------
    cursor = postgres_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # ------------------------ Dict Cursor END ------------------------


    # ------------------------ Query START ------------------------
    # cursor.execute("SELECT*FROM triviafy_all_questions_table WHERE question_approved_for_release=TRUE AND question_uuid NOT IN(SELECT t1.question_uuid FROM triviafy_all_questions_table AS t1 INNER JOIN triviafy_quiz_questions_asked_to_company_slack_table AS t2 ON t1.question_uuid=t2.quiz_question_asked_tracking_question_uuid)AND question_uuid NOT IN(%s)ORDER BY RANDOM()LIMIT %s", [temp_question_id_chosen_str, count_remaining_questions_needed])
    # ------------------------ Query END ------------------------


    # ------------------------ Query START ------------------------
    cursor.execute("SELECT*FROM triviafy_all_questions_table WHERE question_approved_for_release=TRUE AND question_uuid NOT IN(SELECT t1.question_uuid FROM triviafy_all_questions_table AS t1 INNER JOIN triviafy_quiz_questions_asked_to_company_slack_table AS t2 ON t1.question_uuid=t2.quiz_question_asked_tracking_question_uuid WHERE t2.quiz_question_asked_tracking_slack_team_id=%s AND t2.quiz_question_asked_tracking_slack_channel_id=%s)AND question_uuid NOT IN(%s)ORDER BY RANDOM()LIMIT %s", [slack_workspace_team_id, slack_channel_id, temp_question_id_chosen_str, count_remaining_questions_needed])
    # ------------------------ Query END ------------------------
    

    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = cursor.fetchall()
    
    # Put results arr into dict
    result_arr_dicts = []
    for row in result_arr:
      result_arr_dicts.append(dict(row))
    
    # Retunr results dict
    localhost_print_function('=========================================== select_x_questions_for_company_quiz_never_asked_before_not_category_specific_function END ===========================================')
    return result_arr_dicts
    # ------------------------ Query Result END ------------------------


  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_x_questions_for_company_quiz_never_asked_before_not_category_specific_function END ===========================================')
      return 'none'
# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error, extras
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_x_questions_for_company_quiz_never_asked_before_category_specific_function(postgres_connection, postgres_cursor, quiz_number_of_questions, sql_like_statement_str, slack_workspace_team_id, slack_channel_id):
  localhost_print_function('=========================================== select_x_questions_for_company_quiz_never_asked_before_category_specific_function START ===========================================')
  try:
    # ------------------------ Dict Cursor START ------------------------
    cursor = postgres_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # ------------------------ Dict Cursor END ------------------------


    # ------------------------ Query START Before Change on 1/10/2022 ------------------------
    #cursor.execute("SELECT*FROM triviafy_all_questions_table WHERE question_approved_for_release=TRUE AND question_uuid NOT IN(SELECT t1.question_uuid FROM triviafy_all_questions_table AS t1 INNER JOIN triviafy_quiz_questions_asked_to_company_slack_table AS t2 ON t1.question_uuid=t2.quiz_question_asked_tracking_question_uuid)AND({})ORDER BY RANDOM()LIMIT %s".format(sql_like_statement_str), [quiz_number_of_questions])
    # ------------------------ Query END Before Change on 1/10/2022 ------------------------
    
    
    # ------------------------ Query START ------------------------
    cursor.execute("SELECT*FROM triviafy_all_questions_table WHERE question_approved_for_release=TRUE AND question_uuid NOT IN(SELECT t1.question_uuid FROM triviafy_all_questions_table AS t1 INNER JOIN triviafy_quiz_questions_asked_to_company_slack_table AS t2 ON t1.question_uuid=t2.quiz_question_asked_tracking_question_uuid WHERE t2.quiz_question_asked_tracking_slack_team_id=%s AND t2.quiz_question_asked_tracking_slack_channel_id=%s)AND({})ORDER BY RANDOM()LIMIT %s".format(sql_like_statement_str), [slack_workspace_team_id, slack_channel_id, quiz_number_of_questions])
    # ------------------------ Query END ------------------------
    

    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = cursor.fetchall()
    
    # Put results arr into dict
    result_arr_dicts = []
    for row in result_arr:
      result_arr_dicts.append(dict(row))
    
    # Retunr results dict
    localhost_print_function('=========================================== select_x_questions_for_company_quiz_never_asked_before_category_specific_function END ===========================================')
    return result_arr_dicts
    # ------------------------ Query Result END ------------------------


  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ')
      localhost_print_function('=========================================== select_x_questions_for_company_quiz_never_asked_before_category_specific_function END ===========================================')
      return 'none'
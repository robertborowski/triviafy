# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_quiz_week_winner_function(postgres_connection, postgres_cursor, uuid_quiz):
  localhost_print_function('=========================================== select_quiz_week_winner_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT COUNT(answers.*),users.user_display_name,MIN(answers.quiz_answer_timestamp),users.user_uuid,users.user_slack_authed_id FROM triviafy_quiz_answers_master_table AS answers LEFT JOIN triviafy_user_login_information_table_slack AS users ON answers.quiz_answer_user_uuid_fk=users.user_uuid WHERE answers.quiz_answer_quiz_uuid_fk=%s AND answers.quiz_answer_provided_is_correct=TRUE GROUP BY users.user_display_name,users.user_uuid ORDER BY COUNT(answers.*)DESC,MIN(answers.quiz_answer_timestamp)LIMIT 1", [uuid_quiz])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_quiz_week_winner_function END ===========================================')
      return None
    
    localhost_print_function('=========================================== select_quiz_week_winner_function END ===========================================')
    return result_row
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_quiz_week_winner_function END ===========================================')
      return None
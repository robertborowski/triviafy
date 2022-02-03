# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_triviafy_quiz_answers_master_table_count_correct_answers_per_team_channel_function(postgres_connection, postgres_cursor, team_id, channel_id, quiz_uuid):
  localhost_print_function('=========================================== select_triviafy_quiz_answers_master_table_count_correct_answers_per_team_channel_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT COUNT(*) FROM triviafy_quiz_answers_master_table WHERE quiz_answer_slack_team_id=%s AND quiz_answer_slack_channel_id=%s AND quiz_answer_quiz_uuid_fk=%s AND quiz_answer_has_been_graded=TRUE AND quiz_answer_provided_is_correct=TRUE;", [team_id, channel_id, quiz_uuid])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_triviafy_quiz_answers_master_table_count_correct_answers_per_team_channel_function END ===========================================')
      return None

    localhost_print_function('=========================================== select_triviafy_quiz_answers_master_table_count_correct_answers_per_team_channel_function END ===========================================')
    return result_row[0]
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_triviafy_quiz_answers_master_table_count_correct_answers_per_team_channel_function END ===========================================')
      return None
# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_skipped_quiz_count_team_channel_combo_function(postgres_connection, postgres_cursor, team_id, channel_id):
  localhost_print_function('=========================================== select_skipped_quiz_count_team_channel_combo_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT skipped_quiz_count FROM triviafy_skipped_quiz_count_slack_team_channel_table WHERE skipped_quiz_slack_team_id=%s AND skipped_quiz_slack_channel_id=%s;", [team_id, channel_id])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_skipped_quiz_count_team_channel_combo_function END ===========================================')
      return None

    localhost_print_function('=========================================== select_skipped_quiz_count_team_channel_combo_function END ===========================================')
    return result_row[0]
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_skipped_quiz_count_team_channel_combo_function END ===========================================')
      return None
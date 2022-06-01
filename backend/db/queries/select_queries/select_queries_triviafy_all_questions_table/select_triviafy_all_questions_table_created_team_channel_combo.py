# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_triviafy_all_questions_table_created_team_channel_combo_function(postgres_connection, postgres_cursor, question_author_team_id, question_author_channel_id, today_date_year, today_date_month):
  localhost_print_function('=========================================== select_triviafy_all_questions_table_created_team_channel_combo_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT COUNT(*)FROM triviafy_all_questions_table WHERE question_author_team_id=%s AND question_author_channel_id=%s AND EXTRACT(YEAR FROM triviafy_all_questions_table.question_timestamp_created)=%s AND EXTRACT(MONTH FROM triviafy_all_questions_table.question_timestamp_created)=%s;", [question_author_team_id, question_author_channel_id, today_date_year, today_date_month])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_triviafy_all_questions_table_created_team_channel_combo_function END ===========================================')
      return None
    
    localhost_print_function('=========================================== select_triviafy_all_questions_table_created_team_channel_combo_function END ===========================================')
    return result_row[0]
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_triviafy_all_questions_table_created_team_channel_combo_function END ===========================================')
      return None
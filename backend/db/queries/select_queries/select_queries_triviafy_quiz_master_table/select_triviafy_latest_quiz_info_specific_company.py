# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_triviafy_latest_quiz_info_specific_company_function(postgres_connection, postgres_cursor, monday_date, tuesday_date, wednesday_date, thursday_date, friday_date, saturday_date, sunday_date, team_id, channel_id):
  localhost_print_function('=========================================== select_triviafy_latest_quiz_info_specific_company_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT * FROM triviafy_quiz_master_table WHERE (quiz_start_date=%s OR quiz_start_date=%s OR quiz_start_date=%s OR quiz_start_date=%s OR quiz_start_date=%s OR quiz_start_date=%s OR quiz_start_date=%s) AND (quiz_slack_team_id=%s AND quiz_slack_channel_id=%s)", [monday_date, tuesday_date, wednesday_date, thursday_date, friday_date, saturday_date, sunday_date, team_id, channel_id])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = postgres_cursor.fetchall()
    if result_arr == None or result_arr == []:
      localhost_print_function('=========================================== select_triviafy_latest_quiz_info_specific_company_function END ===========================================')
      return None

    localhost_print_function('=========================================== select_triviafy_latest_quiz_info_specific_company_function END ===========================================')  
    return result_arr
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_triviafy_latest_quiz_info_specific_company_function END ===========================================')
      return None
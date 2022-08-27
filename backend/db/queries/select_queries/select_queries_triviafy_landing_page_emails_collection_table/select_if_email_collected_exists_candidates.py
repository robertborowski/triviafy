# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_if_email_collected_exists_candidates_function(postgres_connection, postgres_cursor, user_collected_email):
  localhost_print_function('=========================================== select_if_email_collected_exists_candidates_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT * FROM triviafy_landing_emails_candidates_table WHERE collect_email_actual_email=%s", [user_collected_email])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_if_email_collected_exists_candidates_function END ===========================================')
      return None
    
    localhost_print_function('=========================================== select_if_email_collected_exists_candidates_function END ===========================================')
    return result_row
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_if_email_collected_exists_candidates_function END ===========================================')
      return None
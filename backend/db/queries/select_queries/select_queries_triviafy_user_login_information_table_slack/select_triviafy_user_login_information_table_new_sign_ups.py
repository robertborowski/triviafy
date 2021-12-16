# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_triviafy_user_login_information_table_new_sign_ups_function(postgres_connection, postgres_cursor):
  localhost_print_function('=========================================== select_triviafy_user_login_information_table_new_sign_ups_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("WITH sub1 AS(SELECT i.user_email,i.user_uuid FROM triviafy_user_login_information_table_slack AS i WHERE i.user_datetime_account_created>=CURRENT_DATE-0)SELECT COUNT(*)FROM sub1;")
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_triviafy_user_login_information_table_new_sign_ups_function END ===========================================')
      return None
    

    localhost_print_function('=========================================== select_triviafy_user_login_information_table_new_sign_ups_function END ===========================================')
    return result_row[0]
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_triviafy_user_login_information_table_new_sign_ups_function END ===========================================')
      return None
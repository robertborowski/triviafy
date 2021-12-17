# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_triviafy_user_login_information_table_new_emails_for_dist_list_function(postgres_connection, postgres_cursor):
  localhost_print_function('=========================================== select_triviafy_user_login_information_table_new_emails_for_dist_list_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("WITH sub1 AS(SELECT l.collect_email_actual_email,l.collect_email_uuid AS uuid_type FROM triviafy_landing_page_emails_collection_table AS l WHERE l.collect_email_timestamp>=CURRENT_DATE)SELECT COUNT(*)FROM sub1;")
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_triviafy_user_login_information_table_new_emails_for_dist_list_function END ===========================================')
      return None
    

    localhost_print_function('=========================================== select_triviafy_user_login_information_table_new_emails_for_dist_list_function END ===========================================')
    return result_row[0]
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_triviafy_user_login_information_table_new_emails_for_dist_list_function END ===========================================')
      return None
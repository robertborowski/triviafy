# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_email_exists_skipped_quiz_request_feedback_function(postgres_connection, postgres_cursor, user_uuid, email_sent_search_category):
  localhost_print_function('=========================================== select_email_exists_skipped_quiz_request_feedback_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT * FROM triviafy_emails_sent_table WHERE email_sent_to_user_uuid_fk=%s AND email_sent_category=%s AND email_sent_timestamp >= CURRENT_DATE;", [user_uuid, email_sent_search_category])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_email_exists_skipped_quiz_request_feedback_function END ===========================================')
      return None

    localhost_print_function('=========================================== select_email_exists_skipped_quiz_request_feedback_function END ===========================================')
    return result_row
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_email_exists_skipped_quiz_request_feedback_function END ===========================================')
      return None
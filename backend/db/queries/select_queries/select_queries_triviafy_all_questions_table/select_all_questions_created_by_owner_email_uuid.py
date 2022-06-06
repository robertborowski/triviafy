# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_all_questions_created_by_owner_email_uuid_function(postgres_connection, postgres_cursor, user_uuid):
  localhost_print_function('=========================================== select_all_questions_created_by_owner_email_uuid_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT question_uuid FROM triviafy_all_questions_table WHERE question_author_uuid=%s ORDER BY question_timestamp_created;", [user_uuid])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = postgres_cursor.fetchall()
    if result_arr == None or result_arr == []:
      localhost_print_function('=========================================== select_all_questions_created_by_owner_email_uuid_function END ===========================================')
      return None

    localhost_print_function('=========================================== select_all_questions_created_by_owner_email_uuid_function END ===========================================')
    return result_arr
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_all_questions_created_by_owner_email_uuid_function END ===========================================')
      return None
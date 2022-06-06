# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_all_questions_created_by_owner_email_count_function(postgres_connection, postgres_cursor, user_uuid):
  localhost_print_function('=========================================== select_all_questions_created_by_owner_email_count_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT COUNT(question_author_uuid)FROM triviafy_all_questions_table WHERE question_author_uuid=%s;", [user_uuid])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_all_questions_created_by_owner_email_count_function END ===========================================')
      return None
    
    localhost_print_function('=========================================== select_all_questions_created_by_owner_email_count_function END ===========================================')
    return result_row[0]
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_all_questions_created_by_owner_email_count_function END ===========================================')
      return None
# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_if_email_already_sent_expiring_id_function(postgres_connection, postgres_cursor, additional_input):
  localhost_print_function('=========================================== select_if_email_already_sent_expiring_id_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT \
                              * \
                            FROM \
                              candidates_email_sent_obj \
                            WHERE \
                              assessment_expiring_url_fk=%s;", [additional_input])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = postgres_cursor.fetchall()
    if result_arr == None or result_arr == []:
      localhost_print_function('=========================================== select_if_email_already_sent_expiring_id_function END ===========================================')
      return None

    localhost_print_function('=========================================== select_if_email_already_sent_expiring_id_function END ===========================================')
    return result_arr
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_if_email_already_sent_expiring_id_function END ===========================================')
      return None
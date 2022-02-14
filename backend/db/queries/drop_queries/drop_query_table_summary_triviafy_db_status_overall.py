# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def drop_query_table_summary_triviafy_db_status_overall_function(postgres_connection, postgres_cursor):
  localhost_print_function('=========================================== drop_query_table_summary_triviafy_db_status_overall_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("DROP TABLE summary_triviafy_db_status_overall;")
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    postgres_connection.commit()
    localhost_print_function('=========================================== drop_query_table_summary_triviafy_db_status_overall_function END ===========================================')
    return True
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== drop_query_table_summary_triviafy_db_status_overall_function END ===========================================')
      return None
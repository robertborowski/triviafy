# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def insert_email_sent_row_function(postgres_connection, postgres_cursor, input_arr):
  localhost_print_function('=========================================== insert_email_sent_row_function START ===========================================')
  
  # ------------------------ Query START ------------------------
  postgres_insert_query = """INSERT INTO candidates_email_sent_obj(id,created_timestamp,from_user_id_fk,to_email,assessment_expiring_url_fk,subject,body) VALUES(%s,%s,%s,%s,%s,%s,%s)"""
  # ------------------------ Query END ------------------------


  # ------------------------ Record row START ------------------------
  record_to_insert = (input_arr[0],input_arr[1],input_arr[2],input_arr[3],input_arr[4],input_arr[5],input_arr[6])
  # ------------------------ Record row END ------------------------


  # ------------------------ Insert attempt START ------------------------
  try:
    postgres_cursor.execute(postgres_insert_query, record_to_insert)
    postgres_connection.commit()
    localhost_print_function('=========================================== insert_email_sent_row_function END ===========================================')
    return True
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== insert_email_sent_row_function END ===========================================')
      return False
  # ------------------------ Insert attempt END ------------------------
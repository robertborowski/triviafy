# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def insert_user_collected_email_candidates_function(postgres_connection, postgres_cursor, collect_email_uuid, collect_email_timestamp, collect_email_actual_email):
  localhost_print_function('=========================================== insert_user_collected_email_candidates_function START ===========================================')
  
  # ------------------------ Query START ------------------------
  postgres_insert_query = """INSERT INTO z_candidates_collect_email(collect_email_uuid,collect_email_timestamp,collect_email_actual_email) VALUES(%s,%s,%s)"""
  # ------------------------ Query END ------------------------


  # ------------------------ Record row START ------------------------
  record_to_insert = (collect_email_uuid, collect_email_timestamp, collect_email_actual_email)
  # ------------------------ Record row END ------------------------


  # ------------------------ Insert attempt START ------------------------
  try:
    postgres_cursor.execute(postgres_insert_query, record_to_insert)
    postgres_connection.commit()
    
    localhost_print_function('=========================================== insert_user_collected_email_candidates_function END ===========================================')
    return True
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== insert_user_collected_email_candidates_function END ===========================================')
      return False
  # ------------------------ Insert attempt END ------------------------
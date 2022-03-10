# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def insert_triviafy_deleted_accounts_table_function(postgres_connection, postgres_cursor, deleted_account_uuid, deleted_account_timestamp, deleted_account_team_id, deleted_account_channel_id, deleted_account_users_obj):
  localhost_print_function('=========================================== insert_triviafy_deleted_accounts_table_function START ===========================================')
  
  # ------------------------ Query START ------------------------
  postgres_insert_query = """INSERT INTO triviafy_deleted_accounts_table(deleted_account_uuid, deleted_account_timestamp, deleted_account_team_id, deleted_account_channel_id, deleted_account_users_obj) VALUES(%s,%s,%s,%s,%s)"""
  # ------------------------ Query END ------------------------


  # ------------------------ Record row START ------------------------
  record_to_insert = (deleted_account_uuid, deleted_account_timestamp, deleted_account_team_id, deleted_account_channel_id, deleted_account_users_obj)
  # ------------------------ Record row END ------------------------


  # ------------------------ Insert attempt START ------------------------
  try:
    postgres_cursor.execute(postgres_insert_query, record_to_insert)
    postgres_connection.commit()

    localhost_print_function('=========================================== insert_triviafy_deleted_accounts_table_function END ===========================================')
    return True
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== insert_triviafy_deleted_accounts_table_function END ===========================================')
      return None
  # ------------------------ Insert attempt END ------------------------
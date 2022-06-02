# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_count_all_table_team_channel_combo_special_by_user_uuid_function(postgres_connection, postgres_cursor, user_uuid, table_name, table_user_uuid_fk_column_name):
  localhost_print_function('=========================================== select_count_all_table_team_channel_combo_special_by_user_uuid_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT COUNT(*) FROM {} WHERE {} = %s;".format(table_name, table_user_uuid_fk_column_name), [user_uuid])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_count_all_table_team_channel_combo_special_by_user_uuid_function END ===========================================')
      return None
    
    localhost_print_function('=========================================== select_count_all_table_team_channel_combo_special_by_user_uuid_function END ===========================================')
    return result_row
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_count_all_table_team_channel_combo_special_by_user_uuid_function END ===========================================')
      return None
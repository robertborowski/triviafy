# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_all_users_team_channel import select_all_users_team_channel_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_all_column_names import select_all_column_names_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.db.queries.insert_queries.insert_queries_triviafy_deleted_accounts_table.insert_triviafy_deleted_accounts_table import insert_triviafy_deleted_accounts_table_function
import json
from datetime import datetime



# -------------------------------------------------------------- Main
def job_pre_delete_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id):
  localhost_print_function('=========================================== job_pre_delete_table_checks_function START ===========================================')
  

  # ------------------------ Get Table Columns Info START ------------------------
  table_all_column_names_arr = select_all_column_names_function(postgres_connection, postgres_cursor)
  column_names_match_arr = []
  for i in table_all_column_names_arr:    
    column_names_match_arr.append(i[0])
  # ------------------------ Get Table Columns Info END ------------------------
  
  
  # ------------------------ Loop Match Up Info START ------------------------
  all_users_team_channel_combo = select_all_users_team_channel_function(postgres_connection, postgres_cursor, team_id, channel_id)
  """
  # Method 1 - Arr of dicts
  store_info_arr_of_dicts = []  
  for user_arr in all_users_team_channel_combo:
    store_info_dict = {}
    for j in range(len(column_names_match_arr)):
      col_name = column_names_match_arr[j]
      store_info_dict[col_name] = user_arr[j]
    store_info_arr_of_dicts.append(store_info_dict)
  """
  # Method 2 - Nested Dict
  nested_dict = {}
  total_users = len(all_users_team_channel_combo)
  counter = 0
  while counter < total_users:
    counter_str = str(counter)
    nested_dict[counter_str] = {}
    for j in range(len(column_names_match_arr)):
      col_name = column_names_match_arr[j]
      if col_name == 'user_datetime_account_created':
        nested_dict[counter_str][col_name] = all_users_team_channel_combo[counter][j].strftime("%m/%d/%Y, %H:%M:%S")
      else: 
        nested_dict[counter_str][col_name] = all_users_team_channel_combo[counter][j]
    counter += 1
  
  nested_dict = json.dumps(nested_dict)#.encode('utf-8')
  # ------------------------ Loop Match Up Info END ------------------------


  # ------------------------ Create Variables START ------------------------
  # Insert this sent email into DB
  deleted_account_uuid = create_uuid_function('deleted_team_')
  deleted_account_timestamp = create_timestamp_function()
  # ------------------------ Create Variables END ------------------------


  # ------------------------ Insert To DB START ------------------------
  output_message = insert_triviafy_deleted_accounts_table_function(postgres_connection, postgres_cursor, deleted_account_uuid, deleted_account_timestamp, team_id, channel_id, nested_dict)
  # ------------------------ Insert To DB END ------------------------


  localhost_print_function('=========================================== job_pre_delete_table_checks_function END ===========================================')
  return True
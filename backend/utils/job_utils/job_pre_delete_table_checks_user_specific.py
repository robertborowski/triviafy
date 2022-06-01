# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_one_user_uuid import select_one_user_uuid_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_all_column_names import select_all_column_names_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.db.queries.insert_queries.insert_queries_triviafy_deleted_accounts_table.insert_triviafy_deleted_accounts_table import insert_triviafy_deleted_accounts_table_function
import json
from datetime import datetime
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_team_id_and_channel_id import select_team_id_and_channel_id_function



# -------------------------------------------------------------- Main
def job_pre_delete_table_checks_user_specific_function(postgres_connection, postgres_cursor, user_uuid):
  localhost_print_function('=========================================== job_pre_delete_table_checks_user_specific_function START ===========================================')
  

  # ------------------------ Get Table Columns Info START ------------------------
  table_all_column_names_arr = select_all_column_names_function(postgres_connection, postgres_cursor)
  column_names_match_arr = []
  for i in table_all_column_names_arr:    
    column_names_match_arr.append(i[0])
  # ------------------------ Get Table Columns Info END ------------------------
  
  
  # ------------------------ Loop Match Up Info START ------------------------
  one_specific_user_tuple = select_one_user_uuid_function(postgres_connection, postgres_cursor, user_uuid)
  
  # Nested Dict
  nested_dict = {}
  counter = 0
  counter_str = str(counter)
  nested_dict[counter_str] = {}
  for col_name in column_names_match_arr:
    if col_name == 'user_datetime_account_created':
      nested_dict[counter_str][col_name] = one_specific_user_tuple[counter].strftime("%m/%d/%Y, %H:%M:%S")
    else: 
      nested_dict[counter_str][col_name] = one_specific_user_tuple[counter]
    counter += 1

  nested_dict = json.dumps(nested_dict)#.encode('utf-8')
  # ------------------------ Loop Match Up Info END ------------------------


  # ------------------------ Create Variables START ------------------------
  # Insert this sent email into DB
  deleted_account_uuid = create_uuid_function('deleted_person_')
  deleted_account_timestamp = create_timestamp_function()
  # ------------------------ Create Variables END ------------------------


  # ------------------------ Get user's team id and channel id Start ------------------------
  team_channel_ids_arr = select_team_id_and_channel_id_function(postgres_connection, postgres_cursor, user_uuid)
  team_id = team_channel_ids_arr[0]
  channel_id = team_channel_ids_arr[1]
  # ------------------------ Get user's team id and channel id END ------------------------


  # ------------------------ Insert To DB START ------------------------
  output_message = insert_triviafy_deleted_accounts_table_function(postgres_connection, postgres_cursor, deleted_account_uuid, deleted_account_timestamp, team_id, channel_id, nested_dict)
  # ------------------------ Insert To DB END ------------------------


  localhost_print_function('=========================================== job_pre_delete_table_checks_user_specific_function END ===========================================')
  return True
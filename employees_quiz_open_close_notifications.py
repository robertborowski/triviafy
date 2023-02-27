# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.employees import select_manual_function
from datetime import datetime, timedelta
import os, time
# ------------------------ imports end ------------------------

# ------------------------ set timezone start ------------------------
# Set the timezone of the application when user creates account is will be in US/Easterm time
os.environ['TZ'] = 'US/Eastern'
time.tzset()
# ------------------------ set timezone end ------------------------

# ------------------------ individual function start ------------------------
def get_current_timestamp_function():
  current_timestamp = datetime.now()
  current_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
  current_timestamp = datetime.strptime(current_timestamp, "%Y-%m-%d %H:%M:%S")
  return current_timestamp
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def employees_quiz_open_close_notifications():
  localhost_print_function(' ------------------------ employees_quiz_open_close_notifications start ------------------------ ')
  # ------------------------ open connection start ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ open connection end ------------------------
  # ------------------------ get all groups start ------------------------
  db_groups_arr_of_dict = select_manual_function(postgres_connection, postgres_cursor, 'select_groups_1')
  # ------------------------ get all groups end ------------------------
  # ------------------------ current datetime start ------------------------
  current_timestamp = get_current_timestamp_function()
  # ------------------------ current datetime end ------------------------
  # ------------------------ loop all groups start ------------------------
  localhost_print_function(' ------------- 0 ------------- ')
  for i_group_dict in db_groups_arr_of_dict:
    localhost_print_function(' ')
    localhost_print_function(f"i_group_dict | type: {type(i_group_dict)} | {i_group_dict}")
    i_group_status = 'start of script'
    # ------------------------ get latest test start ------------------------
    i_group_status = 'no latest test'
    latest_test_id = None
    db_latest_test_dict = {}
    db_latest_test_arr = select_manual_function(postgres_connection, postgres_cursor, 'select_latest_test_1', i_group_dict['public_group_id'])
    if db_latest_test_arr != None and db_latest_test_arr != []:
      db_latest_test_dict = db_latest_test_arr[0]
      i_group_status = 'at least 1 test exists'
      latest_test_id = db_latest_test_dict['id']
      # ------------------------ get latest test status start ------------------------
      latest_test_start_timestamp = db_latest_test_dict['start_timestamp']
      latest_test_end_timestamp = db_latest_test_dict['end_timestamp']
      localhost_print_function(f"latest_test_start_timestamp | type: {type(latest_test_start_timestamp)} | {latest_test_start_timestamp}")
      localhost_print_function(f"latest_test_end_timestamp | type: {type(latest_test_end_timestamp)} | {latest_test_end_timestamp}")
      localhost_print_function(f"current_timestamp | type: {type(current_timestamp)} | {current_timestamp}")
      # ------------------------ get latest test status end ------------------------
    # ------------------------ get latest test end ------------------------
    # ------------------------ get all group settings start ------------------------
    db_group_settings_arr_of_dict = select_manual_function(postgres_connection, postgres_cursor, 'select_group_settings_1', i_group_dict['public_group_id'])
    # ------------------------ get all group settings end ------------------------
  localhost_print_function(' ------------- 0 ------------- ')
  # ------------------------ loop all groups end ------------------------
  # ------------------------ close connection start ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ close connection end ------------------------
  localhost_print_function(' ------------------------ employees_quiz_open_close_notifications end ------------------------ ')
  return True
# ------------------------ individual function end ------------------------

# ------------------------ run function start ------------------------
if __name__ == "__main__":
  employees_quiz_open_close_notifications()
# ------------------------ run function end ------------------------
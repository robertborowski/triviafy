# -------------------------------------------------------------- Imports
from flask import redirect
from datetime import date, timedelta
from backend.db.queries.select_queries.select_queries_triviafy_free_trial_tracker_slack_table.select_triviafy_free_trial_tracker_slack_table_all_authed_id_info import select_triviafy_free_trial_tracker_slack_table_all_authed_id_info_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.update_queries.update_queries_triviafy_free_trial_tracker_slack_table.update_triviafy_free_trial_tracker_slack_table_expired_user import update_triviafy_free_trial_tracker_slack_table_expired_user_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def check_if_free_trial_period_is_expired_days_left_function(user_nested_dict):
  localhost_print_function('=========================================== check_if_free_trial_period_is_expired_days_left_function START ===========================================')

  # Assign Variable
  user_slack_authed_id = user_nested_dict['user_slack_authed_id']

  # ------------------------ Connect To DB START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ Connect To DB END ------------------------


  # ------------------------ Check Free Trial Expire START ------------------------
  # Get slack user info from free trial table, this should not be blank, it was inserted when account was made
  user_free_trial_row_status_arr = select_triviafy_free_trial_tracker_slack_table_all_authed_id_info_function(postgres_connection, postgres_cursor, user_slack_authed_id)
  if user_free_trial_row_status_arr == None:
    localhost_print_function('=========================================== check_if_free_trial_period_is_expired_days_left_function END ===========================================')
    return None
  
  # Assign variables based on result arr
  free_trial_end_timestamp = user_free_trial_row_status_arr[3].date()   # datetime.date
  free_trial_period_is_expired = user_free_trial_row_status_arr[7]      # bool
  free_trial_end_date = free_trial_end_timestamp.strftime('%Y-%m-%d')   # str

  # Assign variables based on today
  today_date_timestamp = date.today()                                   # datetime.date

  trial_period_days_left_timedelta = free_trial_end_timestamp - today_date_timestamp    # datetime.timedelta
  trial_period_days_left_int = trial_period_days_left_timedelta.days    # int
  # ------------------------ Check Free Trial Expire END ------------------------


  # ------------------------ Update Free Trial Expire START ------------------------
  if trial_period_days_left_int < 0:
    free_trial_period_is_expired == True
    trial_period_days_left_int = -1
    output_message = update_triviafy_free_trial_tracker_slack_table_expired_user_function(postgres_connection, postgres_cursor, user_slack_authed_id)
  # ------------------------ Update Free Trial Expire END ------------------------


  # ------------------------ Close Connection To DB START ------------------------
  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Close Connection To DB END ------------------------


  # ------------------------ Append User Nested Dict START ------------------------
  if free_trial_period_is_expired == None:
    localhost_print_function('There is no user found in the free trial table')
    return None
  elif free_trial_period_is_expired == True:
    localhost_print_function('user free trial has expired')
    return None
  else:
    user_nested_dict['free_trial_period_is_expired'] = free_trial_period_is_expired
    user_nested_dict['trial_period_days_left_int'] = trial_period_days_left_int
    user_nested_dict['free_trial_end_date'] = free_trial_end_date
  # ------------------------ Append User Nested Dict END ------------------------
  

  localhost_print_function('=========================================== check_if_free_trial_period_is_expired_days_left_function END ===========================================')
  return user_nested_dict
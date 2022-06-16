# -------------------------------------------------------------- Imports
from flask import redirect
from datetime import date, timedelta
from backend.db.queries.select_queries.select_queries_triviafy_free_trial_tracker_slack_table.select_triviafy_free_trial_tracker_slack_table_all_authed_id_info import select_triviafy_free_trial_tracker_slack_table_all_authed_id_info_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.update_queries.update_queries_triviafy_free_trial_tracker_slack_table.update_triviafy_free_trial_tracker_slack_table_expired_user import update_triviafy_free_trial_tracker_slack_table_expired_user_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_slack_payment_status_table.select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only import select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only_function

# -------------------------------------------------------------- Main Function
def check_if_user_team_channel_combo_paid_latest_month_function(user_nested_dict):
  localhost_print_function('=========================================== check_if_user_team_channel_combo_paid_latest_month_function START ===========================================')

  # Get/assign variables
  slack_team_id = user_nested_dict['user_slack_workspace_team_id']
  slack_channel_id = user_nested_dict['user_slack_channel_id']

  # ------------------------ Get Today's Date Information START ------------------------
  # Today's date
  today_date = date.today()
  today_date_split_arr = str(today_date).split('-')
  # Separate Today's date into year month and day
  today_date_year = today_date_split_arr[0]
  today_date_month = today_date_split_arr[1]
  today_date_date = today_date_split_arr[2]
  # ------------------------ Get Today's Date Information END ------------------------

  # ------------------------ Pull Info From DB START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()

  # Pull result from table
  team_channel_year_month_combo_exists_in_db = select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only_function(postgres_connection, postgres_cursor, slack_team_id, slack_channel_id, today_date_year, today_date_month)

  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Pull Info From DB END ------------------------

  if team_channel_year_month_combo_exists_in_db == None:
    return False
  else:
    paid_status_slack_team_channel_year_month = team_channel_year_month_combo_exists_in_db[0]
    localhost_print_function('=========================================== check_if_user_team_channel_combo_paid_latest_month_function END ===========================================')
    return paid_status_slack_team_channel_year_month
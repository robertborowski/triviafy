# -------------------------------------------------------------- Imports
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.latest_quiz_utils.supporting_make_company_latest_quiz_utils.get_previous_week_dates_data_dict import get_previous_week_dates_data_dict_function
from backend.db.queries.select_queries.select_queries_triviafy_quiz_master_table.select_triviafy_latest_quiz_info import select_triviafy_latest_quiz_info_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def get_previous_week_company_quiz_if_exists_function(user_nested_dict):
  localhost_print_function('=========================================== get_previous_week_company_quiz_if_exists_function START ===========================================')

  # ------------------------ Get Variables From User Object START ------------------------
  slack_workspace_team_id = user_nested_dict['user_slack_workspace_team_id']
  slack_channel_id = user_nested_dict['user_slack_channel_id']
  # ------------------------ Get Variables From User Object END ------------------------


  # ------------------------ This Week Dates Data Dict START ------------------------
  previous_week_dates_dict = get_previous_week_dates_data_dict_function()

  monday_date = previous_week_dates_dict['Monday']
  tuesday_date = previous_week_dates_dict['Tuesday']
  wednesday_date = previous_week_dates_dict['Wednesday']
  thursday_date = previous_week_dates_dict['Thursday']
  friday_date = previous_week_dates_dict['Friday']
  saturday_date = previous_week_dates_dict['Saturday']
  sunday_date = previous_week_dates_dict['Sunday']
  # ------------------------ This Week Dates Data Dict END ------------------------


  # ------------------------ Get Company Latest Quiz Info START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()

  # Get latest company quiz info
  previous_week_quiz_info_arr = select_triviafy_latest_quiz_info_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id, monday_date, tuesday_date, wednesday_date, thursday_date, friday_date, saturday_date, sunday_date)

  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Get Company Latest Quiz Info END ------------------------

  localhost_print_function('returing previous_week_quiz_info_arr')
  localhost_print_function('=========================================== get_previous_week_company_quiz_if_exists_function END ===========================================')
  return previous_week_quiz_info_arr
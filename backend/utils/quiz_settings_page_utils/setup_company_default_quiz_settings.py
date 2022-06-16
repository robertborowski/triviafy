# -------------------------------------------------------------- Imports
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.insert_queries.insert_queries_triviafy_company_quiz_settings_slack_table.insert_triviafy_company_quiz_settings_slack_table import insert_triviafy_company_quiz_settings_slack_table_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def setup_company_default_quiz_settings_function(user_slack_workspace_team_id, user_slack_channel_id):
  localhost_print_function('=========================================== setup_company_default_quiz_settings_function START ===========================================')

  # ------------------------ Set Default Quiz Settings START ------------------------
  uuid_company_quiz_settings = create_uuid_function('quiz_settg')
  company_quiz_settings_last_updated_timestamp = create_timestamp_function()
  company_quiz_settings_start_day = "Monday"
  company_quiz_settings_start_time = '1 PM'
  company_quiz_settings_end_day = "Friday"
  company_quiz_settings_end_time = '1 PM'
  company_quiz_settings_questions_per_quiz = '10'
  company_quiz_settings_slack_workspace_team_id = user_slack_workspace_team_id
  company_quiz_settings_slack_channel_id = user_slack_channel_id
  # ------------------------ Set Default Quiz Settings END ------------------------


  # ------------------------ Insert into DB START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()

  insert_attempt_output_message = insert_triviafy_company_quiz_settings_slack_table_function(postgres_connection, postgres_cursor, uuid_company_quiz_settings, company_quiz_settings_last_updated_timestamp, company_quiz_settings_start_day, company_quiz_settings_start_time, company_quiz_settings_end_day, company_quiz_settings_end_time, company_quiz_settings_questions_per_quiz, company_quiz_settings_slack_workspace_team_id, company_quiz_settings_slack_channel_id)
  localhost_print_function(insert_attempt_output_message)

  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Insert into DB END ------------------------

  localhost_print_function('=========================================== setup_company_default_quiz_settings_function END ===========================================')
  return True
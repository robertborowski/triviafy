# -------------------------------------------------------------- Imports
from datetime import date
from backend.db.queries.select_queries.select_queries_triviafy_company_quiz_settings_slack_table.select_company_quiz_settings_all_companies import select_company_quiz_settings_all_companies_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.latest_quiz_utils.get_latest_company_quiz_if_exists import get_latest_company_quiz_if_exists_function
from backend.utils.latest_quiz_utils.make_company_latest_quiz import make_company_latest_quiz_function
import os, time
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_free_trial_tracker_slack_table.select_triviafy_free_trial_tracker_slack_table_end_timestamp import select_triviafy_free_trial_tracker_slack_table_end_timestamp_function
from backend.db.queries.select_queries.select_queries_triviafy_slack_payment_status_table.select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only import select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only_function

# -------------------------------------------------------------- Main Function
def job_weekly_make_latest_quizzes_for_all_companies_function():
  localhost_print_function('=========================================== job_weekly_make_latest_quizzes_for_all_companies_function START ===========================================')
  

  # ------------------------ Set Timezone START ------------------------
  # Set the timezone of the application when user creates account is will be in US/Easterm time
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  # ------------------------ Set Timezone END ------------------------
  
  
  # ------------------------ Running on localhost START ------------------------
  # Check environment variable that was passed in from user on the command line
  server_env = os.environ.get('TESTING', 'false')
  if server_env and server_env == 'true':
    localhost_print_function('testing mode')
    pass
  # ------------------------ Running on localhost END ------------------------


  # ------------------------ Get Today's Date START ------------------------
  else:
    # Today's date
    today_date = date.today()
    # Today's date, day of week
    today_day_of_week = today_date.strftime('%A')

    if today_day_of_week != 'Sunday':
      localhost_print_function('Today is not Sunday.')
      localhost_print_function('=========================================== job_weekly_make_latest_quizzes_for_all_companies_function END ===========================================')
      return True
  # ------------------------ Get Today's Date END ------------------------


  # ------------------------ Get all slack company quiz settings START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()

  all_companies_quiz_settings_arr = select_company_quiz_settings_all_companies_function(postgres_connection, postgres_cursor)

  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Get all slack company quiz settings START ------------------------


  # ------------------------ Make Quiz For Every Company This Week START ------------------------
  for indv_company_quiz_settings_arr in all_companies_quiz_settings_arr:
    # ------------------------ Check If Latest Quiz Already Exists START ------------------------
    # Get variables from arr
    slack_workspace_team_id = indv_company_quiz_settings_arr[7]
    slack_channel_id = indv_company_quiz_settings_arr[8]

    localhost_print_function('=======================================================')
    localhost_print_function('slack_workspace_team_id {}, slack_channel_id {}'.format(slack_workspace_team_id, slack_channel_id))

    # Put the variables in dict format, becasue a dict is what the get_latest_company_quiz_if_exists_function requires
    function_input_dict = {
      'slack_team_id' : slack_workspace_team_id,
      'slack_channel_id' : slack_channel_id 
    }

    # Check if a quiz was already made for this company
    latest_company_quiz_object = get_latest_company_quiz_if_exists_function(function_input_dict)
    if latest_company_quiz_object != None:
      localhost_print_function('There is already a latest quiz made for this company.')
      pass
    # ------------------------ Check If Latest Quiz Already Exists END ------------------------
    # ------------------------ Make The Latest Quiz For The Week START ------------------------
    else:
      # ------------------------ Check If Free Trial Expired START ------------------------
      # Connect to Postgres database
      postgres_connection, postgres_cursor = postgres_connect_to_database_function()
      
      # Select free trial end date for company team
      company_team_free_trial_end_timestamp = select_triviafy_free_trial_tracker_slack_table_end_timestamp_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)

      # Close postgres db connection
      postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
      
      # Set variables
      today_date_record = date.today()
      free_trial_expired_for_company_team = False

      # Assign variable
      if today_date_record > company_team_free_trial_end_timestamp[0].date():
        free_trial_expired_for_company_team = True
      elif today_date_record <= company_team_free_trial_end_timestamp[0].date():
        free_trial_expired_for_company_team = False
      # ------------------------ Check If Free Trial Expired END ------------------------


      # ------------------------ Check If Paid Latest Month START ------------------------
      if free_trial_expired_for_company_team == True:
        # ------------------------ Get Today's Date Information START ------------------------
        # Today's date
        today_date = date.today()
        today_date_split_arr = str(today_date).split('-')
        # Separate Today's date into year month and day
        today_date_year = today_date_split_arr[0]
        today_date_month = today_date_split_arr[1]
        today_date_date = today_date_split_arr[2]
        # ------------------------ Get Today's Date Information END ------------------------

        # Connect to Postgres database
        postgres_connection, postgres_cursor = postgres_connect_to_database_function()

        # Select if company paid latest month
        company_paid_latest_month = select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id, today_date_year, today_date_month)

        # Close postgres db connection
        postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
        
        if company_paid_latest_month[0] == False:
          localhost_print_function('Cannot make a quiz for this company team because their free trial ended and they did not pay the latest month')
          continue
      # ------------------------ Check If Paid Latest Month END ------------------------


      # ------------------------ Check If Free Trial Expired / Latest Month Paid END ------------------------
      latest_company_quiz_object = make_company_latest_quiz_function(function_input_dict, indv_company_quiz_settings_arr)
      localhost_print_function('Made the latest company quiz from scratch and stored in DB')
    # ------------------------ Make The Latest Quiz For The Week END ------------------------
  # ------------------------ Make Quiz For Every Company This Week END ------------------------

  localhost_print_function('=========================================== job_weekly_make_latest_quizzes_for_all_companies_function END ===========================================')
  return True



# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  job_weekly_make_latest_quizzes_for_all_companies_function()
  
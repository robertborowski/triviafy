# -------------------------------------------------------------- Imports
import os, time
from datetime import date
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_team_channel_combos_with_user_count import select_triviafy_user_login_information_table_slack_all_team_channel_combos_with_user_count_function
from backend.utils.latest_quiz_utils.supporting_make_company_latest_quiz_utils.get_upcoming_week_dates_data_dict import get_upcoming_week_dates_data_dict_function
from backend.utils.job_utils.job_check_db_status_overall_free_trial_table_checks import job_check_db_status_overall_free_trial_table_checks_function
from backend.utils.job_utils.job_check_db_status_overall_payment_status_table_checks import job_check_db_status_overall_payment_status_table_checks_function
from backend.utils.job_utils.job_check_db_status_overall_categories_table_checks import job_check_db_status_overall_categories_table_checks_function
from backend.utils.job_utils.job_check_db_status_overall_quiz_settings_table_checks import job_check_db_status_overall_quiz_settings_table_checks_function
from backend.utils.job_utils.job_check_db_status_overall_quiz_master_table_checks import job_check_db_status_overall_quiz_master_table_checks_function
from backend.utils.job_utils.job_check_db_status_overall_midweek_changes_quiz_settings_table_checks import job_check_db_status_overall_midweek_changes_quiz_settings_table_checks_function

# -------------------------------------------------------------- Main Function
def job_check_db_status_overall_function():
  localhost_print_function('=========================================== job_check_db_status_overall_function START ===========================================')


  # ------------------------ Set Timezone START ------------------------
  # Set the timezone of the application when user creates account is will be in US/Easterm time
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  # ------------------------ Set Timezone END ------------------------


  # ------------------------ Get Today's Date START ------------------------
  # Today's date
  today_date = date.today()
  today_date_split_arr = str(today_date).split('-')
  # Separate Today's date into year month and day
  today_date_year = today_date_split_arr[0]
  today_date_month = today_date_split_arr[1]
  # ------------------------ Get Today's Date END ------------------------


  # ------------------------ Get Upcoming Week Dates START ------------------------
  this_upcoming_week_dates_dict = get_upcoming_week_dates_data_dict_function()

  start_date_monday = this_upcoming_week_dates_dict['Monday']
  start_date_tuesday = this_upcoming_week_dates_dict['Tuesday']
  start_date_wednesday = this_upcoming_week_dates_dict['Wednesday']
  start_date_thursday = this_upcoming_week_dates_dict['Thursday']
  start_date_friday = this_upcoming_week_dates_dict['Friday']
  start_date_saturday = this_upcoming_week_dates_dict['Saturday']
  start_date_sunday = this_upcoming_week_dates_dict['Sunday']
  # ------------------------ Get Upcoming Week Dates END ------------------------


  # ------------------------ DB Conection START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ DB Conection End ------------------------


  # ------------------------ Get Unique team channel combos START ------------------------
  team_channel_combos_with_users_arr = select_triviafy_user_login_information_table_slack_all_team_channel_combos_with_user_count_function(postgres_connection, postgres_cursor)
  # ------------------------ Get Unique team channel combos END ------------------------


  # ------------------------ Loop through each team channel combo START ------------------------
  db_check_dict = {}
  db_check_errors_caught_dict = {}
  for i in team_channel_combos_with_users_arr:
    # initial variables
    team_id = i[0]
    channel_id = i[1]
    team_name = i[2]
    channel_name = i[3]
    total_team_channel_users = i[4]
    localhost_print_function('- - - - - - - - - - - - - - - - - - -')
    localhost_print_function('team_name: {} | channel_name: {}'.format(team_name, channel_name))
    
    # Initial dict
    db_check_dict[team_id] = {}
    db_check_dict[team_id][channel_id] = {}
    db_check_dict[team_id][channel_id]['team_name'] = team_name
    db_check_dict[team_id][channel_id]['channel_name'] = channel_name
    db_check_dict[team_id][channel_id]['total_team_channel_users'] = total_team_channel_users

    # Errors Caught dict
    db_check_errors_caught_dict[team_id] = {}
    db_check_errors_caught_dict[team_id][channel_id] = {}
    db_check_errors_caught_dict[team_id][channel_id]['team_name'] = team_name
    db_check_errors_caught_dict[team_id][channel_id]['channel_name'] = channel_name
    db_check_errors_caught_dict[team_id][channel_id]['total_team_channel_users'] = total_team_channel_users

    # ------------------------ Table Checks - Free Trial START ------------------------
    db_check_dict = job_check_db_status_overall_free_trial_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, today_date, db_check_dict)
    # ------------------------ Table Checks - Free Trial END ------------------------


    # ------------------------ Table Checks - Payment Status START ------------------------
    db_check_dict = job_check_db_status_overall_payment_status_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict, today_date_year, today_date_month)
    # ------------------------ Table Checks - Payment Status END ------------------------


    # ------------------------ Table Checks - Categories Selected START ------------------------
    db_check_dict = job_check_db_status_overall_categories_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict)
    # ------------------------ Table Checks - Categories Selected END ------------------------


    # ------------------------ Table Checks - Quiz Settings START ------------------------
    db_check_dict = job_check_db_status_overall_quiz_settings_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict)
    # ------------------------ Table Checks - Quiz Settings END ------------------------


    # ------------------------ Table Checks - Quiz Master START ------------------------
    db_check_dict = job_check_db_status_overall_quiz_master_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict, start_date_monday, start_date_tuesday, start_date_wednesday, start_date_thursday, start_date_friday, start_date_saturday, start_date_sunday)
    # ------------------------ Table Checks - Quiz Master START ------------------------


    # ------------------------ Table Checks - Mid-Week Changes To Quiz Settings START ------------------------
    db_check_dict = job_check_db_status_overall_midweek_changes_quiz_settings_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict)
    # ------------------------ Table Checks - Mid-Week Changes To Quiz Settings END ------------------------


    # ------------------------ Table Checks - Remaining Questions Per Company Categories START ------------------------
    # ------------------------ Table Checks - Remaining Questions Per Company Categories END ------------------------


  print('= = = = = = = 1 = = = = = = = =')
  print(db_check_dict['abc'])
  print('= = = = = = = 1 = = = = = = = =')
  # ------------------------ Loop through each team channel combo END ------------------------


  # ------------------------ DB Close Conection START ------------------------
  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ DB Close Conection END ------------------------

  localhost_print_function('=========================================== job_check_db_status_overall_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  job_check_db_status_overall_function()
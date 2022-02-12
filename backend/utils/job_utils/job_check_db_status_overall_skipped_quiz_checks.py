# -------------------------------------------------------------- Imports
import math
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_skipped_quiz_count_slack_team_channel_table.select_skipped_quiz_count_team_channel_combo import select_skipped_quiz_count_team_channel_combo_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_team_channel_min_start_date import select_triviafy_user_login_information_table_team_channel_min_start_date_function

# -------------------------------------------------------------- Main
def job_check_db_status_overall_skipped_quiz_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict, today_date):
  localhost_print_function('=========================================== job_check_db_status_overall_skipped_quiz_checks_function START ===========================================')


  # ------------------------ Identify Team Channel Earliest Start Date START ------------------------
  min_account_created_date = select_triviafy_user_login_information_table_team_channel_min_start_date_function(postgres_connection, postgres_cursor, team_id, channel_id)
  min_account_created_date = min_account_created_date.date()
  total_weeks_active = math.floor((today_date - min_account_created_date).days / 7)
  try:
    db_check_dict[team_id][channel_id]['min_account_created_date'] = min_account_created_date
    db_check_dict[team_id][channel_id]['total_weeks_active'] = total_weeks_active
  except:
    db_check_dict[team_id][channel_id]['min_account_created_date'] = None
    db_check_dict[team_id][channel_id]['total_weeks_active'] = None
  # ------------------------ Identify Team Channel Earliest Start Date END ------------------------
  
  
  # ------------------------ Identify Quiz Winner START ------------------------
  team_channel_skipped_quiz_count = select_skipped_quiz_count_team_channel_combo_function(postgres_connection, postgres_cursor, team_id, channel_id)
  if team_channel_skipped_quiz_count != None:
    db_check_dict[team_id][channel_id]['team_channel_skipped_quiz_count'] = team_channel_skipped_quiz_count
  else:
    db_check_dict[team_id][channel_id]['team_channel_skipped_quiz_count'] = None
  # ------------------------ Identify Quiz Winner END ------------------------
  

  localhost_print_function('=========================================== job_check_db_status_overall_skipped_quiz_checks_function END ===========================================')
  return db_check_dict
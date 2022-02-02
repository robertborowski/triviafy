# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_company_quiz_settings_slack_table.select_quiz_settings_team_channel_combo_count import select_quiz_settings_team_channel_combo_count_function
from backend.db.queries.select_queries.select_queries_triviafy_company_quiz_settings_slack_table.select_company_quiz_settings import select_company_quiz_settings_function

# -------------------------------------------------------------- Main
def job_check_db_status_overall_quiz_settings_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict):
  localhost_print_function('=========================================== job_check_db_status_overall_quiz_settings_table_checks_function START ===========================================')
  

  # ------------------------ Check Quiz Settings Rules - Count START ------------------------
  int_quiz_settings_count_team_channel_combo = select_quiz_settings_team_channel_combo_count_function(postgres_connection, postgres_cursor, team_id, channel_id)
  if int_quiz_settings_count_team_channel_combo != 1:
    localhost_print_function('=========================================== job_check_db_status_overall_quiz_settings_table_checks_function END ===========================================')
    print('Error: There is more than 1 row for the team channel combo quiz settings table')
    return False
  # ------------------------ Check Quiz Settings Rules - Count END ------------------------


  # ------------------------ Check Quiz Settings Rules - Latest Date START ------------------------
  quiz_settings_arr = select_company_quiz_settings_function(postgres_connection, postgres_cursor, team_id, channel_id)
  
  quiz_settings_start_day_of_week = quiz_settings_arr[2]
  quiz_settings_start_time_of_day = quiz_settings_arr[3]
  quiz_settings_end_day_of_week = quiz_settings_arr[4]
  quiz_settings_end_time_of_day = quiz_settings_arr[5]
  quiz_settings_questions_per_quiz = quiz_settings_arr[6]

  db_check_dict[team_id][channel_id]['quiz_settings_start_day_of_week'] = quiz_settings_start_day_of_week
  db_check_dict[team_id][channel_id]['quiz_settings_start_time_of_day'] = quiz_settings_start_time_of_day
  db_check_dict[team_id][channel_id]['quiz_settings_end_day_of_week'] = quiz_settings_end_day_of_week
  db_check_dict[team_id][channel_id]['quiz_settings_end_time_of_day'] = quiz_settings_end_time_of_day
  db_check_dict[team_id][channel_id]['quiz_settings_questions_per_quiz'] = quiz_settings_questions_per_quiz
  # ------------------------ Check Quiz Settings Rules - Latest Date END ------------------------

  localhost_print_function('=========================================== job_check_db_status_overall_quiz_settings_table_checks_function END ===========================================')
  return db_check_dict
# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function


# -------------------------------------------------------------- Main
def job_check_db_status_overall_midweek_changes_quiz_settings_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict):
  localhost_print_function('=========================================== job_check_db_status_overall_midweek_changes_quiz_settings_table_checks_function START ===========================================')  
  
  # ------------------------ Check Quiz Settings Mid Week Changes START ------------------------
  if db_check_dict[team_id][channel_id]['quiz_created_this_week'] == False:
    # Quiz Settings mid week change calculations bool
    db_check_dict[team_id][channel_id]['user_quiz_settings_start_day_of_week_unchanged'] = None
    db_check_dict[team_id][channel_id]['user_quiz_settings_start_time_unchanged'] = None
    db_check_dict[team_id][channel_id]['user_quiz_settings_end_day_of_week_unchanged'] = None
    db_check_dict[team_id][channel_id]['user_quiz_settings_end_time_unchanged'] = None
    db_check_dict[team_id][channel_id]['user_quiz_settings_num_questions_unchanged'] = None
  
  else:
    # Quiz Settings mid week change calculations bool
    user_quiz_settings_start_day_of_week_unchanged = db_check_dict[team_id][channel_id]['latest_quiz_start_day_of_week'] == db_check_dict[team_id][channel_id]['quiz_settings_start_day_of_week']
    user_quiz_settings_start_time_unchanged = db_check_dict[team_id][channel_id]['latest_quiz_start_time'] == db_check_dict[team_id][channel_id]['quiz_settings_start_time_of_day']
    user_quiz_settings_end_day_of_week_unchanged = db_check_dict[team_id][channel_id]['latest_quiz_end_day_of_week'] == db_check_dict[team_id][channel_id]['quiz_settings_end_day_of_week']
    user_quiz_settings_end_time_unchanged = db_check_dict[team_id][channel_id]['latest_quiz_end_time'] == db_check_dict[team_id][channel_id]['quiz_settings_end_time_of_day']
    user_quiz_settings_num_questions_unchanged = db_check_dict[team_id][channel_id]['latest_quiz_num_questions'] == db_check_dict[team_id][channel_id]['quiz_settings_questions_per_quiz']

    # Assign variables    
    db_check_dict[team_id][channel_id]['user_quiz_settings_start_day_of_week_unchanged'] = user_quiz_settings_start_day_of_week_unchanged
    db_check_dict[team_id][channel_id]['user_quiz_settings_start_time_unchanged'] = user_quiz_settings_start_time_unchanged
    db_check_dict[team_id][channel_id]['user_quiz_settings_end_day_of_week_unchanged'] = user_quiz_settings_end_day_of_week_unchanged
    db_check_dict[team_id][channel_id]['user_quiz_settings_end_time_unchanged'] = user_quiz_settings_end_time_unchanged
    db_check_dict[team_id][channel_id]['user_quiz_settings_num_questions_unchanged'] = user_quiz_settings_num_questions_unchanged
  # ------------------------ Check Quiz Settings Mid Week Changes END ------------------------


  localhost_print_function('=========================================== job_check_db_status_overall_midweek_changes_quiz_settings_table_checks_function END ===========================================')
  return db_check_dict
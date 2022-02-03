# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.latest_quiz_utils.check_if_today_is_greater_than_equal_to_latest_quiz_start_date_utils.check_if_today_is_greater_than_equal_to_latest_quiz_start_date import check_if_today_is_greater_than_equal_to_latest_quiz_start_date_function
from backend.db.queries.select_queries.select_queries_triviafy_quiz_master_table.select_triviafy_latest_quiz_info_specific_company import select_triviafy_latest_quiz_info_specific_company_function


# -------------------------------------------------------------- Main
def job_check_db_status_overall_quiz_master_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict, start_date_monday, start_date_tuesday, start_date_wednesday, start_date_thursday, start_date_friday, start_date_saturday, start_date_sunday):
  localhost_print_function('=========================================== job_check_db_status_overall_quiz_master_table_checks_function START ===========================================')
  

  # ------------------------ Check Quiz Master Rules - If Past Start Date START ------------------------
  quiz_settings_start_day_of_week = db_check_dict[team_id][channel_id]['quiz_settings_start_day_of_week']
  quiz_settings_start_time_of_day = db_check_dict[team_id][channel_id]['quiz_settings_start_time_of_day']
  quiz_settings_end_day_of_week = db_check_dict[team_id][channel_id]['quiz_settings_end_day_of_week']
  quiz_settings_end_time_of_day = db_check_dict[team_id][channel_id]['quiz_settings_end_time_of_day']
  quiz_settings_questions_per_quiz = db_check_dict[team_id][channel_id]['quiz_settings_questions_per_quiz']

  latest_quiz_should_be_open_check = check_if_today_is_greater_than_equal_to_latest_quiz_start_date_function(quiz_settings_start_day_of_week, quiz_settings_start_time_of_day)
  db_check_dict[team_id][channel_id]['latest_quiz_should_be_open_check'] = latest_quiz_should_be_open_check
  # ------------------------ Check Quiz Master Rules - If Past Start Date END ------------------------
  
  
  
  # ------------------------ Check Quiz Master Rules - Check If Quiz Made START ------------------------
  # Get latest company quiz info
  latest_quiz_info_company_arr = select_triviafy_latest_quiz_info_specific_company_function(postgres_connection, postgres_cursor, start_date_monday, start_date_tuesday, start_date_wednesday, start_date_thursday, start_date_friday, start_date_saturday, start_date_sunday, team_id, channel_id)
  
  if latest_quiz_info_company_arr == None:
    db_check_dict[team_id][channel_id]['quiz_created_this_week'] = False
    # Assign to dictionary
    db_check_dict[team_id][channel_id]['quiz_master_latest_quiz_uuid'] = None
    db_check_dict[team_id][channel_id]['latest_quiz_timestamp_created'] = None
    db_check_dict[team_id][channel_id]['latest_quiz_start_date'] = None
    db_check_dict[team_id][channel_id]['latest_quiz_start_day_of_week'] = None
    db_check_dict[team_id][channel_id]['latest_quiz_start_time'] = None
    db_check_dict[team_id][channel_id]['latest_quiz_end_date'] = None
    db_check_dict[team_id][channel_id]['latest_quiz_end_day_of_week'] = None
    db_check_dict[team_id][channel_id]['latest_quiz_end_time'] = None
    db_check_dict[team_id][channel_id]['latest_quiz_num_questions'] = None
    db_check_dict[team_id][channel_id]['latest_quiz_count'] = None
  
  else:
    db_check_dict[team_id][channel_id]['quiz_created_this_week'] = True
    # Assign variables from pull
    quiz_master_latest_quiz_uuid = latest_quiz_info_company_arr[0][0]     # str
    quiz_master_timestamp_created = latest_quiz_info_company_arr[0][1]    # datetime
    quiz_master_start_date = latest_quiz_info_company_arr[0][4]           # datetime
    quiz_master_start_day_of_week = latest_quiz_info_company_arr[0][5]    # str
    quiz_master_start_time = latest_quiz_info_company_arr[0][6]           # str
    quiz_master_end_date = latest_quiz_info_company_arr[0][7]             # datetime
    quiz_master_end_day_of_week = latest_quiz_info_company_arr[0][8]      # str
    quiz_master_end_time = latest_quiz_info_company_arr[0][9]             # str
    quiz_master_num_questions = latest_quiz_info_company_arr[0][10]       # int
    quiz_master_quiz_count = latest_quiz_info_company_arr[0][12]          # int
    # Assign to dictionary
    db_check_dict[team_id][channel_id]['quiz_master_latest_quiz_uuid'] = quiz_master_latest_quiz_uuid
    db_check_dict[team_id][channel_id]['latest_quiz_timestamp_created'] = quiz_master_timestamp_created
    db_check_dict[team_id][channel_id]['latest_quiz_start_date'] = quiz_master_start_date
    db_check_dict[team_id][channel_id]['latest_quiz_start_day_of_week'] = quiz_master_start_day_of_week
    db_check_dict[team_id][channel_id]['latest_quiz_start_time'] = quiz_master_start_time
    db_check_dict[team_id][channel_id]['latest_quiz_end_date'] = quiz_master_end_date
    db_check_dict[team_id][channel_id]['latest_quiz_end_day_of_week'] = quiz_master_end_day_of_week
    db_check_dict[team_id][channel_id]['latest_quiz_end_time'] = quiz_master_end_time
    db_check_dict[team_id][channel_id]['latest_quiz_num_questions'] = quiz_master_num_questions
    db_check_dict[team_id][channel_id]['latest_quiz_count'] = quiz_master_quiz_count
  # ------------------------ Check Quiz Master Rules - Check If Quiz Made END ------------------------


  localhost_print_function('=========================================== job_check_db_status_overall_quiz_master_table_checks_function END ===========================================')
  return db_check_dict
# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_free_trial_tracker_slack_table.select_free_trial_min_max_start_end_match_check import select_free_trial_min_max_start_end_match_check_function
from backend.db.queries.select_queries.select_queries_triviafy_free_trial_tracker_slack_table.select_free_trial_matching_expire_status import select_free_trial_matching_expire_status_function
from backend.db.queries.select_queries.select_queries_triviafy_free_trial_tracker_slack_table.select_free_trial_total_accounted_for import select_free_trial_total_accounted_for_function

# -------------------------------------------------------------- Main
def job_check_db_status_overall_free_trial_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, today_date, db_check_dict):
  localhost_print_function('=========================================== job_check_db_status_overall_free_trial_table_checks_function START ===========================================')
  
  # ------------------------ Assign Variables START ------------------------
  total_team_channel_users = db_check_dict[team_id][channel_id]['total_team_channel_users']
  # ------------------------ Assign Variables END ------------------------


  # ------------------------ Check Free Trial Rules - Count Free Trials START ------------------------
  free_trial_total_users_arr = select_free_trial_total_accounted_for_function(postgres_connection, postgres_cursor, team_id, channel_id)
  free_trial_total_users_count = free_trial_total_users_arr[0]
  if total_team_channel_users != free_trial_total_users_count:
    localhost_print_function('=========================================== job_check_db_status_overall_function END ===========================================')
    print('Error: Free Trial total users not matching for all users for this team channel combo. Total users = {}, while free trial total users = {}'.format(total_team_channel_users, free_trial_total_users_count))
    return False
  else:
    db_check_dict[team_id][channel_id]['free_trial_total_users_count_match'] = True
  # ------------------------ Check Free Trial Rules - Count Free Trials EMD ------------------------


  # ------------------------ Check Free Trial Rules - Same Start End Dates START ------------------------
  free_trial_start_end_match_check_arr = select_free_trial_min_max_start_end_match_check_function(postgres_connection, postgres_cursor, team_id, channel_id)
  free_trial_times_arr = free_trial_start_end_match_check_arr[0]
  free_trial_min_start_date = free_trial_times_arr[0]
  free_trial_max_start_date = free_trial_times_arr[1]
  free_trial_min_end_date = free_trial_times_arr[2]
  free_trial_max_end_date = free_trial_times_arr[3]
  if free_trial_min_start_date != free_trial_max_start_date or free_trial_min_end_date != free_trial_max_end_date:
    localhost_print_function('=========================================== job_check_db_status_overall_function END ===========================================')
    print('Error: Free Trial start/end times are not matching for all users for this team channel combo')
    return False
  # ------------------------ Check Free Trial Rules - Same Start End Dates END ------------------------


  # ------------------------ Check Free Trial Rules - Expire Status START ------------------------
  free_trial_expire_status_arr = select_free_trial_matching_expire_status_function(postgres_connection, postgres_cursor, team_id, channel_id)
  if len(free_trial_expire_status_arr) != 1:
    localhost_print_function('=========================================== job_check_db_status_overall_function END ===========================================')
    print('Error: Free Trial Expire status is not the same for all users for this team channel combo')
    return False
  else:
    free_trial_expire_status = free_trial_expire_status_arr[0][0]
    db_check_dict[team_id][channel_id]['free_trial_expired'] = free_trial_expire_status
    free_trial_days_left = -1
    if free_trial_expire_status == False:
      free_trial_days_left = (free_trial_min_end_date.date() - today_date).days
      db_check_dict[team_id][channel_id]['free_trial_days_left'] = free_trial_days_left
    else:
      db_check_dict[team_id][channel_id]['free_trial_days_left'] = free_trial_days_left
  # ------------------------ Check Free Trial Rules - Expire Status END ------------------------

  localhost_print_function('=========================================== job_check_db_status_overall_free_trial_table_checks_function END ===========================================')
  return db_check_dict
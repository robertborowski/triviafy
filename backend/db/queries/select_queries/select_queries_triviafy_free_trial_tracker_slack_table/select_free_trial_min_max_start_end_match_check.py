# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_free_trial_min_max_start_end_match_check_function(postgres_connection, postgres_cursor, team_id, channel_id):
  localhost_print_function('=========================================== select_free_trial_min_max_start_end_match_check_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT MIN(f.free_trial_start_timestamp)AS min_start,MAX(f.free_trial_start_timestamp)AS max_start,MIN(f.free_trial_end_timestamp)AS min_end,MAX(f.free_trial_end_timestamp)AS max_end FROM triviafy_free_trial_tracker_slack_table AS f WHERE f.free_trial_user_slack_workspace_team_id_fk=%s AND f.free_trial_user_slack_channel_id_fk=%s;", [team_id, channel_id])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = postgres_cursor.fetchall()
    if result_arr == None or result_arr == []:
      localhost_print_function('=========================================== select_free_trial_min_max_start_end_match_check_function END ===========================================')
      return None

    localhost_print_function('=========================================== select_free_trial_min_max_start_end_match_check_function END ===========================================')
    return result_arr
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_free_trial_min_max_start_end_match_check_function END ===========================================')
      return None
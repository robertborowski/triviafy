# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_free_trial_identify_duplicate_auth_id_and_uuid_combo_function(postgres_connection, postgres_cursor, team_id, channel_id):
  localhost_print_function('=========================================== select_free_trial_identify_duplicate_auth_id_and_uuid_combo_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT f.free_trial_user_slack_authed_id_fk,f.free_trial_user_uuid_fk,COUNT(f.*)AS dups_count FROM triviafy_user_login_information_table_slack AS l LEFT JOIN triviafy_free_trial_tracker_slack_table AS f ON(l.user_slack_authed_id=f.free_trial_user_slack_authed_id_fk)OR(l.user_uuid=f.free_trial_user_uuid_fk)WHERE l.user_slack_workspace_team_id=%s AND l.user_slack_channel_id=%s GROUP BY f.free_trial_user_slack_authed_id_fk,f.free_trial_user_uuid_fk HAVING COUNT(f.*)>1 ORDER BY f.free_trial_user_slack_authed_id_fk,f.free_trial_user_uuid_fk;", [team_id, channel_id])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = postgres_cursor.fetchall()
    if result_arr == None or result_arr == []:
      localhost_print_function('=========================================== select_free_trial_identify_duplicate_auth_id_and_uuid_combo_function END ===========================================')
      return None

    localhost_print_function('=========================================== select_free_trial_identify_duplicate_auth_id_and_uuid_combo_function END ===========================================')
    return result_arr[0]
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_free_trial_identify_duplicate_auth_id_and_uuid_combo_function END ===========================================')
      return None
# -------------------------------------------------------------- Imports
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_company_slack_authed_ids import select_triviafy_user_login_information_table_slack_all_company_slack_authed_ids_function
from backend.db.queries.select_queries.select_queries_triviafy_free_trial_tracker_slack_table.select_triviafy_free_trial_tracker_slack_table_all_authed_id_info import select_triviafy_free_trial_tracker_slack_table_all_authed_id_info_function
from datetime import datetime
from backend.db.queries.update_queries.update_queries_triviafy_free_trial_tracker_slack_table.update_triviafy_free_trial_tracker_slack_table_earliest_start_end_whole_team import update_triviafy_free_trial_tracker_slack_table_earliest_start_end_whole_team_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
 
# -------------------------------------------------------------- Main Function
def update_start_end_free_trial_info_whole_team_function(postgres_connection, postgres_cursor, user_slack_workspace_team_id, user_slack_channel_id):
  localhost_print_function('=========================================== update_start_end_free_trial_info_whole_team_function START ===========================================')

  # ------------------------ Update All Team Members Same Start End Dates START ------------------------
  all_current_team_members_authed_id_for_this_user_arr = select_triviafy_user_login_information_table_slack_all_company_slack_authed_ids_function(postgres_connection, postgres_cursor, user_slack_workspace_team_id, user_slack_channel_id)
  
  if len(all_current_team_members_authed_id_for_this_user_arr) > 1:
    # Make variable for earliest free trial start timestamp
    free_trial_start_timestamp = datetime.now()
    free_trial_end_timestamp = datetime.now()

    # Loop through each team member to find the earliest free trial start timestamp
    for team_member_authed_id in all_current_team_members_authed_id_for_this_user_arr:
      team_member_free_trial_info_arr = select_triviafy_free_trial_tracker_slack_table_all_authed_id_info_function(postgres_connection, postgres_cursor, team_member_authed_id[0])
      
      team_member_free_trial_start_timestamp = team_member_free_trial_info_arr[2]
      team_member_free_trial_end_timestamp = team_member_free_trial_info_arr[3]

      if team_member_free_trial_start_timestamp < free_trial_start_timestamp:
        free_trial_start_timestamp = team_member_free_trial_start_timestamp
        free_trial_end_timestamp = team_member_free_trial_end_timestamp

    # Loop through each team member again, now update the start and end date so that they are the same for all team members
    for team_member_authed_id in all_current_team_members_authed_id_for_this_user_arr:
      output_message = update_triviafy_free_trial_tracker_slack_table_earliest_start_end_whole_team_function(postgres_connection, postgres_cursor, free_trial_start_timestamp, free_trial_end_timestamp, team_member_authed_id[0])
  # ------------------------ Update All Team Members Same Start End Dates END ------------------------

  localhost_print_function('=========================================== update_start_end_free_trial_info_whole_team_function END ===========================================')
  return True
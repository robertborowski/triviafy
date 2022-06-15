# -------------------------------------------------------------- Imports
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.utils.free_trial_period_utils.free_trial_period_start_end import free_trial_period_start_end_function
from backend.db.queries.insert_queries.insert_queries_triviafy_free_trial_tracker_slack_table.insert_triviafy_free_trial_tracker_slack_table import insert_triviafy_free_trial_tracker_slack_table_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_company_slack_authed_ids import select_triviafy_user_login_information_table_slack_all_company_slack_authed_ids_function
from backend.db.queries.select_queries.select_queries_triviafy_free_trial_tracker_slack_table.select_triviafy_free_trial_tracker_slack_table_all_authed_id_info import select_triviafy_free_trial_tracker_slack_table_all_authed_id_info_function
from datetime import datetime
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function


# -------------------------------------------------------------- Main Function
def update_insert_free_trial_info_team_function(postgres_connection, postgres_cursor, user_slack_authed_id, user_slack_workspace_team_id, user_slack_channel_id, user_uuid):
  localhost_print_function('=========================================== update_insert_free_trial_info_team_function START ===========================================')

  # ------------------------ Free Trial Period Tracker START ------------------------
  # Check if user slack authed id is already in the free trial table
  slack_user_authed_id_exists_already = select_triviafy_free_trial_tracker_slack_table_all_authed_id_info_function(postgres_connection, postgres_cursor, user_slack_authed_id)
  if slack_user_authed_id_exists_already == None:
    # Set variables for DB
    uuid_free_trial = create_uuid_function('free_trial_')
    free_trial_created_timestamp = create_timestamp_function()
    free_trial_user_slack_authed_id_fk = user_slack_authed_id
    free_trial_user_slack_workspace_team_id_fk = user_slack_workspace_team_id
    free_trial_user_slack_channel_id_fk = user_slack_channel_id
    free_trial_period_is_expired = False
    free_trial_user_uuid_fk = user_uuid
    
    # ------------------------ Get Earliest Team Member Free Trial Dates START ------------------------
    all_current_team_members_authed_id_for_this_user_arr = select_triviafy_user_login_information_table_slack_all_company_slack_authed_ids_function(postgres_connection, postgres_cursor, free_trial_user_slack_workspace_team_id_fk, free_trial_user_slack_channel_id_fk)

    if all_current_team_members_authed_id_for_this_user_arr == None:
      free_trial_start_timestamp, free_trial_end_timestamp = free_trial_period_start_end_function()
    
    else:
      # Make variable for earliest free trial start timestamp
      free_trial_start_timestamp = datetime.now()
      # Loop through each team member to find the earliest free trial start timestamp
      for team_member_authed_id in all_current_team_members_authed_id_for_this_user_arr:
        team_member_free_trial_info_arr = select_triviafy_free_trial_tracker_slack_table_all_authed_id_info_function(postgres_connection, postgres_cursor, team_member_authed_id[0])
        
        team_member_free_trial_start_timestamp = team_member_free_trial_info_arr[2]
        team_member_free_trial_end_timestamp = team_member_free_trial_info_arr[3]

        if team_member_free_trial_start_timestamp < free_trial_start_timestamp:
          free_trial_start_timestamp = team_member_free_trial_start_timestamp
          free_trial_end_timestamp = team_member_free_trial_end_timestamp
    # ------------------------ Get Earliest Team Member Free Trial Dates END ------------------------

    # ------------------------ Insert Free Trial Info To DB START ------------------------
    output_message = insert_triviafy_free_trial_tracker_slack_table_function(postgres_connection, postgres_cursor, uuid_free_trial, free_trial_created_timestamp, free_trial_start_timestamp, free_trial_end_timestamp, free_trial_user_slack_authed_id_fk, free_trial_user_slack_workspace_team_id_fk, free_trial_user_slack_channel_id_fk, free_trial_period_is_expired, free_trial_user_uuid_fk)
    localhost_print_function(output_message)
    # ------------------------ Insert Free Trial Info To DB END ------------------------
  # ------------------------ Free Trial Period Tracker END ------------------------

  localhost_print_function('=========================================== update_insert_free_trial_info_team_function END ===========================================')
  return True
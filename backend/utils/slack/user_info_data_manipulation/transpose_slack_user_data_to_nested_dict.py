# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def transpose_slack_user_data_to_nested_dict_function(user_uuid, user_datetime_account_created, user_first_name, user_last_name, user_display_name, user_email, user_slack_authed_id, user_slack_workspace_team_id, user_slack_workspace_team_name, user_slack_channel_id, user_slack_channel_name, user_company_name, user_slack_bot_user_id, user_is_payment_admin_teamid_channelid,  user_slack_token_type, user_slack_access_token, user_slack_timezone, user_slack_timezone_label, user_slack_timezone_offset, user_slack_job_title, user_slack_email_permission_granted, user_slack_team_channel_incoming_webhook_url, user_slack_new_user_questionnaire_answered, user_slack_new_user_categories_selected):
  localhost_print_function('=========================================== transpose_slack_user_data_to_nested_dict_function START ===========================================')

  user_dict = {
    'user_uuid' : user_uuid,
    'user_datetime_account_created' : user_datetime_account_created,
    'user_first_name' : user_first_name,
    'user_last_name' : user_last_name,
    'user_display_name' : user_display_name,
    'user_email' : user_email,
    'user_slack_authed_id' : user_slack_authed_id,
    'user_slack_workspace_team_id' : user_slack_workspace_team_id,
    'user_slack_workspace_team_name' : user_slack_workspace_team_name,
    'user_slack_channel_id' : user_slack_channel_id,
    'user_slack_channel_name' : user_slack_channel_name,
    'user_company_name' : user_company_name,
    'user_slack_bot_user_id' : user_slack_bot_user_id,
    'user_is_payment_admin_teamid_channelid' : user_is_payment_admin_teamid_channelid,
    'user_slack_token_type' : user_slack_token_type,
    'user_slack_access_token' : user_slack_access_token,
    'user_slack_timezone' : user_slack_timezone,
    'user_slack_timezone_label' : user_slack_timezone_label,
    'user_slack_timezone_offset' : user_slack_timezone_offset,
    'user_slack_job_title' : user_slack_job_title,
    'user_slack_email_permission_granted' : user_slack_email_permission_granted,
    'user_slack_team_channel_incoming_webhook_url' : user_slack_team_channel_incoming_webhook_url,
    'user_slack_new_user_questionnaire_answered' : user_slack_new_user_questionnaire_answered,
    'user_slack_new_user_categories_selected' : user_slack_new_user_categories_selected
  }

  localhost_print_function('=========================================== transpose_slack_user_data_to_nested_dict_function END ===========================================')
  return user_dict
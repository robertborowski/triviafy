# -------------------------------------------------------------- Imports
from flask import request
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_login_info_one_user import select_triviafy_user_login_information_table_slack_all_login_info_one_user_function
import os
from backend.page_templates_backend.slack_confirm_oauth_redirect_dashboard_backend.user_store_loggedin_data_redis import user_store_loggedin_data_redis_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.free_trial_period_utils.check_if_free_trial_period_is_expired_days_left import check_if_free_trial_period_is_expired_days_left_function

# -------------------------------------------------------------- Main Function
def update_user_nested_dict_information_after_account_edit_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id, user_uuid):
  localhost_print_function('=========================================== update_user_nested_dict_information_after_account_edit_function START ===========================================')
  
  # Pull all login information from DB
  pulled_user_arr = select_triviafy_user_login_information_table_slack_all_login_info_one_user_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id, user_uuid)
  
  user_dict = {
    'user_uuid' : pulled_user_arr[0],
    'user_account_created_timestamp' : str(pulled_user_arr[1]),
    'user_first_name' : pulled_user_arr[2],
    'user_last_name' : pulled_user_arr[3],
    'user_full_name' : pulled_user_arr[4],
    'user_email' : pulled_user_arr[6],
    'slack_user_id' : pulled_user_arr[7],
    'slack_team_id' : pulled_user_arr[8],
    'slack_team_name' : pulled_user_arr[9],
    'slack_channel_id' : pulled_user_arr[10],
    'slack_channel_name' : pulled_user_arr[11],
    'user_company_name' : pulled_user_arr[12],
    'slack_bot_user_id' : pulled_user_arr[13],
    'user_is_payment_admin' : pulled_user_arr[14],
    'slack_token_type' : pulled_user_arr[15],
    'slack_access_token' : pulled_user_arr[16],
    'slack_timezone' : pulled_user_arr[17],
    'slack_timezone_label' : pulled_user_arr[18],
    'slack_timezone_offset' : pulled_user_arr[19],
    'slack_user_job_title' : pulled_user_arr[20],
    'user_slack_email_permission_granted' : pulled_user_arr[21],
    'slack_authed_webhook_url' : pulled_user_arr[22],
    'user_slack_new_user_questionnaire_answered' : pulled_user_arr[23]
  }

  # Add free trial information
  user_dict = check_if_free_trial_period_is_expired_days_left_function(user_dict)

  # ------------------------ Check Server Running START ------------------------
  # -------------------------------------------------------------- Running on localhost
  server_env = os.environ.get('TESTING', 'false')
  # If running on localhost
  if server_env == 'true':
    # Connect to redis database pool (no need to close)
    redis_connection = redis_connect_to_database_function()

    # Get key:value from redis then delete row from redis
    localhost_redis_browser_cookie_key = 'localhost_redis_browser_cookie_key'
    get_cookie_value_from_browser = redis_connection.get(localhost_redis_browser_cookie_key).decode('utf-8')

  # -------------------------------------------------------------- NOT running on localhost
  # If running on production
  else:
    get_cookie_value_from_browser = request.cookies.get('triviafy_browser_cookie')
    pass
  # ------------------------ Check Server Running END ------------------------

  # Store in redis
  user_store_in_redis_status = user_store_loggedin_data_redis_function(user_dict, get_cookie_value_from_browser)
  
  
  localhost_print_function('=========================================== update_user_nested_dict_information_after_account_edit_function END ===========================================')
  return True
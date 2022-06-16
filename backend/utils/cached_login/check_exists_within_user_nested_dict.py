# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import json
from backend.page_templates_backend.slack_sign_in_with_slack_page_backend.slack_oauth_checking_database_for_user import slack_oauth_checking_database_for_user_function
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.utils.cached_login.check_cookie_browser import check_cookie_browser_function

# -------------------------------------------------------------- Main Function
def check_exists_within_user_nested_dict_function(user_nested_dict, user_nested_dict_item_to_search):
  localhost_print_function('=========================================== check_exists_within_user_nested_dict_function START ===========================================')

  user_slack_authed_id = user_nested_dict['user_slack_authed_id']
  # ------------------------ Check If Column Exists in Redis START ------------------------
  try:
    requested_end_value = user_nested_dict[f'{user_nested_dict_item_to_search}']
  except:
    # ------------------------ Pull from dict before db pull START ------------------------
    free_trial_period_is_expired = user_nested_dict['free_trial_period_is_expired']
    trial_period_days_left_int = user_nested_dict['trial_period_days_left_int']
    free_trial_end_date = user_nested_dict['free_trial_end_date']
    # ------------------------ Pull from dict before db pull END ------------------------
    authed_user_id_already_exists, user_nested_dict = slack_oauth_checking_database_for_user_function(user_slack_authed_id)
    
    # ------------------------ Add to dict from earlier pull START ------------------------
    user_nested_dict['free_trial_period_is_expired'] = free_trial_period_is_expired
    user_nested_dict['trial_period_days_left_int'] = trial_period_days_left_int
    user_nested_dict['free_trial_end_date'] = free_trial_end_date
    # ------------------------ Add to dict from earlier pull END ------------------------

    requested_end_value = user_nested_dict[f'{user_nested_dict_item_to_search}']
    # ------------------------ Check If Column Exists in Redis END ------------------------


    # ------------------------ Update Redis DB START ------------------------
    # Get cookie value from browser
    get_cookie_value_from_browser = check_cookie_browser_function()
    # Connect to redis database pool (no need to close)
    redis_connection = redis_connect_to_database_function()
    # Upload dictionary to redis based on cookies
    redis_connection.set(get_cookie_value_from_browser, json.dumps(user_nested_dict).encode('utf-8'))
    # ------------------------ Update Redis DB END ------------------------
  
  
  localhost_print_function('=========================================== check_exists_within_user_nested_dict_function END ===========================================')
  return user_nested_dict
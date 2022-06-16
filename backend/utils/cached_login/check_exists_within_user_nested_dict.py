# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import json
from backend.page_templates_backend.slack_sign_in_with_slack_page_backend.slack_oauth_checking_database_for_user import slack_oauth_checking_database_for_user_function

# -------------------------------------------------------------- Main Function
def check_exists_within_user_nested_dict_function(user_nested_dict, user_nested_dict_item_to_search):
  localhost_print_function('=========================================== check_exists_within_user_nested_dict_function START ===========================================')

  user_slack_authed_id = user_nested_dict['user_slack_authed_id']
  # ------------------------ Check If Column Exists in Redis START ------------------------
  try:
    requested_end_value = user_nested_dict[f'{user_nested_dict_item_to_search}']
  except:
    authed_user_id_already_exists, user_nested_dict = slack_oauth_checking_database_for_user_function(user_slack_authed_id)
    # ------------------------ Check If Column Exists in Redis END ------------------------
  
  localhost_print_function('=========================================== check_exists_within_user_nested_dict_function END ===========================================')
  return user_nested_dict
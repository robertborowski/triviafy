# -------------------------------------------------------------- Imports
from backend.utils.cached_login.check_if_user_login_through_cookies import check_if_user_login_through_cookies_function
from backend.utils.free_trial_period_utils.check_if_free_trial_period_is_expired_days_left import check_if_free_trial_period_is_expired_days_left_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.check_paid_latest_month_utils.check_if_user_team_channel_combo_paid_latest_month import check_if_user_team_channel_combo_paid_latest_month_function
from backend.utils.cached_login.check_exists_within_user_nested_dict import check_exists_within_user_nested_dict_function

# -------------------------------------------------------------- Main Function
def pre_load_page_checks_function(page_location_name):
  localhost_print_function('=========================================== pre_load_page_checks_function Page START ===========================================')

  try:
    # ------------------------ Page Pre Load Check - User Logged In Through Cookies START ------------------------
    # Check if user logged in through cookies
    user_nested_dict = check_if_user_login_through_cookies_function()
    # ------------------------ Page Pre Load Check - User Logged In Through Cookies END ------------------------


    # ------------------------ Pages To Exclude From Checks START ------------------------
    # page_check_skip_step_subscription_arr = ['/employees/admin', '/employees/subscription']
    page_check_skip_step_subscription_arr = [
      '/employees/admin',
      '/employees/admin/leaderboard',
      '/employees/subscription',
      '/notifications/email/permission',
      '/notifications/email/permission/processing',
      '/new/user/questionnaire',
      '/new/user/questionnaire/processing',
      '/categories/edit',
      '/categories/edit/processing'
    ]
    page_check_skip_step_permission_arr = [
      '/notifications/email/permission',
      '/notifications/email/permission/processing'
    ]
    page_check_skip_step_questionnaire_arr = [
      '/notifications/email/permission',
      '/notifications/email/permission/processing',
      '/new/user/questionnaire',
      '/new/user/questionnaire/processing'
    ]
    page_check_skip_step_categories_selected_arr = [
      '/notifications/email/permission',
      '/notifications/email/permission/processing',
      '/new/user/questionnaire',
      '/new/user/questionnaire/processing',
      '/categories/edit',
      '/categories/edit/processing'
    ]
    # ------------------------ Pages To Exclude From Checks END ------------------------
    

    # ------------------------ Page Pre Load Check - Redirect Check - Free Trial / Latest Month Paid START ------------------------
    if page_location_name not in page_check_skip_step_subscription_arr:
      # Check if user Team/Channel combo paid the latest month
      user_team_channeL_paid_latest_month = check_if_user_team_channel_combo_paid_latest_month_function(user_nested_dict)

      # If user's company did not pay latest month
      if user_team_channeL_paid_latest_month == False:
        # Check if user free trial is expired
        user_nested_dict = check_if_free_trial_period_is_expired_days_left_function(user_nested_dict)
        if user_nested_dict == None or user_nested_dict == True:
          localhost_print_function('Error: Free Trial Over and User Subscription Not Paid')
          return '/employees/subscription', None

        days_left = str(user_nested_dict['trial_period_days_left_int'])
        if user_nested_dict['trial_period_days_left_int'] == 1:
          days_left = str(user_nested_dict['trial_period_days_left_int'])

        free_trial_ends_info = "Free Trial Days: " + days_left
      
      # If user's company did pay latest month
      if user_team_channeL_paid_latest_month == True:
        free_trial_ends_info = ''

    else:
      localhost_print_function('skipped subscription check for page {}'.format(page_location_name))
      free_trial_ends_info = ''
      pass
    # ------------------------ Page Pre Load Check - Redirect Check - Free Trial / Latest Month Paid END ------------------------


    # ------------------------ Page Pre Load Check - Redirect Check - Permission Granted START ------------------------
    if page_location_name not in page_check_skip_step_permission_arr:
      # Does this item exist in nested dict, if not create new nested dict in redis
      user_nested_dict = check_exists_within_user_nested_dict_function(user_nested_dict, 'user_slack_email_permission_granted')
      user_slack_email_permission_granted = user_nested_dict['user_slack_email_permission_granted']
      if user_slack_email_permission_granted == False or user_slack_email_permission_granted == 'False':
        localhost_print_function('Error: User Email Permission Not Granted')
        return '/notifications/email/permission', None
    else:
      localhost_print_function('skipped email permission check for page {}'.format(page_location_name))
      pass
    # ------------------------ Page Pre Load Check - Redirect Check - Permission Granted END ------------------------


    # ------------------------ Page Pre Load Check - Redirect Check - New User Questionnaire Answered START ------------------------
    if page_location_name not in page_check_skip_step_questionnaire_arr:
      # Does this item exist in nested dict, if not create new nested dict in redis
      user_nested_dict = check_exists_within_user_nested_dict_function(user_nested_dict, 'user_slack_new_user_questionnaire_answered')
      user_slack_new_user_questionnaire_answered = user_nested_dict['user_slack_new_user_questionnaire_answered']
      if user_slack_new_user_questionnaire_answered == False or user_slack_new_user_questionnaire_answered == 'False':
        localhost_print_function('Error: New User Questionnaire Not Answered')
        return '/new/user/questionnaire', None
    else:
      localhost_print_function('skipped user questionnaire check for page {}'.format(page_location_name))
      pass
    # ------------------------ Page Pre Load Check - Redirect Check - New User Questionnaire Answered END ------------------------


    # ------------------------ Page Pre Load Check - Redirect Check - Select Categories START ------------------------
    if page_location_name not in page_check_skip_step_categories_selected_arr:
      # Does this item exist in nested dict, if not create new nested dict in redis
      user_nested_dict = check_exists_within_user_nested_dict_function(user_nested_dict, 'user_slack_new_user_categories_selected')
      user_slack_new_user_categories_selected = user_nested_dict['user_slack_new_user_categories_selected']
      if user_slack_new_user_categories_selected == False or user_slack_new_user_categories_selected == 'False':
        localhost_print_function('Error: New User Categories Selected Not Answered')
        return '/categories/edit', None
    else:
      localhost_print_function('skipped user categories check for page {}'.format(page_location_name))
      pass
    # ------------------------ Page Pre Load Check - Redirect Check - Select Categories END ------------------------


  except:
    localhost_print_function('page load except error hit - pre_load_page_checks_function (non page)')
    localhost_print_function('=========================================== pre_load_page_checks_function Page END ===========================================')
    return '/logout', None


  localhost_print_function('=========================================== pre_load_page_checks_function Page END ===========================================')
  return user_nested_dict, free_trial_ends_info
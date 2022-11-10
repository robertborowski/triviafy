# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.utils.sanitize_user_inputs.sanitize_account_edit_settings_company_name import sanitize_account_edit_settings_company_name_function
from backend.utils.sanitize_user_inputs.sanitize_account_edit_settings_first_last_name import sanitize_account_edit_settings_first_last_name_function
from backend.db.queries.update_queries.update_queries_triviafy_user_login_information_table_slack.update_account_edit_settings_company_name import update_account_edit_settings_company_name_function
from backend.db.queries.update_queries.update_queries_triviafy_user_login_information_table_slack.update_account_edit_settings_first_name import update_account_edit_settings_first_name_function
from backend.db.queries.update_queries.update_queries_triviafy_user_login_information_table_slack.update_account_edit_settings_last_name import update_account_edit_settings_last_name_function
from backend.db.queries.update_queries.update_queries_triviafy_user_login_information_table_slack.update_account_edit_settings_full_name import update_account_edit_settings_full_name_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_company_user_uuids import select_triviafy_user_login_information_table_slack_all_company_user_uuids_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_payment_admins import select_triviafy_user_login_information_table_slack_all_payment_admins_function
from backend.db.queries.update_queries.update_queries_triviafy_user_login_information_table_slack.update_account_edit_settings_company_payment_admins import update_account_edit_settings_company_payment_admins_function
from backend.db.queries.update_queries.update_queries_triviafy_user_login_information_table_slack.update_account_edit_settings_company_non_payment_admin import update_account_edit_settings_company_non_payment_admin_function
from backend.utils.cached_login.update_user_nested_dict_information_after_account_edit import update_user_nested_dict_information_after_account_edit_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
account_edit_settings_processing_changes_page_render_template = Blueprint("account_edit_settings_processing_changes_page_render_template", __name__, static_folder="static", template_folder="templates")
@account_edit_settings_processing_changes_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@account_edit_settings_processing_changes_page_render_template.route("/employees/account/edit/settings/processing", methods=['GET','POST'])
def account_edit_settings_processing_changes_page_render_template_function():
  localhost_print_function('=========================================== /account/edit/settings/processing Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------

  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/account/edit/settings/processing')
    # Redirects based on returned value - pre load checks
    if user_nested_dict == '/subscription':
      return redirect('/subscription', code=302)
    elif user_nested_dict == '/notifications/email/permission':
      return redirect('/notifications/email/permission', code=302)
    elif user_nested_dict == '/new/user/questionnaire':
      return redirect('/new/user/questionnaire', code=302)
    elif user_nested_dict == '/categories/edit':
      return redirect('/categories/edit', code=302)
    elif user_nested_dict == '/logout':
      return redirect('/employees/logout', code=302)
    # ------------------------ Pre Load Page Checks END ------------------------

    
    # ------------------------ Page Company Info START ------------------------
    user_company_name = user_nested_dict['user_company_name']
    user_company_name = sanitize_page_output_company_name_function(user_company_name)
    user_channel_name = user_nested_dict['user_slack_channel_name']
    # ------------------------ Page Company Info END ------------------------
    

    # Get additional variables
    user_first_name = user_nested_dict['user_first_name']
    user_last_name = user_nested_dict['user_last_name']
    slack_workspace_team_id = user_nested_dict['user_slack_workspace_team_id']
    slack_channel_id = user_nested_dict['user_slack_channel_id']
    user_uuid = user_nested_dict['user_uuid']
    user_is_payment_admin = user_nested_dict['user_is_payment_admin_teamid_channelid']


    # ------------------------ Set Variables Pre Checks START ------------------------
    account_settings_company_name_changed = False
    account_settings_first_name_changed = False
    account_settings_last_name_changed = False
    # ------------------------ Set Variables Pre Checks END ------------------------


    # ------------------------ Sanitize/Update Company Name Input START ------------------------
    if user_is_payment_admin == True:
      user_input_quiz_settings_edit_company_name = request.form.get('user_input_account_settings_company_name')
      if user_input_quiz_settings_edit_company_name == user_company_name:
        localhost_print_function('company name did not change')
        pass
      else:
        account_settings_company_name_changed = True
        user_input_quiz_settings_edit_company_name = sanitize_account_edit_settings_company_name_function(request.form.get('user_input_account_settings_company_name'))
        if user_input_quiz_settings_edit_company_name != None:
          # Connect to Postgres database
          postgres_connection, postgres_cursor = postgres_connect_to_database_function()

          # Update the company name
          output_message = update_account_edit_settings_company_name_function(postgres_connection, postgres_cursor, user_input_quiz_settings_edit_company_name, slack_workspace_team_id, slack_channel_id)

          # Close postgres db connection
          postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Sanitize/Update Company Name Input END ------------------------


    # ------------------------ Sanitize/Update User First Name Input START ------------------------
    user_input_quiz_settings_edit_first_name = request.form.get('user_input_account_settings_first_name')
    if user_input_quiz_settings_edit_first_name == user_first_name:
      localhost_print_function('user first name did not change')
      pass
    else:
      account_settings_first_name_changed = True
      user_input_quiz_settings_edit_first_name = sanitize_account_edit_settings_first_last_name_function(user_input_quiz_settings_edit_first_name)
      if user_input_quiz_settings_edit_first_name != None:
        # Connect to Postgres database
        postgres_connection, postgres_cursor = postgres_connect_to_database_function()

        # Update the company name
        output_message = update_account_edit_settings_first_name_function(postgres_connection, postgres_cursor, user_input_quiz_settings_edit_first_name, user_uuid)

        # Close postgres db connection
        postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Sanitize/Update User First Name Input END ------------------------


    # ------------------------ Sanitize/Update User Last Name Input START ------------------------
    user_input_quiz_settings_edit_last_name = request.form.get('user_input_account_settings_last_name')
    if user_input_quiz_settings_edit_last_name == user_last_name:
      localhost_print_function('user last name did not change')
      pass
    else:
      account_settings_last_name_changed = True
      user_input_quiz_settings_edit_last_name = sanitize_account_edit_settings_first_last_name_function(user_input_quiz_settings_edit_last_name)
      if user_input_quiz_settings_edit_last_name != None:
        # Connect to Postgres database
        postgres_connection, postgres_cursor = postgres_connect_to_database_function()

        # Update the company name
        output_message = update_account_edit_settings_last_name_function(postgres_connection, postgres_cursor, user_input_quiz_settings_edit_last_name, user_uuid)

        # Close postgres db connection
        postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Sanitize/Update User Last Name Input END ------------------------


    # ------------------------ Update User Full Name in DB START ------------------------
    if user_input_quiz_settings_edit_first_name == user_first_name and user_input_quiz_settings_edit_last_name == user_last_name:
      localhost_print_function('user first and last name did not change')
    else:
      user_input_quiz_settings_edit_full_name = user_input_quiz_settings_edit_first_name + '_' + user_input_quiz_settings_edit_last_name
      # Connect to Postgres database
      postgres_connection, postgres_cursor = postgres_connect_to_database_function()

      # Update the company name
      output_message = update_account_edit_settings_full_name_function(postgres_connection, postgres_cursor, user_input_quiz_settings_edit_full_name, user_uuid)

      # Close postgres db connection
      postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Update User Full Name in DB END ------------------------


    # ------------------------ Connect to DB START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()
    # Connect to redis database pool (no need to close)
    redis_connection = redis_connect_to_database_function()
    # ------------------------ Connect to DB END ------------------------
    

    # ------------------------ Update Payment Admins in DB START ------------------------
    if user_is_payment_admin == True:
      # Get all company user UUID's
      company_user_uuids_arr = select_triviafy_user_login_information_table_slack_all_company_user_uuids_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)
      
      for pulled_user_uuid_arr in company_user_uuids_arr:
        # Get real_uuid
        pulled_user_uuid = pulled_user_uuid_arr[0]
        # Get temp_uuid from redis
        temp_uuid_value_from_redis = redis_connection.get(pulled_user_uuid).decode('utf-8')
        
        # Check is temp_uuid is checked on in the html file
        try:
          # Get temp_uuid value from html
          temp_uuid_value_from_html = request.form.get(temp_uuid_value_from_redis)
          
          # If temp_uuid != None, means that user was selected on checkbox
          if temp_uuid_value_from_html != None:
            output_message = update_account_edit_settings_company_payment_admins_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id, pulled_user_uuid)
            localhost_print_function('User has been changed to payment admin')
            try:
              redis_connection.delete(pulled_user_uuid)
            except:
              pass

          # If temp_uuid == None, means that user was not selected on checkbox
          else:
            company_payment_admins_arr = select_triviafy_user_login_information_table_slack_all_payment_admins_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)
            # First check total user payment admins, has to be 2 or more in order to remove payment admin access
            if len(company_payment_admins_arr) >= 2:
              output_message = update_account_edit_settings_company_non_payment_admin_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id, pulled_user_uuid)
              localhost_print_function('User has been changed to NON payment admin')
              try:
                redis_connection.delete(pulled_user_uuid)
              except:
                pass
            else:
              localhost_print_function('There must always be at least 1 payment admin for a company')
              pass

        except:
          company_payment_admins_arr = select_triviafy_user_login_information_table_slack_all_payment_admins_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)
          localhost_print_function('total user payment admins within company')
          localhost_print_function(len(company_payment_admins_arr))
          # First check total user payment admins, has to be 2 or more in order to remove payment admin access
          if len(company_payment_admins_arr) >= 2:
            output_message = update_account_edit_settings_company_non_payment_admin_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id, pulled_user_uuid)
            localhost_print_function('User has been changed to NON payment admin')
            try:
              redis_connection.delete(pulled_user_uuid)
            except:
              pass
    else:
      localhost_print_function('user is not a payment admin and cannot make changes to current payment admin access')
      pass
    # ------------------------ Update Payment Admins in DB END ------------------------


    # ------------------------ Loop through and delete stored user uuids from Redis START ------------------------
    # Get all company user UUID's
    company_user_uuids_arr = select_triviafy_user_login_information_table_slack_all_company_user_uuids_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)
    
    for pulled_user_uuid_arr in company_user_uuids_arr:
      # Get real_uuid
      pulled_user_uuid = pulled_user_uuid_arr[0]
      try:
        redis_connection.delete(pulled_user_uuid)
      except:
        pass
    # ------------------------ Loop through and delete stored user uuids from Redis END ------------------------


    # ------------------------ Update user_nested_dict Associated With Redis Cookie START ------------------------
    if account_settings_company_name_changed == True or account_settings_first_name_changed == True or account_settings_last_name_changed == True:
      output_message = update_user_nested_dict_information_after_account_edit_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id, user_uuid)
    # ------------------------ Update user_nested_dict Associated With Redis Cookie END ------------------------


    # ------------------------ Close Connection to DB START ------------------------
    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Close Connection to DB END ------------------------


  except:
    localhost_print_function('page load except error hit - /account/edit/settings/processing Page')
    localhost_print_function('=========================================== /account/edit/settings/processing Page END ===========================================')
    return redirect('/employees/logout', code=302)
    # return redirect('/', code=302)
  
  localhost_print_function('=========================================== /account/edit/settings/processing Page END ===========================================')
  return redirect('/account', code=302)
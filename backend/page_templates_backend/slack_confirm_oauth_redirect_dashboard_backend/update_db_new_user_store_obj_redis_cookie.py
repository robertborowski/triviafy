# -------------------------------------------------------------- Imports
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_if_slack_user_combo_already_exists import select_if_slack_user_combo_already_exists_function
from backend.utils.slack.user_info_data_manipulation.guess_first_last_name import guess_first_last_name_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.db.queries.insert_queries.insert_queries_triviafy_user_login_information_table_slack.insert_triviafy_slack_user_login_information_table import insert_triviafy_user_login_information_table_slack_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_check_assign_payment_admin import select_check_assign_payment_admin_function
from backend.utils.slack.user_info_data_manipulation.transpose_slack_user_data_to_nested_dict import transpose_slack_user_data_to_nested_dict_function
from backend.utils.quiz_settings_page_utils.setup_company_default_quiz_settings import setup_company_default_quiz_settings_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_company_name_check import select_triviafy_user_login_information_table_company_name_check_function
from datetime import datetime
from backend.page_templates_backend.slack_confirm_oauth_redirect_dashboard_backend.update_insert_free_trial_info_team import update_insert_free_trial_info_team_function
from backend.page_templates_backend.slack_confirm_oauth_redirect_dashboard_backend.update_start_end_free_trial_info_whole_team import update_start_end_free_trial_info_whole_team_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os
from backend.utils.send_emails.send_email_template import send_email_template_function
from backend.db.queries.insert_queries.insert_queries_triviafy_emails_sent_table.insert_triviafy_emails_sent_table import insert_triviafy_emails_sent_table_function
from backend.page_templates_backend.slack_confirm_oauth_redirect_dashboard_backend.check_insert_default_categories_team_channel_combo import check_insert_default_categories_team_channel_combo_function

# -------------------------------------------------------------- Main Function
def update_db_new_user_store_obj_redis_cookie_function(client, authed_response_obj):
  localhost_print_function('=========================================== update_db_new_user_store_obj_redis_cookie_function START ===========================================')
  
  # Get bare minimum info to check if user already exists in database table
  user_slack_authed_id = authed_response_obj['authed_user']['id']
  user_slack_workspace_team_id = authed_response_obj['team']['id']
  user_slack_channel_id = authed_response_obj['incoming_webhook']['channel_id']
  user_slack_team_channel_incoming_webhook_url = authed_response_obj['incoming_webhook']['url']

  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # Check if user combo already exists in slack db table
  check_slack_user_combo_already_exists_arr = select_if_slack_user_combo_already_exists_function(postgres_connection, postgres_cursor, user_slack_authed_id, user_slack_workspace_team_id, user_slack_channel_id)

  
  # ------------------------ Account Does Not Exist START ------------------------
  if check_slack_user_combo_already_exists_arr == None:
    
    # ------------------------ Get User Basic Info START ------------------------
    # Get nessesary variables from the authed response Slack obj for database check/insert
    user_slack_workspace_team_name = authed_response_obj['team']['name']
    user_slack_channel_name = authed_response_obj['incoming_webhook']['channel']
    user_slack_bot_user_id = authed_response_obj['bot_user_id']
    user_slack_token_type = authed_response_obj['token_type']
    user_slack_access_token = authed_response_obj['access_token']

    try:
      # Authed user, get user information object, slack method
      user_information_obj = client.users_info(
        user = user_slack_authed_id,
        # - - - - -
        token=user_slack_access_token
        # - - - - -
      )
      # Get additional user information for the database check/insert
      slack_authed_user_name = user_information_obj['user']['name']
      user_display_name = user_information_obj['user']['real_name']
      user_email = user_information_obj['user']['profile']['email']
    except:
      slack_authed_user_name = 'unavailable'
      user_display_name = 'unavailable'
      user_email = 'unavailable'
    
    try:
      # From the slack full name provided try to guess the first last name
      user_first_name, user_last_name = guess_first_last_name_function(user_display_name, slack_authed_user_name)
    except:
      user_first_name = 'unavailable'
      user_last_name = 'unavailable'
    
    try:
      user_slack_timezone = user_information_obj['user']['tz']
      user_slack_timezone_label = user_information_obj['user']['tz_label']
      user_slack_timezone_offset = user_information_obj['user']['tz_offset']
    except:
      user_slack_timezone = 'unavailable'
      user_slack_timezone_label = 'unavailable'
      user_slack_timezone_offset = -14400
    
    try:
      user_slack_job_title = user_information_obj['user']['profile']['title']
    except:
      user_slack_job_title = 'unavailable'
    
    user_slack_email_permission_granted = False
    user_slack_new_user_questionnaire_answered = False
    user_slack_new_user_categories_selected = False
    # ------------------------ Get User Basic Info END ------------------------


    # ------------------------ Once New User Created START ------------------------
    # If this is the first user on this team_id + channel_id combination then they will be asigned role of payment_admin (payment manager) but this can changed within website once logged in
    user_is_payment_admin_teamid_channelid = False
    check_if_team_id_channel_id_combo_contains_payment_admin = select_check_assign_payment_admin_function(postgres_connection, postgres_cursor, user_slack_workspace_team_id, user_slack_channel_id)
    if check_if_team_id_channel_id_combo_contains_payment_admin == None:
      
      # ------------------------ Make Person Payment Admin START ------------------------
      user_is_payment_admin_teamid_channelid = True
      # ------------------------ Make Person Payment Admin END ------------------------
      
      # ------------------------ Create Default Quiz Settings for new Slack team/channel ID-combo START ------------------------
      new_quiz_settings_row_created = setup_company_default_quiz_settings_function(user_slack_workspace_team_id, user_slack_channel_id)
      localhost_print_function(new_quiz_settings_row_created)
      # ------------------------ Create Default Quiz Settings for new Slack team/channel ID-combo END ------------------------
    # ------------------------ Once New User Created END ------------------------


    # Create uuid and timestamp for insert
    user_uuid = create_uuid_function('user-slack_')
    user_datetime_account_created = create_timestamp_function()


    # ------------------------ Free Trial Period Tracker START ------------------------
    output_message = update_insert_free_trial_info_team_function(postgres_connection, postgres_cursor, user_slack_authed_id, user_slack_workspace_team_id, user_slack_channel_id, user_uuid)
    # ------------------------ Free Trial Period Tracker END ------------------------

    # ------------------------ Set Default Categories START ------------------------
    output_message = check_insert_default_categories_team_channel_combo_function(postgres_connection, postgres_cursor, user_slack_workspace_team_id, user_slack_channel_id)
    # ------------------------ Set Default Categories END ------------------------


    # ------------------------ Insert New User to DB START ------------------------
    db_insert_output_message = insert_triviafy_user_login_information_table_slack_function(postgres_connection, postgres_cursor, user_uuid, user_datetime_account_created, user_first_name, user_last_name, user_display_name, user_email, user_slack_authed_id, user_slack_workspace_team_id, user_slack_workspace_team_name, user_slack_channel_id, user_slack_channel_name, user_slack_bot_user_id, user_is_payment_admin_teamid_channelid, user_slack_token_type, user_slack_access_token, user_slack_timezone, user_slack_timezone_label, user_slack_timezone_offset, user_slack_job_title, user_slack_email_permission_granted, user_slack_team_channel_incoming_webhook_url, user_slack_new_user_questionnaire_answered, user_slack_new_user_categories_selected)
    # ------------------------ Insert New User to DB END ------------------------


    # ------------------------ Email Self About New Account START ------------------------
    personal_email = os.environ.get('PERSONAL_EMAIL')
    if user_email != personal_email:
      output_email = personal_email
      output_subject_line = 'Someone Created A Triviafy Account'
      output_message_content = f"Hi,\n\n{user_email} CREATED AN ACCOUNT with Triviafy.\n\nTeam name: {user_slack_workspace_team_name}\nChannel name: {user_slack_channel_name}"
      output_message_content_str_for_db = output_message_content

      email_sent_successfully = send_email_template_function(output_email, output_subject_line, output_message_content)

      # Insert this sent email into DB
      uuid_email_sent = create_uuid_function('email_sent_')
      email_sent_timestamp = create_timestamp_function()
      # - - -
      email_sent_search_category = 'Notify Me Someone Created Account'
      uuid_quiz = None
      # - - -
      output_message = insert_triviafy_emails_sent_table_function(postgres_connection, postgres_cursor, uuid_email_sent, email_sent_timestamp, user_uuid, email_sent_search_category, uuid_quiz, output_message_content_str_for_db)
    # ------------------------ Email Self About New Account END ------------------------


    # ------------------------ Free Trial Period Tracker Update START ------------------------
    output_message = update_start_end_free_trial_info_whole_team_function(postgres_connection, postgres_cursor, user_slack_workspace_team_id, user_slack_channel_id)
    # ------------------------ Free Trial Period Tracker Update END ------------------------


    # ------------------------ Use Company Name of Already Existing Users (If Changed) START ------------------------
    try:
      company_name_arr = select_triviafy_user_login_information_table_company_name_check_function(postgres_connection, postgres_cursor, user_slack_workspace_team_id, user_slack_channel_id, user_uuid)
      if company_name_arr == None:
        user_company_name = user_slack_workspace_team_name
      else:
        user_company_name = company_name_arr[0]
    except:
      # Transpose user data to nested dictionary
      user_company_name = user_slack_workspace_team_name
    # ------------------------ Use Company Name of Already Existing Users (If Changed) END ------------------------


    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Account Does Not Exist END ------------------------  


  # ------------------------ Account Already Exist START ------------------------
  elif check_slack_user_combo_already_exists_arr != None:
    # Pull the user info from DB
    user_uuid = check_slack_user_combo_already_exists_arr[0]
    user_datetime_account_created = check_slack_user_combo_already_exists_arr[1]
    user_first_name = check_slack_user_combo_already_exists_arr[2]
    user_last_name = check_slack_user_combo_already_exists_arr[3]
    user_display_name = check_slack_user_combo_already_exists_arr[4]
    user_email = check_slack_user_combo_already_exists_arr[6]
    user_slack_authed_id = check_slack_user_combo_already_exists_arr[7]
    user_slack_workspace_team_id = check_slack_user_combo_already_exists_arr[8]
    user_slack_workspace_team_name = check_slack_user_combo_already_exists_arr[9]
    user_slack_channel_id = check_slack_user_combo_already_exists_arr[10]
    user_slack_channel_name = check_slack_user_combo_already_exists_arr[11]
    user_company_name = check_slack_user_combo_already_exists_arr[12]
    user_slack_bot_user_id = check_slack_user_combo_already_exists_arr[13]
    user_is_payment_admin_teamid_channelid = check_slack_user_combo_already_exists_arr[14]
    user_slack_token_type = check_slack_user_combo_already_exists_arr[15]
    user_slack_access_token = check_slack_user_combo_already_exists_arr[16]
    user_slack_timezone = check_slack_user_combo_already_exists_arr[17]
    user_slack_timezone_label = check_slack_user_combo_already_exists_arr[18]
    user_slack_timezone_offset = check_slack_user_combo_already_exists_arr[19]
    user_slack_job_title = check_slack_user_combo_already_exists_arr[20]
    user_slack_email_permission_granted = check_slack_user_combo_already_exists_arr[21]
    user_slack_team_channel_incoming_webhook_url = check_slack_user_combo_already_exists_arr[22]
    user_slack_new_user_questionnaire_answered = check_slack_user_combo_already_exists_arr[23]
    user_slack_new_user_categories_selected = check_slack_user_combo_already_exists_arr[24]
  # ------------------------ Account Already Exist END ------------------------


  # ------------------------ Transpose the SQL pulled table to dict START ------------------------
  # Transpose user data to nested dictionary. Make timestamp a string because you cannot upload timestamp to redis as a json obj
  user_nested_dict = transpose_slack_user_data_to_nested_dict_function(user_uuid, str(user_datetime_account_created), user_first_name, user_last_name, user_display_name, user_email, user_slack_authed_id, user_slack_workspace_team_id, user_slack_workspace_team_name, user_slack_channel_id, user_slack_channel_name, user_company_name, user_slack_bot_user_id, user_is_payment_admin_teamid_channelid,  user_slack_token_type, user_slack_access_token, user_slack_timezone, user_slack_timezone_label, user_slack_timezone_offset, user_slack_job_title, user_slack_email_permission_granted, user_slack_team_channel_incoming_webhook_url, user_slack_new_user_questionnaire_answered, user_slack_new_user_categories_selected)
  # ------------------------ Transpose the SQL pulled table to dict END ------------------------


  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)

  localhost_print_function('=========================================== update_db_new_user_store_obj_redis_cookie_function END ===========================================')
  return user_nested_dict
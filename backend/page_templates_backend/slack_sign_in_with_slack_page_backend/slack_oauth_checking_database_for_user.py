# -------------------------------------------------------------- Imports
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_if_slack_user_authed_id_exists import select_if_slack_user_authed_id_exists_function
from backend.utils.slack.user_info_data_manipulation.transpose_slack_user_data_to_nested_dict import transpose_slack_user_data_to_nested_dict_function

# -------------------------------------------------------------- Main Function
def slack_oauth_checking_database_for_user_function(response_authed_user_id):
  localhost_print_function('=========================================== slack_oauth_checking_database_for_user_function START ===========================================')


  """
  # Have to come back to this and put this check on every page not the one that you have to memorize to list out.
  # Pull all info for user uuid
  # ------------------------ Get Table Columns Info START ------------------------
  table_all_column_names_arr = select_all_column_names_function(postgres_connection, postgres_cursor)
  column_names_match_arr = []
  for i in table_all_column_names_arr:    
    column_names_match_arr.append(i[0])
  # ------------------------ Get Table Columns Info END ------------------------
  
  
  # ------------------------ Loop Match Up Info START ------------------------
  one_specific_user_tuple = select_one_user_uuid_function(postgres_connection, postgres_cursor, user_uuid)
  
  # Nested Dict
  nested_dict = {}
  for i in range(len(column_names_match_arr)):
    if column_names_match_arr[i] == 'user_datetime_account_created':
      nested_dict[column_names_match_arr[i]] = one_specific_user_tuple[i].strftime("%m/%d/%Y, %H:%M:%S")
    else: 
      nested_dict[column_names_match_arr[i]] = one_specific_user_tuple[i]

  nested_dict = json.dumps(nested_dict)#.encode('utf-8')
  # ------------------------ Loop Match Up Info END ------------------------
  """


  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()

  # Get user login info from db
  user_db_object = select_if_slack_user_authed_id_exists_function(postgres_connection, postgres_cursor, response_authed_user_id)

  # If user does not exist in db
  if user_db_object == None:
    authed_user_id_already_exists = False
    authed_user_id_signed_in_object = None
  # If user does exist in db
  else:
    # ------------------------ Account Already Exist START ------------------------
    user_uuid = user_db_object[0]
    user_datetime_account_created = user_db_object[1]
    user_first_name = user_db_object[2]
    user_last_name = user_db_object[3]
    user_display_name = user_db_object[4]
    user_email = user_db_object[6]
    user_slack_authed_id = user_db_object[7]
    user_slack_workspace_team_id = user_db_object[8]
    user_slack_workspace_team_name = user_db_object[9]
    user_slack_channel_id = user_db_object[10]
    user_slack_channel_name = user_db_object[11]
    user_company_name = user_db_object[12]
    user_slack_bot_user_id = user_db_object[13]
    user_is_payment_admin_teamid_channelid = user_db_object[14]
    user_slack_token_type = user_db_object[15]
    user_slack_access_token = user_db_object[16]
    user_slack_timezone = user_db_object[17]
    user_slack_timezone_label = user_db_object[18]
    user_slack_timezone_offset = user_db_object[19]
    user_slack_job_title = user_db_object[20]
    user_slack_email_permission_granted = user_db_object[21]
    user_slack_team_channel_incoming_webhook_url = user_db_object[22]
    user_slack_new_user_questionnaire_answered = user_db_object[23]
    user_slack_new_user_categories_selected = user_db_object[24]
    # ------------------------ Account Already Exist END ------------------------

    # ------------------------ Transpose the SQL pulled table to dict START ------------------------
    # Transpose user data to nested dictionary. Make timestamp a string because you cannot upload timestamp to redis as a json obj
    user_nested_dict = transpose_slack_user_data_to_nested_dict_function(user_uuid, str(user_datetime_account_created), user_first_name, user_last_name, user_display_name, user_email, user_slack_authed_id, user_slack_workspace_team_id, user_slack_workspace_team_name, user_slack_channel_id, user_slack_channel_name, user_company_name, user_slack_bot_user_id, user_is_payment_admin_teamid_channelid,  user_slack_token_type, user_slack_access_token, user_slack_timezone, user_slack_timezone_label, user_slack_timezone_offset, user_slack_job_title, user_slack_email_permission_granted, user_slack_team_channel_incoming_webhook_url, user_slack_new_user_questionnaire_answered, user_slack_new_user_categories_selected)
    # ------------------------ Transpose the SQL pulled table to dict END ------------------------

    authed_user_id_already_exists = True
    authed_user_id_signed_in_object = user_nested_dict


  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)

  localhost_print_function('=========================================== slack_oauth_checking_database_for_user_function END ===========================================')
  return authed_user_id_already_exists, authed_user_id_signed_in_object
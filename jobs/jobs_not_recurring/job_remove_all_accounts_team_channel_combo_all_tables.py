# -------------------------------------------------------------- Imports
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_team_name_and_channel_name import select_team_name_and_channel_name_function
from backend.db.queries.select_queries.select_queries_all_tables.select_count_all_table_team_channel_combo_general import select_count_all_table_team_channel_combo_general_function
from backend.db.queries.delete_queries.delete_queries_all_tables.delete_query_all_team_channel_combo_general import delete_query_all_team_channel_combo_general_function
from backend.db.queries.select_queries.select_queries_all_tables.select_count_all_table_team_channel_combo_special import select_count_all_table_team_channel_combo_special_function
from backend.db.queries.delete_queries.delete_queries_all_tables.delete_query_all_team_channel_combo_special import delete_query_all_team_channel_combo_special_function
import json
from backend.utils.job_utils.job_pre_delete_table_checks import job_pre_delete_table_checks_function

# -------------------------------------------------------------- Main Function
def job_remove_all_accounts_team_channel_combo_all_tables_function(arr_to_remove, arr_table_names_with_user_uuid_names, arr_table_names_with_team_id_channel_id_names):
  localhost_print_function('=========================================== job_remove_all_accounts_team_channel_combo_all_tables_function START ===========================================')

  # ------------------------ DB Conection START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ DB Conection End ------------------------

  for arr in arr_to_remove:
    localhost_print_function('- - - - - - - - - - - - - - - Team Channel Deletion Start - - - - - - - - - - - - - - - - - - ')
    team_id = arr[0]
    channel_id = arr[1]

    
    # ------------------------ Pre Delete Info Checks START ------------------------
    pre_delete_check = job_pre_delete_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id)
    if pre_delete_check == False:
      return True
    # ------------------------ Pre Delete Info Checks END ------------------------


    # ------------------------ Redis Delete START ------------------------
    # Connect to redis database pool (no need to close)
    redis_connection = redis_connect_to_database_function()
    redis_keys = redis_connection.keys()

    for key in redis_keys:
      if 'user-slack_' in str(key) or 'aa_foo' in str(key) or 'localhost_' in str(key):
        localhost_print_function('skipping key: {}'.format(key))
        continue
      else:
        value = redis_connection.get(key).decode('utf-8')
        user_nested_dict = json.loads(value)
        redis_slack_team_id = user_nested_dict['user_slack_workspace_team_id']
        redis_slack_channel_id = user_nested_dict['user_slack_channel_id']
        redis_user_email = user_nested_dict['user_email']
        if redis_slack_team_id == team_id and redis_slack_channel_id == channel_id:
          redis_connection.delete(key)
          localhost_print_function('deleted logged in user from Redis. Email: {}'.format(redis_user_email))
    # ------------------------ Redis Delete END ------------------------


    # ------------------------ State Team Channel Names START ------------------------
    try:
      team_channel_name_arr = select_team_name_and_channel_name_function(postgres_connection, postgres_cursor, team_id, channel_id)
      team_name = team_channel_name_arr[0]
      channel_name = team_channel_name_arr[1]
      localhost_print_function('Team name: {}\nChannel name: {}'.format(team_name, channel_name))
    except:
      localhost_print_function('Team name: not found on login\nChannel name: not found on login')
      localhost_print_function('- - - - - - - - - - - - - - - Team Channel Deletion End - - - - - - - - - - - - - - - - - - ')
      continue
    # ------------------------ State Team Channel Names END ------------------------


    # ------------------------ Special Deletion From Table START ------------------------
    for table_arr in arr_table_names_with_user_uuid_names:
      table_name = table_arr[0]
      table_user_uuid_fk_column_name = table_arr[1]
      
      try:
        select_count_arr = select_count_all_table_team_channel_combo_special_function(postgres_connection, postgres_cursor, team_id, channel_id, table_name, table_user_uuid_fk_column_name)
        select_count_int = select_count_arr[0]
        if select_count_int == 0:
          localhost_print_function('No rows to remove from {}'.format(table_name))

        if select_count_int > 0:
          output_message = delete_query_all_team_channel_combo_special_function(postgres_connection, postgres_cursor, team_id, channel_id, table_name, table_user_uuid_fk_column_name)
          localhost_print_function('{} row(s) deleted from {}'.format(select_count_int, table_name))
      except:
          localhost_print_function('Error, skiped {}'.format(table_name))
    # ------------------------ Special Deletion From Table END ------------------------


    # ------------------------ General Deletion From Table START ------------------------
    for table_arr in arr_table_names_with_team_id_channel_id_names:
      table_name = table_arr[0]
      table_team_id_column_name = table_arr[1]
      table_channel_id_column_name = table_arr[2]
      
      try:
        select_count_arr = select_count_all_table_team_channel_combo_general_function(postgres_connection, postgres_cursor, team_id, channel_id, table_name, table_team_id_column_name, table_channel_id_column_name)
        select_count_int = select_count_arr[0]
        if select_count_int == 0:
          localhost_print_function('No rows to remove from {}'.format(table_name))

        if select_count_int > 0:
          output_message = delete_query_all_team_channel_combo_general_function(postgres_connection, postgres_cursor, team_id, channel_id, table_name, table_team_id_column_name, table_channel_id_column_name)
          localhost_print_function('{} row(s) deleted from {}'.format(select_count_int, table_name))
      except:
          localhost_print_function('Error, skiped {}'.format(table_name))
    # ------------------------ General Deletion From Table END ------------------------

    
    localhost_print_function('- - - - - - - - - - - - - - - Team Channel Deletion End - - - - - - - - - - - - - - - - - - ')


  # ------------------------ DB Close Conection START ------------------------
  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ DB Close Conection END ------------------------

  localhost_print_function('=========================================== job_remove_all_accounts_team_channel_combo_all_tables_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  arr_to_remove = [
    # [SlackTeamID, SlackChannelID]
    ['abc','xyz']
  ]

  arr_table_names_with_user_uuid_names = [
    # [table_name, user_uuid_column_name]
    ['triviafy_quiz_feedback_responses_table', 'quiz_feedback_user_uuid'],
    ['triviafy_quiz_winners_table', 'quiz_winner_user_uuid_fk'],
    ['triviafy_send_prize_to_email_table', 'send_prize_to_user_uuid_fk'],
    ['triviafy_waitlist_create_question_table', 'waitlist_user_uuid_signed_up']
  ]

  arr_table_names_with_team_id_channel_id_names = [
    # [table_name, table_team_id_column_name, table_channel_id_column_name]
    ['triviafy_categories_selected_table', 'categories_team_id_fk', 'categories_channel_id_fk'],
    ['triviafy_company_quiz_settings_slack_table', 'company_quiz_settings_slack_workspace_team_id', 'company_quiz_settings_slack_channel_id'],
    ['triviafy_free_trial_tracker_slack_table', 'free_trial_user_slack_workspace_team_id_fk', 'free_trial_user_slack_channel_id_fk'],
    ['triviafy_new_user_questionnaire_response_table', 'questionnaire_user_slack_team_id_fk', 'questionnaire_user_slack_channel_id_fk'],
    ['triviafy_quiz_answers_master_table', 'quiz_answer_slack_team_id', 'quiz_answer_slack_channel_id'],
    ['triviafy_quiz_master_table', 'quiz_slack_team_id', 'quiz_slack_channel_id'],
    ['triviafy_quiz_questions_asked_to_company_slack_table', 'quiz_question_asked_tracking_slack_team_id', 'quiz_question_asked_tracking_slack_channel_id'],
    ['triviafy_skipped_quiz_count_slack_team_channel_table', 'skipped_quiz_slack_team_id', 'skipped_quiz_slack_channel_id'],
    ['triviafy_slack_payment_status_table', 'payment_status_slack_team_id', 'payment_status_slack_channel_id'],
    ['triviafy_user_login_information_table_slack', 'user_slack_workspace_team_id', 'user_slack_channel_id']
  ]

  job_remove_all_accounts_team_channel_combo_all_tables_function(arr_to_remove, arr_table_names_with_user_uuid_names, arr_table_names_with_team_id_channel_id_names)
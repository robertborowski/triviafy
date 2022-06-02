# -------------------------------------------------------------- Imports
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.db.queries.select_queries.select_queries_all_tables.select_count_all_table_team_channel_combo_special_by_user_uuid import select_count_all_table_team_channel_combo_special_by_user_uuid_function
from backend.db.queries.delete_queries.delete_queries_all_tables.delete_query_all_team_channel_combo_special_by_user_uuid import delete_query_all_team_channel_combo_special_by_user_uuid_function
import json
from backend.utils.job_utils.job_pre_delete_table_checks_user_specific import job_pre_delete_table_checks_user_specific_function

# -------------------------------------------------------------- Main Function
def job_remove_all_accounts_user_specific_all_tables_function(arr_to_remove, arr_table_names_with_user_uuid_names):
  localhost_print_function('=========================================== job_remove_all_accounts_user_specific_all_tables_function START ===========================================')

  # ------------------------ DB Conection START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ DB Conection End ------------------------

  for user_uuid in arr_to_remove:
    localhost_print_function('- - - - - - - - - - - - - - - Team Channel Deletion Start - - - - - - - - - - - - - - - - - - ')

    
    # ------------------------ Pre Delete Info Checks START ------------------------
    pre_delete_check = job_pre_delete_table_checks_user_specific_function(postgres_connection, postgres_cursor, user_uuid)
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
        redis_user_email = user_nested_dict['user_email']
        redis_user_uuid = user_nested_dict['user_uuid']
        if redis_user_uuid == user_uuid:
          redis_connection.delete(key)
          localhost_print_function('deleted logged in user from Redis. Email: {}'.format(redis_user_email))
    # ------------------------ Redis Delete END ------------------------


    # ------------------------ Special Deletion From Table START ------------------------
    for table_arr in arr_table_names_with_user_uuid_names:
      table_name = table_arr[0]
      table_user_uuid_fk_column_name = table_arr[1]
      
      try:
        select_count_arr = select_count_all_table_team_channel_combo_special_by_user_uuid_function(postgres_connection, postgres_cursor, user_uuid, table_name, table_user_uuid_fk_column_name)
        select_count_int = select_count_arr[0]
        if select_count_int == 0:
          localhost_print_function('No rows to remove from {}'.format(table_name))

        if select_count_int > 0:
          output_message = delete_query_all_team_channel_combo_special_by_user_uuid_function(postgres_connection, postgres_cursor, user_uuid, table_name, table_user_uuid_fk_column_name)
          localhost_print_function('{} row(s) deleted from {}'.format(select_count_int, table_name))
      except:
          localhost_print_function('Error, skiped {}'.format(table_name))
    # ------------------------ Special Deletion From Table END ------------------------

    
    localhost_print_function('- - - - - - - - - - - - - - - Team Channel Deletion End - - - - - - - - - - - - - - - - - - ')


  # ------------------------ DB Close Conection START ------------------------
  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ DB Close Conection END ------------------------

  localhost_print_function('=========================================== job_remove_all_accounts_user_specific_all_tables_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  arr_to_remove = [
    # 'user_uuid',
    'abc'
  ]

  arr_table_names_with_user_uuid_names = [
    # [table_name, user_uuid_column_name]
    ['triviafy_emails_sent_table', 'email_sent_to_user_uuid_fk'],
    ['triviafy_free_trial_tracker_slack_table', 'free_trial_user_uuid_fk'],
    ['triviafy_new_user_questionnaire_response_table', 'questionnaire_user_slack_uuid_fk'],
    ['triviafy_quiz_answers_master_table', 'quiz_answer_user_uuid_fk'],
    ['triviafy_quiz_feedback_responses_table', 'quiz_feedback_user_uuid'],
    ['triviafy_quiz_winners_table', 'quiz_winner_user_uuid_fk'],
    ['triviafy_send_prize_to_email_table', 'send_prize_to_user_uuid_fk'],
    ['triviafy_slack_messages_sent_table', 'slack_message_sent_to_user_uuid_fk'],
    ['triviafy_user_login_information_table_slack', 'user_uuid'],
    ['triviafy_waitlist_create_question_table', 'waitlist_user_uuid_signed_up']
  ]

  job_remove_all_accounts_user_specific_all_tables_function(arr_to_remove, arr_table_names_with_user_uuid_names)
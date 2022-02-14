# -------------------------------------------------------------- Imports
import json
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import pandas as pd
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.drop_queries.drop_query_table_summary_triviafy_db_status_overall import drop_query_table_summary_triviafy_db_status_overall_function
from backend.db.queries.create_queries.create_query_table_summary_triviafy_db_status_overall import create_query_table_summary_triviafy_db_status_overall_function
from backend.db.queries.insert_queries.insert_queries_summary_triviafy_db_status_overall_table.insert_summary_triviafy_db_status_overall_table import insert_summary_triviafy_db_status_overall_table_function

# -------------------------------------------------------------- Main Function
def job_check_db_status_overall_part_2_redis_to_pandas_df_function():
  localhost_print_function('=========================================== job_check_db_status_overall_part_2_redis_to_pandas_df_function START ===========================================')


  # ------------------------ Upload To Redis START ------------------------
  # Connect to redis database pool (no need to close)
  redis_connection = redis_connect_to_database_function()

  localhost_db_check_dict = 'localhost_db_check_dict'
  value = redis_connection.get(localhost_db_check_dict).decode('utf-8')
  db_check_dict = json.loads(value)
  # ------------------------ Upload To Redis END ------------------------


  # ------------------------ Loop Through Nested Dict START ------------------------
  # Arr initialization
  rows_arr = []
  column_names_row = ['team_id', 'channel_id']

  # Loop through nested dict creating row by row
  for k_team_id, v_inner_dict in db_check_dict.items():
    row = []
    row.append(k_team_id)
    for k_channel_id, v_inner_dict2 in v_inner_dict.items():
      row.append(k_channel_id)
      for k_column_name, v_column_value in v_inner_dict2.items():
        if k_column_name not in column_names_row:
          column_names_row.append(k_column_name)
        row.append(v_column_value)
        # print(f'{k_team_id} | {k_channel_id} | {k_column_name} | {v_column_value}')
      rows_arr.append(row)
    # print('- - - - - - - - - - - - -')

  # Create the pandas DataFrame
  df = pd.DataFrame(rows_arr, columns = column_names_row)
  
  # ------------------------ Excel View START ------------------------
  # Create desktop Excel file
  # df.to_excel(r'/Users/robert/desktop/test.xlsx', index = True)
  # ------------------------ Excel View END ------------------------
  # ------------------------ Loop Through Nested Dict END ------------------------


  # ------------------------ DB Conection START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ DB Conection End ------------------------


  # ------------------------ Drop Existing DB Table START ------------------------
  try:
    drop_query_table_summary_triviafy_db_status_overall_function(postgres_connection, postgres_cursor)
    localhost_print_function('Dropped Table')
  except:
    localhost_print_function('Error: No table to drop')
    pass
  # ------------------------ Drop Existing DB Table END ------------------------


  # ------------------------ Create Summary Table START ------------------------
  try:
    create_query_table_summary_triviafy_db_status_overall_function(postgres_connection, postgres_cursor)
    localhost_print_function('Table Created')
  except:
    localhost_print_function('Error: Table already exists')
  # ------------------------ Create Summary Table END ------------------------


  pk_value = 0
  for index, row in df.iterrows():
    pk_index = pk_value
    team_id = row[0]
    channel_id = row[1]
    team_name = row[2]
    channel_name = row[3]
    total_team_channel_users = row[4]
    free_trial_total_users_count_match = row[5]
    free_trial_auth_id_and_uuid_no_duplicates = row[6]
    free_trial_expired = row[7]
    free_trial_days_left = row[8]
    latest_sub_month_status_exists = row[9]
    latest_sub_month_paid_status = row[10]
    categories_selected_str = row[11]
    quiz_settings_start_day_of_week = row[12]
    quiz_settings_start_time_of_day = row[13]
    quiz_settings_end_day_of_week = row[14]
    quiz_settings_end_time_of_day = row[15]
    quiz_settings_questions_per_quiz = row[16]
    latest_quiz_should_be_open_check = row[17]
    latest_quiz_should_be_closed_check = row[18]
    quiz_created_this_week = row[19]
    quiz_master_latest_quiz_uuid = row[20]
    latest_quiz_timestamp_created = row[21]
    latest_quiz_start_date = row[22]
    latest_quiz_start_day_of_week = row[23]
    latest_quiz_start_time = row[24]
    latest_quiz_end_date = row[25]
    latest_quiz_end_day_of_week = row[26]
    latest_quiz_end_time = row[27]
    latest_quiz_num_questions = row[28]
    latest_quiz_count = row[29]
    user_quiz_settings_start_day_of_week_unchanged = row[30]
    user_quiz_settings_start_time_unchanged = row[31]
    user_quiz_settings_end_day_of_week_unchanged = row[32]
    user_quiz_settings_end_time_unchanged = row[33]
    user_quiz_settings_num_questions_unchanged = row[34]
    remaining_unasked_num_questions_all_categories = row[35]
    remaining_unasked_num_questions_all_categories_below_threshold = row[36]
    remaining_unasked_num_questions_category_specific = row[37]
    remaining_unasked_questions_category_below_threshold = row[38]
    all_team_channel_users_received_email_account_created = row[39]
    email_sent_count_all_users_received_quiz_open = row[40]
    email_sent_count_all_users_received_quiz_closed = row[41]
    slack_message_sent_team_channel_received_quiz_open = row[42]
    slack_message_sent_received_quiz_pre_close_reminder = row[43]
    slack_message_sent_team_channel_received_quiz_closed = row[44]
    total_team_channel_users_answered_new_user_questionnaire = row[45]
    percent_team_channel_users_answered_new_user_questionnaire = row[46]
    total_team_channel_users_answered_quiz_questions = row[47]
    percent_team_channel_users_answered_quiz_questions = row[48]
    percent_team_channel_users_answered_quiz_correct_answers = row[49]
    quiz_winner_this_week_email = row[50]
    quiz_winner_this_week_email_cumulative_win_total = row[51]
    min_account_created_date = row[52]
    total_weeks_active = row[53]
    team_channel_skipped_quiz_count = row[54]
    payment_admins_arr = row[55]
    payment_admins_arr_len = row[56]
    try:
      insert_summary_triviafy_db_status_overall_table_function(postgres_connection, postgres_cursor, pk_index, team_id,channel_id,team_name,channel_name,total_team_channel_users,free_trial_total_users_count_match,free_trial_auth_id_and_uuid_no_duplicates,free_trial_expired,free_trial_days_left,latest_sub_month_status_exists,latest_sub_month_paid_status,categories_selected_str,quiz_settings_start_day_of_week,quiz_settings_start_time_of_day,quiz_settings_end_day_of_week,quiz_settings_end_time_of_day,quiz_settings_questions_per_quiz,latest_quiz_should_be_open_check,latest_quiz_should_be_closed_check,quiz_created_this_week,quiz_master_latest_quiz_uuid,latest_quiz_timestamp_created,latest_quiz_start_date,latest_quiz_start_day_of_week,latest_quiz_start_time,latest_quiz_end_date,latest_quiz_end_day_of_week,latest_quiz_end_time,latest_quiz_num_questions,latest_quiz_count,user_quiz_settings_start_day_of_week_unchanged,user_quiz_settings_start_time_unchanged,user_quiz_settings_end_day_of_week_unchanged,user_quiz_settings_end_time_unchanged,user_quiz_settings_num_questions_unchanged,remaining_unasked_num_questions_all_categories,remaining_unasked_num_questions_all_categories_below_threshold,remaining_unasked_num_questions_category_specific,remaining_unasked_questions_category_below_threshold,all_team_channel_users_received_email_account_created,email_sent_count_all_users_received_quiz_open,email_sent_count_all_users_received_quiz_closed,slack_message_sent_team_channel_received_quiz_open,slack_message_sent_received_quiz_pre_close_reminder,slack_message_sent_team_channel_received_quiz_closed,total_team_channel_users_answered_new_user_questionnaire,percent_team_channel_users_answered_new_user_questionnaire,total_team_channel_users_answered_quiz_questions,percent_team_channel_users_answered_quiz_questions,percent_team_channel_users_answered_quiz_correct_answers,quiz_winner_this_week_email,quiz_winner_this_week_email_cumulative_win_total,min_account_created_date,total_weeks_active,team_channel_skipped_quiz_count,payment_admins_arr,payment_admins_arr_len)
      localhost_print_function('successfully inserted')
    except:
      localhost_print_function('UN-sucessfully inserted')
      return False
      pass
    pk_value += 1
    localhost_print_function('- - - - - - -')


  # ------------------------ DB Close Conection START ------------------------
  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ DB Close Conection END ------------------------



  localhost_print_function('=========================================== job_check_db_status_overall_part_2_redis_to_pandas_df_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  job_check_db_status_overall_part_2_redis_to_pandas_df_function()
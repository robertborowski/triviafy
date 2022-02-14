# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def create_query_table_summary_triviafy_db_status_overall_function(postgres_connection, postgres_cursor):
  localhost_print_function('=========================================== create_query_table_summary_triviafy_db_status_overall_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("CREATE TABLE summary_triviafy_db_status_overall(pk_index int4 PRIMARY KEY, team_id varchar,channel_id varchar,team_name varchar,channel_name varchar,total_team_channel_users int4,free_trial_total_users_count_match bool,free_trial_auth_id_and_uuid_no_duplicates bool,free_trial_expired bool,free_trial_days_left int4,latest_sub_month_status_exists bool,latest_sub_month_paid_status bool,categories_selected_str varchar,quiz_settings_start_day_of_week varchar,quiz_settings_start_time_of_day varchar,quiz_settings_end_day_of_week varchar,quiz_settings_end_time_of_day varchar,quiz_settings_questions_per_quiz int4,latest_quiz_should_be_open_check bool,latest_quiz_should_be_closed_check bool,quiz_created_this_week bool,quiz_master_latest_quiz_uuid varchar,latest_quiz_timestamp_created timestamp,latest_quiz_start_date timestamp,latest_quiz_start_day_of_week varchar,latest_quiz_start_time varchar,latest_quiz_end_date timestamp,latest_quiz_end_day_of_week varchar,latest_quiz_end_time varchar,latest_quiz_num_questions int4,latest_quiz_count int4,user_quiz_settings_start_day_of_week_unchanged bool,user_quiz_settings_start_time_unchanged bool,user_quiz_settings_end_day_of_week_unchanged bool,user_quiz_settings_end_time_unchanged bool,user_quiz_settings_num_questions_unchanged bool,remaining_unasked_num_questions_all_categories int4,remaining_unasked_num_questions_all_categories_below_threshold bool,remaining_unasked_num_questions_category_specific int4,remaining_unasked_questions_category_below_threshold bool,all_team_channel_users_received_email_account_created bool,email_sent_count_all_users_received_quiz_open bool,email_sent_count_all_users_received_quiz_closed bool,slack_message_sent_team_channel_received_quiz_open bool,slack_message_sent_received_quiz_pre_close_reminder bool,slack_message_sent_team_channel_received_quiz_closed bool,total_team_channel_users_answered_new_user_questionnaire int4,percent_team_channel_users_answered_new_user_questionnaire float4,total_team_channel_users_answered_quiz_questions int4,percent_team_channel_users_answered_quiz_questions float4,percent_team_channel_users_answered_quiz_correct_answers float4,quiz_winner_this_week_email varchar,quiz_winner_this_week_email_cumulative_win_total int4,min_account_created_date timestamp,total_weeks_active int4,team_channel_skipped_quiz_count int4,payment_admins_arr varchar,payment_admins_arr_len int4);")
    # ------------------------ Query END ------------------------\


    # ------------------------ Query Result START ------------------------
    postgres_connection.commit()
    localhost_print_function('=========================================== create_query_table_summary_triviafy_db_status_overall_function END ===========================================')
    return True
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== create_query_table_summary_triviafy_db_status_overall_function END ===========================================')
      return None
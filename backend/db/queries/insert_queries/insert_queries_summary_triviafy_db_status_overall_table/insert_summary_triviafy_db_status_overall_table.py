# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def insert_summary_triviafy_db_status_overall_table_function(postgres_connection, postgres_cursor, pk_index, team_id,channel_id,team_name,channel_name,total_team_channel_users,free_trial_total_users_count_match,free_trial_auth_id_and_uuid_no_duplicates,free_trial_expired,free_trial_days_left,latest_sub_month_status_exists,latest_sub_month_paid_status,categories_selected_str,quiz_settings_start_day_of_week,quiz_settings_start_time_of_day,quiz_settings_end_day_of_week,quiz_settings_end_time_of_day,quiz_settings_questions_per_quiz,latest_quiz_should_be_open_check,latest_quiz_should_be_closed_check,quiz_created_this_week,quiz_master_latest_quiz_uuid,latest_quiz_timestamp_created,latest_quiz_start_date,latest_quiz_start_day_of_week,latest_quiz_start_time,latest_quiz_end_date,latest_quiz_end_day_of_week,latest_quiz_end_time,latest_quiz_num_questions,latest_quiz_count,user_quiz_settings_start_day_of_week_unchanged,user_quiz_settings_start_time_unchanged,user_quiz_settings_end_day_of_week_unchanged,user_quiz_settings_end_time_unchanged,user_quiz_settings_num_questions_unchanged,remaining_unasked_num_questions_all_categories,remaining_unasked_num_questions_all_categories_below_threshold,remaining_unasked_num_questions_category_specific,remaining_unasked_questions_category_below_threshold,all_team_channel_users_received_email_account_created,email_sent_count_all_users_received_quiz_open,email_sent_count_all_users_received_quiz_closed,slack_message_sent_team_channel_received_quiz_open,slack_message_sent_received_quiz_pre_close_reminder,slack_message_sent_team_channel_received_quiz_closed,total_team_channel_users_answered_new_user_questionnaire,percent_team_channel_users_answered_new_user_questionnaire,total_team_channel_users_answered_quiz_questions,percent_team_channel_users_answered_quiz_questions,percent_team_channel_users_answered_quiz_correct_answers,quiz_winner_this_week_email,quiz_winner_this_week_email_cumulative_win_total,min_account_created_date,total_weeks_active,team_channel_skipped_quiz_count,payment_admins_arr,payment_admins_arr_len):
  localhost_print_function('=========================================== insert_summary_triviafy_db_status_overall_table_function START ===========================================')
  
  # ------------------------ Query START ------------------------
  postgres_insert_query = """INSERT INTO summary_triviafy_db_status_overall VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
  # ------------------------ Query END ------------------------


  # ------------------------ Record row START ------------------------
  record_to_insert = (pk_index, team_id,channel_id,team_name,channel_name,total_team_channel_users,free_trial_total_users_count_match,free_trial_auth_id_and_uuid_no_duplicates,free_trial_expired,free_trial_days_left,latest_sub_month_status_exists,latest_sub_month_paid_status,categories_selected_str,quiz_settings_start_day_of_week,quiz_settings_start_time_of_day,quiz_settings_end_day_of_week,quiz_settings_end_time_of_day,quiz_settings_questions_per_quiz,latest_quiz_should_be_open_check,latest_quiz_should_be_closed_check,quiz_created_this_week,quiz_master_latest_quiz_uuid,latest_quiz_timestamp_created,latest_quiz_start_date,latest_quiz_start_day_of_week,latest_quiz_start_time,latest_quiz_end_date,latest_quiz_end_day_of_week,latest_quiz_end_time,latest_quiz_num_questions,latest_quiz_count,user_quiz_settings_start_day_of_week_unchanged,user_quiz_settings_start_time_unchanged,user_quiz_settings_end_day_of_week_unchanged,user_quiz_settings_end_time_unchanged,user_quiz_settings_num_questions_unchanged,remaining_unasked_num_questions_all_categories,remaining_unasked_num_questions_all_categories_below_threshold,remaining_unasked_num_questions_category_specific,remaining_unasked_questions_category_below_threshold,all_team_channel_users_received_email_account_created,email_sent_count_all_users_received_quiz_open,email_sent_count_all_users_received_quiz_closed,slack_message_sent_team_channel_received_quiz_open,slack_message_sent_received_quiz_pre_close_reminder,slack_message_sent_team_channel_received_quiz_closed,total_team_channel_users_answered_new_user_questionnaire,percent_team_channel_users_answered_new_user_questionnaire,total_team_channel_users_answered_quiz_questions,percent_team_channel_users_answered_quiz_questions,percent_team_channel_users_answered_quiz_correct_answers,quiz_winner_this_week_email,quiz_winner_this_week_email_cumulative_win_total,min_account_created_date,total_weeks_active,team_channel_skipped_quiz_count,payment_admins_arr,payment_admins_arr_len)
  # ------------------------ Record row END ------------------------


  # ------------------------ Insert attempt START ------------------------
  try:
    postgres_cursor.execute(postgres_insert_query, record_to_insert)
    postgres_connection.commit()
    localhost_print_function('=========================================== insert_summary_triviafy_db_status_overall_table_function END ===========================================')
    return True
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== insert_summary_triviafy_db_status_overall_table_function END ===========================================')
      return False
  # ------------------------ Insert attempt END ------------------------
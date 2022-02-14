# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_slack_messages_sent_table.select_triviafy_slack_messages_sent_table_search_subject_sent_count import select_triviafy_slack_messages_sent_table_search_subject_sent_count_function

# -------------------------------------------------------------- Main
def job_check_db_status_overall_slack_messages_sent_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict):
  localhost_print_function('=========================================== job_check_db_status_overall_slack_messages_sent_checks_function START ===========================================')

  # ------------------------ Assign Variables START ------------------------
  total_team_channel_users = db_check_dict[team_id][channel_id]['total_team_channel_users']
  quiz_master_latest_quiz_uuid = db_check_dict[team_id][channel_id]['quiz_master_latest_quiz_uuid']
  # ------------------------ Assign Variables END ------------------------


  # ------------------------ Check Quiz Open Count START ------------------------
  if db_check_dict[team_id][channel_id]['latest_quiz_should_be_open_check'] == True and db_check_dict[team_id][channel_id]['quiz_created_this_week'] == True:
    slack_message_sent_search_category = 'Quiz Open'
    total_team_channel_received_slack_message_quiz_open = select_triviafy_slack_messages_sent_table_search_subject_sent_count_function(postgres_connection, postgres_cursor, slack_message_sent_search_category, quiz_master_latest_quiz_uuid)
    db_check_dict[team_id][channel_id]['slack_message_sent_team_channel_received_quiz_open'] = total_team_channel_received_slack_message_quiz_open == 1
  else:
    db_check_dict[team_id][channel_id]['slack_message_sent_team_channel_received_quiz_open'] = None
  # ------------------------ Check Quiz Open Count END ------------------------


  # ------------------------ Check Quiz Close Count START ------------------------
  if db_check_dict[team_id][channel_id]['latest_quiz_should_be_closed_check'] == True and db_check_dict[team_id][channel_id]['quiz_created_this_week'] == True:
    slack_message_sent_search_category = 'Quiz Pre Close Reminder'
    total_team_channel_received_slack_message_quiz_pre_close_reminder = select_triviafy_slack_messages_sent_table_search_subject_sent_count_function(postgres_connection, postgres_cursor, slack_message_sent_search_category, quiz_master_latest_quiz_uuid)
    db_check_dict[team_id][channel_id]['slack_message_sent_received_quiz_pre_close_reminder'] = total_team_channel_received_slack_message_quiz_pre_close_reminder == 1
    
    slack_message_sent_search_category = 'Quiz Closed and Graded'
    total_team_channel_received_slack_message_quiz_closed = select_triviafy_slack_messages_sent_table_search_subject_sent_count_function(postgres_connection, postgres_cursor, slack_message_sent_search_category, quiz_master_latest_quiz_uuid)
    db_check_dict[team_id][channel_id]['slack_message_sent_team_channel_received_quiz_closed'] = total_team_channel_received_slack_message_quiz_closed == 1
  else:
    db_check_dict[team_id][channel_id]['slack_message_sent_received_quiz_pre_close_reminder'] = None
    db_check_dict[team_id][channel_id]['slack_message_sent_team_channel_received_quiz_closed'] = None
  # ------------------------ Check Quiz Close Count END ------------------------
  

  localhost_print_function('=========================================== job_check_db_status_overall_slack_messages_sent_checks_function END ===========================================')
  return db_check_dict
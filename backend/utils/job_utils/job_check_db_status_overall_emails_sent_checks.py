# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_emails_sent_table.select_triviafy_emails_sent_table_search_subject_sent_count import select_triviafy_emails_sent_table_search_subject_sent_count_function
from backend.db.queries.select_queries.select_queries_triviafy_emails_sent_table.select_triviafy_emails_sent_table_count_account_created_emails_per_team_channel import select_triviafy_emails_sent_table_count_account_created_emails_per_team_channel_function

# -------------------------------------------------------------- Main
def job_check_db_status_overall_emails_sent_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict):
  localhost_print_function('=========================================== job_check_db_status_overall_emails_sent_checks_function START ===========================================')

  # ------------------------ Assign Variables START ------------------------
  total_team_channel_users = db_check_dict[team_id][channel_id]['total_team_channel_users']
  quiz_master_latest_quiz_uuid = db_check_dict[team_id][channel_id]['quiz_master_latest_quiz_uuid']
  # ------------------------ Assign Variables END ------------------------


  # ------------------------ Count Account Created Email START ------------------------
  email_sent_search_category = 'Account Created'
  total_team_channel_users_received_email_account_created = select_triviafy_emails_sent_table_count_account_created_emails_per_team_channel_function(postgres_connection, postgres_cursor, team_id, channel_id, email_sent_search_category)
  if total_team_channel_users_received_email_account_created != total_team_channel_users:
    localhost_print_function('Error: not all users received Account Created Email')
    localhost_print_function('=========================================== job_check_db_status_overall_emails_sent_checks_function END ===========================================')
    return False
  db_check_dict[team_id][channel_id]['all_team_channel_users_received_email_account_created'] = total_team_channel_users == total_team_channel_users_received_email_account_created
  # ------------------------ Count Account Created Email END ------------------------


  # ------------------------ Check Quiz Open Count START ------------------------
  if db_check_dict[team_id][channel_id]['latest_quiz_should_be_open_check'] == True and db_check_dict[team_id][channel_id]['quiz_created_this_week'] == True:
    email_sent_search_category = 'Quiz Open'
    total_team_channel_users_received_email_quiz_open = select_triviafy_emails_sent_table_search_subject_sent_count_function(postgres_connection, postgres_cursor, email_sent_search_category, quiz_master_latest_quiz_uuid)
    db_check_dict[team_id][channel_id]['email_sent_count_all_users_received_quiz_open'] = total_team_channel_users == total_team_channel_users_received_email_quiz_open
  else:
    db_check_dict[team_id][channel_id]['email_sent_count_all_users_received_quiz_open'] = None
  # ------------------------ Check Quiz Open Count END ------------------------


  # ------------------------ Check Quiz Close Count START ------------------------
  if db_check_dict[team_id][channel_id]['latest_quiz_should_be_closed_check'] == True and db_check_dict[team_id][channel_id]['quiz_created_this_week'] == True:
    email_sent_search_category = 'Quiz Closed and Graded'
    total_team_channel_users_received_email_quiz_closed = select_triviafy_emails_sent_table_search_subject_sent_count_function(postgres_connection, postgres_cursor, email_sent_search_category, quiz_master_latest_quiz_uuid)
    db_check_dict[team_id][channel_id]['email_sent_count_all_users_received_quiz_closed'] = total_team_channel_users == total_team_channel_users_received_email_quiz_closed
  else:
    db_check_dict[team_id][channel_id]['email_sent_count_all_users_received_quiz_closed'] = None
  # ------------------------ Check Quiz Close Count END ------------------------
  

  localhost_print_function('=========================================== job_check_db_status_overall_emails_sent_checks_function END ===========================================')
  return db_check_dict
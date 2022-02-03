# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_emails_sent_table.select_triviafy_emails_sent_table_search_subject_sent_count import select_triviafy_emails_sent_table_search_subject_sent_count_function

# -------------------------------------------------------------- Main
def job_check_db_status_overall_emails_sent_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict):
  localhost_print_function('=========================================== job_check_db_status_overall_emails_sent_checks_function START ===========================================')

  # ------------------------ Check Quiz Open Count START ------------------------
  if db_check_dict[team_id][channel_id]['latest_quiz_should_be_open_check'] == True and db_check_dict[team_id][channel_id]['quiz_created_this_week'] == True:
    total_team_channel_users = db_check_dict[team_id][channel_id]['total_team_channel_users']
    quiz_master_latest_quiz_uuid = db_check_dict[team_id][channel_id]['quiz_master_latest_quiz_uuid']

    email_sent_search_category = 'Quiz Open'
    total_team_channel_users_received_email_quiz_open = select_triviafy_emails_sent_table_search_subject_sent_count_function(postgres_connection, postgres_cursor, email_sent_search_category, quiz_master_latest_quiz_uuid)
    db_check_dict[team_id][channel_id]['email_sent_count_all_users_received_quiz_open'] = total_team_channel_users == total_team_channel_users_received_email_quiz_open
  else:
    db_check_dict[team_id][channel_id]['email_sent_count_all_users_received_quiz_open'] = None
  # ------------------------ Check Quiz Open Count END ------------------------
  

  localhost_print_function('=========================================== job_check_db_status_overall_emails_sent_checks_function END ===========================================')
  return db_check_dict
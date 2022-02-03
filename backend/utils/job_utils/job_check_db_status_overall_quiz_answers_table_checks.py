# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_quiz_answers_master_table.select_triviafy_quiz_answers_master_table_count_per_team_channel import select_triviafy_quiz_answers_master_table_count_per_team_channel_function
from backend.db.queries.select_queries.select_queries_triviafy_quiz_answers_master_table.select_triviafy_quiz_answers_master_table_count_correct_answers_per_team_channel import select_triviafy_quiz_answers_master_table_count_correct_answers_per_team_channel_function

# -------------------------------------------------------------- Main
def job_check_db_status_overall_quiz_answers_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict):
  localhost_print_function('=========================================== job_check_db_status_overall_quiz_answers_table_checks_function START ===========================================')

  # ------------------------ Assign Variables START ------------------------
  total_team_channel_users = db_check_dict[team_id][channel_id]['total_team_channel_users']
  quiz_master_latest_quiz_uuid = db_check_dict[team_id][channel_id]['quiz_master_latest_quiz_uuid']
  latest_quiz_num_questions = db_check_dict[team_id][channel_id]['latest_quiz_num_questions']
  # ------------------------ Assign Variables END ------------------------


  # ------------------------ Count Quiz Answers Users START ------------------------
  total_team_channel_answered_quiz_questions = select_triviafy_quiz_answers_master_table_count_per_team_channel_function(postgres_connection, postgres_cursor, team_id, channel_id, quiz_master_latest_quiz_uuid)
  if total_team_channel_answered_quiz_questions != 0:
    total_team_channel_users_answered_quiz_questions = int(total_team_channel_answered_quiz_questions / latest_quiz_num_questions)
    db_check_dict[team_id][channel_id]['total_team_channel_users_answered_quiz_questions'] = total_team_channel_users_answered_quiz_questions
    db_check_dict[team_id][channel_id]['percent_team_channel_users_answered_quiz_questions'] = round((float(total_team_channel_users_answered_quiz_questions) / float(total_team_channel_users)),2)
  else:
    db_check_dict[team_id][channel_id]['total_team_channel_users_answered_quiz_questions'] = 0
    db_check_dict[team_id][channel_id]['percent_team_channel_users_answered_quiz_questions'] = 0.0
  # ------------------------ Count Quiz Answers Users END ------------------------


  # ------------------------ Count Quiz Correct Answers START ------------------------
  total_team_channel_correct_answers_quiz_questions = select_triviafy_quiz_answers_master_table_count_correct_answers_per_team_channel_function(postgres_connection, postgres_cursor, team_id, channel_id, quiz_master_latest_quiz_uuid)
  if total_team_channel_correct_answers_quiz_questions != 0:
    db_check_dict[team_id][channel_id]['percent_team_channel_users_answered_quiz_correct_answers'] = round((float(total_team_channel_correct_answers_quiz_questions) / float(total_team_channel_answered_quiz_questions)),2)
  else:
    db_check_dict[team_id][channel_id]['percent_team_channel_users_answered_quiz_correct_answers'] = 0.0
  # ------------------------ Count Quiz Correct Answers END ------------------------
  

  localhost_print_function('=========================================== job_check_db_status_overall_quiz_answers_table_checks_function END ===========================================')
  return db_check_dict
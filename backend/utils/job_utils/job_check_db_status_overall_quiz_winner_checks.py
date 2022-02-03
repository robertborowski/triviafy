# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_quiz_winners_table.select_quiz_winner_count_for_team_channel_combo_quiz_specific import select_quiz_winner_count_for_team_channel_combo_quiz_specific_function
from backend.db.queries.select_queries.select_queries_triviafy_quiz_winners_table.select_quiz_winner_count_for_user_email_specific_team_channel import select_quiz_winner_count_for_user_email_specific_team_channel_function

# -------------------------------------------------------------- Main
def job_check_db_status_overall_quiz_winner_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict):
  localhost_print_function('=========================================== job_check_db_status_overall_quiz_winner_checks_function START ===========================================')

  # ------------------------ Assign Variables START ------------------------
  quiz_master_latest_quiz_uuid = db_check_dict[team_id][channel_id]['quiz_master_latest_quiz_uuid']
  # ------------------------ Assign Variables END ------------------------


  # ------------------------ Identify Quiz Winner START ------------------------
  quiz_winner_this_week_email = select_quiz_winner_count_for_team_channel_combo_quiz_specific_function(postgres_connection, postgres_cursor, team_id, channel_id, quiz_master_latest_quiz_uuid)
  if quiz_winner_this_week_email != None:
    db_check_dict[team_id][channel_id]['quiz_winner_this_week_email'] = quiz_winner_this_week_email
  else:
    db_check_dict[team_id][channel_id]['quiz_winner_this_week_email'] = None
  # ------------------------ Identify Quiz Winner END ------------------------


  # ------------------------ Get Quiz Winner Total Wins START ------------------------
  if quiz_winner_this_week_email != None:
    quiz_winner_this_week_email_cumulative_win_total = select_quiz_winner_count_for_user_email_specific_team_channel_function(postgres_connection, postgres_cursor, team_id, channel_id, quiz_winner_this_week_email)
    db_check_dict[team_id][channel_id]['quiz_winner_this_week_email_cumulative_win_total'] = quiz_winner_this_week_email_cumulative_win_total
  else:
    db_check_dict[team_id][channel_id]['quiz_winner_this_week_email_cumulative_win_total'] = 0
  # ------------------------ Get Quiz Winner Total Wins END ------------------------
  

  localhost_print_function('=========================================== job_check_db_status_overall_quiz_winner_checks_function END ===========================================')
  return db_check_dict
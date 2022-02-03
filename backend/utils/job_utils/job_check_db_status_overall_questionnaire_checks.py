# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_new_user_questionnaire_response_table.select_new_user_questionnaire_count_per_team_channel import select_new_user_questionnaire_count_per_team_channel_function

# -------------------------------------------------------------- Main
def job_check_db_status_overall_questionnaire_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict):
  localhost_print_function('=========================================== job_check_db_status_overall_questionnaire_checks_function START ===========================================')

  # ------------------------ Assign Variables START ------------------------
  total_team_channel_users = db_check_dict[team_id][channel_id]['total_team_channel_users']
  # ------------------------ Assign Variables END ------------------------


  # ------------------------ Count Questionnaire Feedback START ------------------------
  total_team_channel_users_answered_questionnaire = select_new_user_questionnaire_count_per_team_channel_function(postgres_connection, postgres_cursor, team_id, channel_id)
  if total_team_channel_users_answered_questionnaire != 0:
    db_check_dict[team_id][channel_id]['total_team_channel_users_answered_new_user_questionnaire'] = total_team_channel_users_answered_questionnaire
    db_check_dict[team_id][channel_id]['percent_team_channel_users_answered_new_user_questionnaire'] = round((float(total_team_channel_users_answered_questionnaire) / float(total_team_channel_users)),2)
  else:
    db_check_dict[team_id][channel_id]['total_team_channel_users_answered_new_user_questionnaire'] = 0
    db_check_dict[team_id][channel_id]['percent_team_channel_users_answered_new_user_questionnaire'] = 0.0
  # ------------------------ Count Questionnaire Feedback END ------------------------
  

  localhost_print_function('=========================================== job_check_db_status_overall_questionnaire_checks_function END ===========================================')
  return db_check_dict
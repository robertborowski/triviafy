# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_skipped_quizzes_company_team_level_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id, today_date_str):
  localhost_print_function('=========================================== select_skipped_quizzes_company_team_level_function START ===========================================')

  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT quiz.*FROM triviafy_quiz_master_table AS quiz LEFT JOIN triviafy_user_login_information_table_slack AS LOGIN ON quiz.quiz_slack_team_id=login.user_slack_workspace_team_id AND quiz.quiz_slack_channel_id=login.user_slack_channel_id WHERE login.user_slack_workspace_team_id=%s AND login.user_slack_channel_id=%s AND quiz.quiz_end_date<%s AND quiz.uuid_quiz NOT IN(SELECT winners.quiz_winner_quiz_uuid_fk FROM triviafy_quiz_winners_table AS winners LEFT JOIN triviafy_quiz_master_table AS quiz ON winners.quiz_winner_quiz_uuid_fk=quiz.uuid_quiz LEFT JOIN triviafy_user_login_information_table_slack AS LOGIN ON winners.quiz_winner_user_uuid_fk=login.user_uuid WHERE login.user_slack_workspace_team_id=%s AND login.user_slack_channel_id=%s) GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13;", [slack_workspace_team_id, slack_channel_id, today_date_str, slack_workspace_team_id, slack_channel_id])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = postgres_cursor.fetchall()
    if result_arr == None or result_arr == []:
      localhost_print_function('=========================================== select_skipped_quizzes_company_team_level_function END ===========================================')
      return None
    
    localhost_print_function('=========================================== select_skipped_quizzes_company_team_level_function END ===========================================')  
    return result_arr
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_skipped_quizzes_company_team_level_function END ===========================================')
      return result_arr
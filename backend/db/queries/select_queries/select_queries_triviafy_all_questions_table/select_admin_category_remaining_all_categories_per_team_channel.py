# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_admin_category_remaining_all_categories_per_team_channel_function(postgres_connection, postgres_cursor, user_slack_workspace_team_id, user_slack_channel_id):
  localhost_print_function('=========================================== select_admin_category_remaining_all_categories_per_team_channel_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT COUNT(*)FROM triviafy_all_questions_table AS q WHERE q.question_uuid NOT IN(SELECT a.quiz_question_asked_tracking_question_uuid FROM triviafy_quiz_questions_asked_to_company_slack_table AS a WHERE a.quiz_question_asked_tracking_slack_team_id=%s AND a.quiz_question_asked_tracking_slack_channel_id=%s)AND q.question_approved_for_release=TRUE;", [user_slack_workspace_team_id, user_slack_channel_id])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_admin_category_remaining_all_categories_per_team_channel_function END ===========================================')
      return None
    
    localhost_print_function('=========================================== select_admin_category_remaining_all_categories_per_team_channel_function END ===========================================')
    return result_row[0]
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_admin_category_remaining_all_categories_per_team_channel_function END ===========================================')
      return None
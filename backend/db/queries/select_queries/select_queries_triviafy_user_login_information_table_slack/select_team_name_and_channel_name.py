# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_team_name_and_channel_name_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id):
  localhost_print_function('=========================================== select_team_name_and_channel_name_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT DISTINCT user_slack_workspace_team_name,user_slack_channel_name FROM triviafy_user_login_information_table_slack WHERE user_slack_workspace_team_id=%s AND user_slack_channel_id=%s GROUP BY user_slack_workspace_team_name,user_slack_channel_name;", [slack_workspace_team_id, slack_channel_id])
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    result_row = postgres_cursor.fetchone()
    
    if result_row == None or result_row == []:
      localhost_print_function('=========================================== select_team_name_and_channel_name_function END ===========================================')
      return None
    

    localhost_print_function('=========================================== select_team_name_and_channel_name_function END ===========================================')
    return result_row
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_team_name_and_channel_name_function END ===========================================')
      return None
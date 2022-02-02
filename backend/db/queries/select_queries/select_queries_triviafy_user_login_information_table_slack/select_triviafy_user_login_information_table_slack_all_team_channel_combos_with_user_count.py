# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_triviafy_user_login_information_table_slack_all_team_channel_combos_with_user_count_function(postgres_connection, postgres_cursor):
  localhost_print_function('=========================================== select_triviafy_user_login_information_table_slack_all_team_channel_combos_with_user_count_function START ===========================================')
  
  try:
    # ------------------------ Query START ------------------------
    postgres_cursor.execute("SELECT DISTINCT l.user_slack_workspace_team_id,l.user_slack_channel_id,l.user_slack_workspace_team_name,l.user_slack_channel_name,COUNT(l.*)AS num_users FROM triviafy_user_login_information_table_slack AS l GROUP BY l.user_slack_workspace_team_id,l.user_slack_channel_id,l.user_slack_workspace_team_name,l.user_slack_channel_name ORDER BY l.user_slack_workspace_team_id,l.user_slack_channel_id,l.user_slack_workspace_team_name,l.user_slack_channel_name;")
    # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = postgres_cursor.fetchall()
    if result_arr == None or result_arr == []:
      localhost_print_function('=========================================== select_triviafy_user_login_information_table_slack_all_team_channel_combos_with_user_count_function END ===========================================')
      return None

    localhost_print_function('=========================================== select_triviafy_user_login_information_table_slack_all_team_channel_combos_with_user_count_function END ===========================================')
    return result_arr
    # ------------------------ Query Result END ------------------------
  
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_triviafy_user_login_information_table_slack_all_team_channel_combos_with_user_count_function END ===========================================')
      return None
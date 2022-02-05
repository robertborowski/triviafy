# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_payment_admins import select_triviafy_user_login_information_table_slack_all_payment_admins_function

# -------------------------------------------------------------- Main
def job_check_db_status_overall_payment_admins_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict):
  localhost_print_function('=========================================== job_check_db_status_overall_payment_admins_function START ===========================================')

  # ------------------------ Count Payment Admins START ------------------------
  payment_admins_arr = select_triviafy_user_login_information_table_slack_all_payment_admins_function(postgres_connection, postgres_cursor, team_id, channel_id)

  if payment_admins_arr == None or len(payment_admins_arr) < 1:
    localhost_print_function('=========================================== job_check_db_status_overall_payment_admins_function END ===========================================')
    print('Error: Payment Admins total error')
    return False
  
  else:
    db_check_dict[team_id][channel_id]['payment_admins_arr'] = payment_admins_arr
    db_check_dict[team_id][channel_id]['payment_admins_arr_len'] = len(payment_admins_arr)
  # ------------------------ Count Payment Admins END ------------------------
  

  localhost_print_function('=========================================== job_check_db_status_overall_payment_admins_function END ===========================================')
  return db_check_dict
# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_slack_payment_status_table.select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only import select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only_function
from backend.db.queries.select_queries.select_queries_triviafy_slack_payment_status_table.select_triviafy_slack_payment_status_table_team_channel_year_month_combo_count import select_triviafy_slack_payment_status_table_team_channel_year_month_combo_count_function

# -------------------------------------------------------------- Main
def job_check_db_status_overall_payment_status_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict, today_date_year, today_date_month):
  localhost_print_function('=========================================== job_check_db_status_overall_payment_status_table_checks_function START ===========================================')
  

  # ------------------------ Check Payment Status Rules - Distinct Count Latest START ------------------------
  payment_status_month_count_arr = select_triviafy_slack_payment_status_table_team_channel_year_month_combo_count_function(postgres_connection, postgres_cursor, team_id, channel_id, today_date_year, today_date_month)
  int_payment_status_month_count = payment_status_month_count_arr[0]
  if int_payment_status_month_count >= 2:
    localhost_print_function('=========================================== job_check_db_status_overall_payment_status_table_checks_function END ===========================================')
    print('Error: There is more than 1 month tracking row for the payment staus table team channel combo')
    return False
  # ------------------------ Check Payment Status Rules - Distinct Count Latest END ------------------------


  # ------------------------ Check Payment Status Rules - Latest Date START ------------------------
  payment_status_arr = select_triviafy_slack_payment_status_table_team_channel_year_month_combo_status_only_function(postgres_connection, postgres_cursor, team_id, channel_id, today_date_year, today_date_month)
  if payment_status_arr == None:
    db_check_dict[team_id][channel_id]['latest_sub_month_status_exists'] = False
    db_check_dict[team_id][channel_id]['latest_sub_month_paid_status'] = False
  else:
    db_check_dict[team_id][channel_id]['latest_sub_month_status_exists'] = True
    db_check_dict[team_id][channel_id]['latest_sub_month_paid_status'] = payment_status_arr[0]
  # ------------------------ Check Payment Status Rules - Latest Date END ------------------------

  localhost_print_function('=========================================== job_check_db_status_overall_payment_status_table_checks_function END ===========================================')
  return db_check_dict
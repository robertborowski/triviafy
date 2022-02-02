# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_categories_selected_table.select_categories_team_channel_combo_count import select_categories_team_channel_combo_count_function
from backend.db.queries.select_queries.select_queries_triviafy_categories_selected_table.select_current_categories_team_channel_combo import select_current_categories_team_channel_combo_function

# -------------------------------------------------------------- Main
def job_check_db_status_overall_categories_table_checks_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict):
  localhost_print_function('=========================================== job_check_db_status_overall_categories_table_checks_function START ===========================================')
  

  # ------------------------ Check Categories Rules - Count Categories START ------------------------
  int_categories_count_team_channel_combo = select_categories_team_channel_combo_count_function(postgres_connection, postgres_cursor, team_id, channel_id)
  if int_categories_count_team_channel_combo != 1:
    localhost_print_function('=========================================== job_check_db_status_overall_categories_table_checks_function END ===========================================')
    print('Error: There is more than 1 row for the team channel combo categories table')
    return False
  # ------------------------ Check Categories Rules - Count Categories END ------------------------


  # ------------------------ Check Categories Rules - Get Categories START ------------------------
  categories_selected_str = select_current_categories_team_channel_combo_function(postgres_connection, postgres_cursor, team_id, channel_id)
  db_check_dict[team_id][channel_id]['categories_selected_str'] = categories_selected_str
  # ------------------------ Check Categories Rules - Get Categories END ------------------------

  localhost_print_function('=========================================== job_check_db_status_overall_categories_table_checks_function END ===========================================')
  return db_check_dict
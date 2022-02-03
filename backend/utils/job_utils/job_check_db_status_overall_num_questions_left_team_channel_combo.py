# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_all_questions_table.select_admin_category_remaining_all_categories_per_team_channel import select_admin_category_remaining_all_categories_per_team_channel_function
from backend.db.queries.select_queries.select_queries_triviafy_all_questions_table.select_admin_category_remaining_questions_per_team_channel_combo import select_admin_category_remaining_questions_per_team_channel_combo_function


# -------------------------------------------------------------- Main
def job_check_db_status_overall_num_questions_left_team_channel_combo_function(postgres_connection, postgres_cursor, team_id, channel_id, db_check_dict):
  localhost_print_function('=========================================== job_check_db_status_overall_num_questions_left_team_channel_combo_function START ===========================================')

  acceptable_question_threshold = 50
  
  # ------------------------ Check Num Questions Left For All Categories START ------------------------
  remaining_unasked_num_questions_all_categories = select_admin_category_remaining_all_categories_per_team_channel_function(postgres_connection, postgres_cursor, team_id, channel_id)
  db_check_dict[team_id][channel_id]['remaining_unasked_num_questions_all_categories'] = remaining_unasked_num_questions_all_categories
  remaining_unasked_num_questions_all_categories_below_threshold = False
  if remaining_unasked_num_questions_all_categories <= acceptable_question_threshold:
    remaining_unasked_num_questions_all_categories_below_threshold = True
  db_check_dict[team_id][channel_id]['remaining_unasked_num_questions_all_categories_below_threshold'] = remaining_unasked_num_questions_all_categories_below_threshold
  # ------------------------ Check Num Questions Left For All Categories END ------------------------
  

  # ------------------------ Check Num Questions Left Category Specific START ------------------------
  categories_selected_str = db_check_dict[team_id][channel_id]['categories_selected_str']

  if categories_selected_str == 'All Categories':
    db_check_dict[team_id][channel_id]['remaining_unasked_num_questions_category_specific'] = remaining_unasked_num_questions_all_categories
    remaining_unasked_num_questions_category_specific_below_threshold = False
    if remaining_unasked_num_questions_all_categories <= acceptable_question_threshold:
      remaining_unasked_num_questions_category_specific_below_threshold = True
    db_check_dict[team_id][channel_id]['remaining_unasked_num_questions_category_specific_below_threshold'] = remaining_unasked_num_questions_category_specific_below_threshold
  
  else:
    # Turn str into array
    company_current_categories_arr = categories_selected_str.split(',')
    
    # LIKE str for the SQL SELECT Statement
    sql_like_statement_arr = []
    for i_category in company_current_categories_arr:
      indv_like_statement = "question_categories_list LIKE '%%" + i_category + "%%'"
      sql_like_statement_arr.append(indv_like_statement)
    sql_like_statement_str = ' OR '.join(sql_like_statement_arr)

    # SQL SELECT Statement to pull all category remainder counts
    remaining_category_count_arr_of_dict = select_admin_category_remaining_questions_per_team_channel_combo_function(postgres_connection, postgres_cursor, team_id, channel_id, sql_like_statement_str)

    # Loop through query result to get total questions left category specific
    if len(remaining_category_count_arr_of_dict) == 0:
      remaining_unasked_num_questions_category_specific = 0
    else:
      remaining_unasked_num_questions_category_specific = 0
      for i_dict in remaining_category_count_arr_of_dict:
        remaining_unasked_num_questions_category_specific += i_dict['count']
      
    db_check_dict[team_id][channel_id]['remaining_unasked_num_questions_category_specific'] = remaining_unasked_num_questions_category_specific
    remaining_unasked_num_questions_category_specific_below_threshold = False
    if remaining_unasked_num_questions_category_specific <= acceptable_question_threshold:
      remaining_unasked_num_questions_category_specific_below_threshold = True
    db_check_dict[team_id][channel_id]['remaining_unasked_num_questions_category_specific_below_threshold'] = remaining_unasked_num_questions_category_specific_below_threshold
  # ------------------------ Check Num Questions Left Category Specific END ------------------------


  localhost_print_function('=========================================== job_check_db_status_overall_num_questions_left_team_channel_combo_function END ===========================================')
  return db_check_dict
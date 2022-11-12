# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.candidates.sql_statements.sql_statements_select_general_v2_jobs import select_general_v2_jobs_function
from website.backend.candidates.sql_statements.sql_statements_delete_general_v1_jobs import delete_general_v1_jobs_function
# ------------------------ imports end ------------------------

# ------------------------ main start ------------------------
def job_candidates_remove_unsub_user_all_tables_function(postgres_connection, postgres_cursor):
  localhost_print_function('=========================================== job_candidates_remove_unsub_user_all_tables_function START ===========================================')
  
  # ------------------------ run specifics start ------------------------
  input_users_to_remove_arr = [
    # '_____input'
  ]
  if input_users_to_remove_arr == []:
    localhost_print_function('input user ids to delete')
    return False

  input_remove_row_table_column_arr = [
    ['candidates_assessment_graded_obj','created_assessment_user_id_fk'],
    ['candidates_assessments_created_obj','user_id_fk'],
    ['candidates_desired_languages_obj','user_id_fk'],
    ['candidates_schedule_obj','user_id_fk'],
    ['candidates_stripe_checkout_session_obj','fk_user_id'],
    ['candidates_uploaded_candidates_obj','user_id_fk'],
    ['candidates_user_obj','id']
  ]
  # ------------------------ run specifics end ------------------------
  
  # ------------------------ loop user start ------------------------
  for i_user_to_delete in input_users_to_remove_arr:
    # ------------------------ check if user is subscribed start ------------------------
    # ------------------------ sql variables start ------------------------
    sql_input_nested_arr = []
    current_arr = [input_remove_row_table_column_arr[0][0], input_remove_row_table_column_arr[0][1], i_user_to_delete]
    sql_input_nested_arr.append(current_arr)
    # ------------------------ sql variables end ------------------------
    query_result_obj = select_general_v2_jobs_function(postgres_connection, postgres_cursor, 'select_stripe_customer_status', additional_input=sql_input_nested_arr)
    if query_result_obj[0]['fk_stripe_customer_id'] != None:
      localhost_print_function(' --------------------- ')
      localhost_print_function(f'skip customer: {i_user_to_delete}')
      localhost_print_function(' --------------------- ')
      continue
    # ------------------------ check if user is subscribed end ------------------------
    # ------------------------ select summary start ------------------------
    for j_table_column in input_remove_row_table_column_arr:
      # ------------------------ sql variables start ------------------------
      sql_input_nested_arr = []
      current_arr = [j_table_column[0], j_table_column[1], i_user_to_delete]
      sql_input_nested_arr.append(current_arr)
      # ------------------------ sql variables end ------------------------
      query_result_arr_of_dicts = select_general_v2_jobs_function(postgres_connection, postgres_cursor, 'select_table1_column1_value1', additional_input=sql_input_nested_arr)
      localhost_print_function(f'i_user_to_delete: {i_user_to_delete} | j_table_column[0]: {j_table_column[0]}: {len(query_result_arr_of_dicts)}')
      # ------------------------ delete query start ------------------------
      if query_result_arr_of_dicts != [] and len(query_result_arr_of_dicts) > 0:
        delete_general_v1_jobs_function(postgres_connection, postgres_cursor, 'delete_table1_column1_value1', additional_input=sql_input_nested_arr)
        localhost_print_function(f'deleted: {len(query_result_arr_of_dicts)}')
      # ------------------------ delete query end ------------------------
    # ------------------------ select summary end ------------------------
    localhost_print_function(' ')
  # ------------------------ loop user end ------------------------
  localhost_print_function('=========================================== job_candidates_remove_unsub_user_all_tables_function END ===========================================')
  return True
# ------------------------ main end ------------------------
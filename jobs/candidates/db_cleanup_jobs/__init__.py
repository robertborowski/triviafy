# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.candidates.sql_statements.sql_statements_select_general_v2_jobs import select_general_v2_jobs_function
# ------------------------ imports end ------------------------

# ------------------------ main start ------------------------
def job_candidates_remove_unsub_user_all_tables_function(postgres_connection, postgres_cursor):
  localhost_print_function('=========================================== job_candidates_remove_unsub_user_all_tables_function START ===========================================')
  
  # ------------------------ run specifics start ------------------------
  input_users_to_remove_arr = [
    # '_____input'
    'abc'
  ]
  input_remove_row_table_column_arr = [
    ['candidates_assessments_created_obj','user_id_fk'],
    ['candidates_uploaded_candidates_obj','user_id_fk'],
    ['candidates_schedule_obj','user_id_fk']
  ]
  # ------------------------ run specifics end ------------------------
  
  # ------------------------ loop select start ------------------------
  for i_user_to_delete in input_users_to_remove_arr:
    for j_table_column in input_remove_row_table_column_arr:
      sql_input_dict = {
        'table_name': j_table_column[0],
        'column_name': j_table_column[1],
        'value_name': i_user_to_delete
      }
      query_result_arr_of_dicts = select_general_v2_jobs_function(postgres_connection, postgres_cursor, 'select_table1_column1_value1', additional_input=sql_input_dict)
      print(query_result_arr_of_dicts)
      print(' ')
  # ------------------------ loop select end ------------------------
  localhost_print_function('=========================================== job_candidates_remove_unsub_user_all_tables_function END ===========================================')
  return True
# ------------------------ main end ------------------------
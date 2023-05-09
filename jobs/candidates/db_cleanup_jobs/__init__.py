# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.candidates.sql_statements.sql_statements_select_general_v2_jobs import select_general_v2_jobs_function
from website.backend.candidates.sql_statements.sql_statements_select_general_v1_jobs import select_general_v1_jobs_function
from website.backend.candidates.sql_statements.sql_statements_delete_general_v1_jobs import delete_general_v1_jobs_function
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def job_candidates_clean_out_redis_function(postgres_connection, postgres_cursor):
  localhost_print_function('=========================================== job_candidates_clean_out_redis_function start ===========================================')
  # ------------------------ get all current user id's as set start ------------------------
  sql_input = 'user_obj'
  query_result_arr_of_dicts = select_general_v1_jobs_function(postgres_connection, postgres_cursor, 'select_table1_id', additional_input=sql_input)
  user_ids_set = {'a'}
  for i in query_result_arr_of_dicts:
    if i['id'] not in user_ids_set:
      user_ids_set.add(i['id'])
  user_ids_set.remove('a')
  # ------------------------ get all current user id's as set end ------------------------
  # ------------------------ loop through redis start ------------------------
  # Connect to redis database pool (no need to close)
  redis_connection = redis_connect_to_database_function()
  redis_keys = redis_connection.keys()
  redis_candidates_deleted_counter = 0
  for key in redis_keys:
    if 'bcooke' in str(key):
      value = redis_connection.get(key).decode('utf-8')
      if value not in user_ids_set:
        redis_connection.delete(key)
        redis_candidates_deleted_counter += 1
  localhost_print_function(f'redis_candidates_deleted_counter: {redis_candidates_deleted_counter}')
  # ------------------------ loop through redis end ------------------------
  localhost_print_function('=========================================== job_candidates_clean_out_redis_function start ===========================================')
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
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
    ['stripe_checkout_session_obj','fk_user_id'],
    ['candidates_uploaded_candidates_obj','user_id_fk'],
    ['activity_a_settings_obj','fk_user_id'],
    ['group_obj','fk_user_id'],
    ['user_obj','id']
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
    if query_result_obj == []:
      localhost_print_function('user id does not exist')
      return False
    if query_result_obj[0]['fk_stripe_customer_id'] != None and query_result_obj[0]['fk_stripe_customer_id'] != '':
      localhost_print_function(' --------------------- ')
      localhost_print_function(f'skip customer: {i_user_to_delete}')
      localhost_print_function(' --------------------- ')
      continue
    # ------------------------ check if user is subscribed end ------------------------
    # ------------------------ select summary start ------------------------
    for j_table_column in input_remove_row_table_column_arr:
      localhost_print_function(' - - - - - - - - - -')
      # ------------------------ sql variables start ------------------------
      sql_input_nested_arr = []
      current_arr = [j_table_column[0], j_table_column[1], i_user_to_delete]
      sql_input_nested_arr.append(current_arr)
      # ------------------------ sql variables end ------------------------
      query_result_arr_of_dicts = select_general_v2_jobs_function(postgres_connection, postgres_cursor, 'select_table1_column1_value1', additional_input=sql_input_nested_arr)
      localhost_print_function(f'i_user_to_delete: {i_user_to_delete} | {len(query_result_arr_of_dicts)} rows in {j_table_column[0]} table')
      # ------------------------ delete query start ------------------------
      if query_result_arr_of_dicts != [] and len(query_result_arr_of_dicts) > 0:
        delete_general_v1_jobs_function(postgres_connection, postgres_cursor, 'delete_table1_column1_value1', additional_input=sql_input_nested_arr)
        localhost_print_function(f'{len(query_result_arr_of_dicts)}: deleted')
      else:
        localhost_print_function('0: deleted')
        pass
      # ------------------------ delete query end ------------------------
    # ------------------------ select summary end ------------------------
    localhost_print_function(' ')
  # ------------------------ loop user end ------------------------
  localhost_print_function('=========================================== job_candidates_remove_unsub_user_all_tables_function END ===========================================')
  return True
# ------------------------ individual function end ------------------------
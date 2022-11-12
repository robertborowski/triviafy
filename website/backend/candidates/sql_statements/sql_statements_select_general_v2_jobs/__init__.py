# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import psycopg2
from psycopg2 import Error, extras
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== sql_statements_select __init__ START ===========================================')


# ------------------------ individual function start ------------------------
def select_general_v2_jobs_function(postgres_connection, postgres_cursor, tag_query_to_use, additional_input=None):
  localhost_print_function('=========================================== select_general_v2_jobs_function START ===========================================')
  # ------------------------ cursor dict start ------------------------
  cursor = postgres_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
  # ------------------------ cursor dict end ------------------------
  # ------------------------ select queries start ------------------------
  select_queries_dict = {
    'select_table1_column1_value1': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      {additional_input['table_name']} \
                    WHERE \
                      {additional_input['column_name']}='{additional_input['value_name']}';",
      'input_args': {}
    }
  }
  # ------------------------ select queries end ------------------------
  # ------------------------ execute sql start ------------------------
  try:
    cursor.execute(select_queries_dict[tag_query_to_use]['raw_query'])
  except:
    localhost_print_function('except hit')
    return False
  # ------------------------ execute sql end ------------------------
  # ------------------------ results start ------------------------
  result_arr = cursor.fetchall()
  cursor.close()
  result_arr_dicts = []
  for row in result_arr:
    result_arr_dicts.append(dict(row))
  # ------------------------ results end ------------------------
  localhost_print_function('=========================================== select_all_questions_created_by_owner_specific_page_function END ===========================================')
  return result_arr_dicts
  # ------------------------ Query Result END ------------------------

# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== sql_statements_select __init__ END ===========================================')
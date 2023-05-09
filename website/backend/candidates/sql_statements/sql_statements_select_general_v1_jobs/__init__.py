# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import psycopg2
from psycopg2 import Error, extras
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def select_general_v1_jobs_function(postgres_connection, postgres_cursor, tag_query_to_use, additional_input=None):
  # ------------------------ cursor dict start ------------------------
  cursor = postgres_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
  # ------------------------ cursor dict end ------------------------
  # ------------------------ select queries start ------------------------
  select_queries_dict = {
    'select_table1_id': {
      'raw_query': f"SELECT \
                      id \
                    FROM \
                      {additional_input};",
      'input_args': {}
    }
  }
  # ------------------------ select queries end ------------------------
  # ------------------------ execute sql start ------------------------
  # try:
  cursor.execute(select_queries_dict[tag_query_to_use]['raw_query'])
  # except:
  #   localhost_print_function('except hit')
  #   return False
  # ------------------------ execute sql end ------------------------
  # ------------------------ results start ------------------------
  result_arr = cursor.fetchall()
  cursor.close()
  result_arr_dicts = []
  for row in result_arr:
    result_arr_dicts.append(dict(row))
  # ------------------------ results end ------------------------
  return result_arr_dicts
  # ------------------------ Query Result END ------------------------
# ------------------------ individual function end ------------------------
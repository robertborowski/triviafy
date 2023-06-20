# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import psycopg2
from psycopg2 import Error, extras
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def select_manual_function(postgres_connection, postgres_cursor, tag_query_to_use, input1=None, input2=None, input3=None):
  # localhost_print_function(' ------------------------ select_manual_function start ------------------------ ')
  # ------------------------ select queries start ------------------------
  select_queries_dict = {
    'select1':
      f"SELECT \
          * \
        FROM \
          shows_queue_obj;"
  }
  # ------------------------ select queries end ------------------------
  # ------------------------ cursor start ------------------------
  cursor = postgres_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cursor.execute(select_queries_dict[tag_query_to_use])
  # ------------------------ cursor end ------------------------
  # ------------------------ results start ------------------------
  results_arr = cursor.fetchall()
  result_arr_dicts = []
  for row in results_arr:
    result_arr_dicts.append(dict(row))
  # ------------------------ results end ------------------------
  # ------------------------ check none start ------------------------
  if result_arr_dicts == [] or result_arr_dicts == None or len(result_arr_dicts) == 0:
    return None
  # ------------------------ check none end ------------------------
  return result_arr_dicts
# ------------------------ individual function end ------------------------
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import psycopg2
from psycopg2 import Error, extras
# ------------------------ imports end ------------------------

localhost_print_function(' ------------------------ select_queries employees __init__ start ------------------------ ')
# ------------------------ individual function start ------------------------
def select_manual_function(postgres_connection, postgres_cursor, tag_query_to_use, additional_input=None, additional_input2=None, additional_input3=None):
  localhost_print_function(' ------------------------ select_manual_function start ------------------------ ')
  # ------------------------ select queries start ------------------------
  select_queries_dict = {
    'select_groups_1':
      f"SELECT \
          fk_company_name, \
          public_group_id \
        FROM \
          employees_groups_obj;",
    'select_group_settings_1':
      f"SELECT \
          * \
        FROM \
          employees_group_settings_obj \
        WHERE \
          fk_group_id='{additional_input}';"
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
  localhost_print_function(' ------------------------ select_manual_function end ------------------------ ')
  return result_arr_dicts
# ------------------------ individual function end ------------------------
localhost_print_function(' ------------------------ select_queries employees __init__ end ------------------------ ')
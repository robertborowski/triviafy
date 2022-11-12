# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import psycopg2
from psycopg2 import Error, extras
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== sql_statements_select __init__ START ===========================================')


# ------------------------ individual function start ------------------------
def delete_general_v1_jobs_function(postgres_connection, postgres_cursor, tag_query_to_use, additional_input=None):
  # ------------------------ cursor dict start ------------------------
  cursor = postgres_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
  # ------------------------ cursor dict end ------------------------
  # ------------------------ select queries start ------------------------
  select_queries_dict = {
    'delete_table1_column1_value1': {
      'raw_query': f"DELETE FROM \
                      {additional_input[0][0]} \
                    WHERE \
                      {additional_input[0][1]}='{additional_input[0][2]}';",
      'input_args': {}
    }
  }
  # ------------------------ select queries end ------------------------
  # ------------------------ execute sql start ------------------------
  try:
    postgres_cursor.execute(select_queries_dict[tag_query_to_use]['raw_query'])
  except:
    localhost_print_function('except hit')
    return False
  # ------------------------ execute sql end ------------------------
  # ------------------------ Query Result START ------------------------
  postgres_connection.commit()
  return True
  # ------------------------ Query Result END ------------------------
  # ------------------------ Query Result END ------------------------

# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== sql_statements_select __init__ END ===========================================')
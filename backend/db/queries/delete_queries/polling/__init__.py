# ------------------------ imports start ------------------------
import psycopg2
from psycopg2 import Error, extras
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def delete_manual_function(postgres_connection, postgres_cursor, tag_query_to_use, input1=None, input2=None, input3=None):
  # ------------------------ delete queries start ------------------------
  delete_queries_dict = {
    'delete_polls': f"DELETE FROM polls_obj WHERE fk_show_id='{input1}';",
    'delete_shows': f"DELETE FROM shows_obj WHERE id='{input1}';",
    'delete_shows_following': f"DELETE FROM shows_following_obj WHERE fk_show_id='{input1}';",
    'delete_queue': f"DELETE FROM shows_queue_obj WHERE id='{input1}';"
  }
  # ------------------------ delete queries end ------------------------
  # ------------------------ cursor start ------------------------
  try:
    cursor = postgres_connection.cursor()
    cursor.execute(delete_queries_dict[tag_query_to_use])
    postgres_connection.commit()
  except:
    pass
  # ------------------------ cursor end ------------------------
  return True
# ------------------------ individual function end ------------------------
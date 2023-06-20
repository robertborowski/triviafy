# ------------------------ imports start ------------------------
import os, time
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.polling import select_manual_function
from backend.db.queries.insert_queries.polling import insert_manual_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def run_function():
  queue_on = True
  while queue_on == True:
    # ------------------------ open db connection start ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()
    # ------------------------ open db connection end ------------------------
    # ------------------------ select start ------------------------
    queue_result_arr_of_dict = select_manual_function(postgres_connection, postgres_cursor, 'select1')
    # ------------------------ select end ------------------------
    # ------------------------ if no results start ------------------------
    if queue_result_arr_of_dict == None:
      # ------------------------ close db connection start ------------------------
      postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
      # ------------------------ close db connection end ------------------------
      time.sleep(60)
    # ------------------------ if no results end ------------------------
    # ------------------------ if yes results start ------------------------
    else:
      # ------------------------ insert to db start ------------------------
      # insert_manual_function(postgres_connection, postgres_cursor, 'inserting_function_1', insert_inputs_arr)
      # ------------------------ insert to db end ------------------------
      # ------------------------ close db connection start ------------------------
      postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
      # ------------------------ close db connection end ------------------------
    # ------------------------ if yes results end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ run function start ------------------------
if __name__ == "__main__":
  run_function()
# ------------------------ run function end ------------------------
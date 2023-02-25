# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.employees import select_manual_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def employees_quiz_open_close_notifications():
  localhost_print_function(' ------------------------ employees_quiz_open_close_notifications start ------------------------ ')
  # ------------------------ open connection start ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ open connection end ------------------------
  # ------------------------ loop group start ------------------------
  db_groups_arr_of_dict = select_manual_function(postgres_connection, postgres_cursor, 'select_groups_1')
  localhost_print_function(' ------------- 0 ------------- ')
  for i in db_groups_arr_of_dict:
    localhost_print_function(f"i | type: {type(i)} | {i}")
  localhost_print_function(' ------------- 0 ------------- ')
  
  for i_group_dict in db_groups_arr_of_dict:
    db_group_settings_arr_of_dict = select_manual_function(postgres_connection, postgres_cursor, 'select_group_settings_1', i_group_dict['public_group_id'])
    localhost_print_function(' ------------- 1 ------------- ')
    for i in db_group_settings_arr_of_dict:
      localhost_print_function(f"i | type: {type(i)} | {i}")
    localhost_print_function(' ------------- 1 ------------- ')
  # ------------------------ loop group end ------------------------
  # ------------------------ close connection start ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ close connection end ------------------------
  localhost_print_function(' ------------------------ employees_quiz_open_close_notifications end ------------------------ ')
  return True
# ------------------------ individual function end ------------------------

# ------------------------ run function start ------------------------
if __name__ == "__main__":
  employees_quiz_open_close_notifications()
# ------------------------ run function end ------------------------
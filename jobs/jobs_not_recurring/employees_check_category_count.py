# -------------------------------------------------------------- Imports
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_all_questions_table.select_triviafy_category_count_totals import select_triviafy_category_count_totals_function
import pandas as pd
from backend.db.queries.select_queries.employees import select_manual_function

# -------------------------------------------------------------- Main Function
def employees_check_category_count_function():
  # Connect to DB
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  
  # SQL query
  db_arr_of_dict = select_manual_function(postgres_connection, postgres_cursor, 'select_categories_v1')
  
  # Loop and assign to dict
  master_dict = {}
  for i_dict in db_arr_of_dict:
    i_categories_str = i_dict['categories']
    try:
      i_categories_arr = i_categories_str.split(',')
      for j in i_categories_arr:
        j = j.strip()
        if j not in master_dict:
          master_dict[j] = 1
        else:
          master_dict[j] += 1
    except:
      i_categories_str = i_categories_str.strip()
      if i_categories_str not in master_dict:
        master_dict[i_categories_str] = 1
      else:
        master_dict[i_categories_str] += 1
  
  # Sort dict by key
  master_dict = {key: value for key, value in sorted(master_dict.items())}

  print(' --------------------------------------- ')
  # Print results
  print(' --> Sort by key')
  for k, v in master_dict.items():
    print(f'{k} : {v}')
  print(' --------------------------------------- ')

  print(' --> Sort by value')
  a1_sorted_keys = sorted(master_dict, key=master_dict.get, reverse=True)
  for r in a1_sorted_keys:
    print(r, master_dict[r])
  print(' --------------------------------------- ')
  
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  employees_check_category_count_function()
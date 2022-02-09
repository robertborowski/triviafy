# -------------------------------------------------------------- Imports
import json
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import pandas as pd

# -------------------------------------------------------------- Main Function
def job_check_db_status_overall_part_2_redis_to_pandas_df_function():
  localhost_print_function('=========================================== job_check_db_status_overall_part_2_redis_to_pandas_df_function START ===========================================')


  # ------------------------ Upload To Redis START ------------------------
  # Connect to redis database pool (no need to close)
  redis_connection = redis_connect_to_database_function()

  localhost_db_check_dict = 'localhost_db_check_dict'
  value = redis_connection.get(localhost_db_check_dict).decode('utf-8')
  db_check_dict = json.loads(value)
  # ------------------------ Upload To Redis END ------------------------


  # ------------------------ Loop Through Nested Dict START ------------------------
  # Arr initialization
  rows_arr = []
  column_names_row = ['team_id', 'channel_id']

  # Loop through nested dict creating row by row
  for k_team_id, v_inner_dict in db_check_dict.items():
    row = []
    row.append(k_team_id)
    for k_channel_id, v_inner_dict2 in v_inner_dict.items():
      row.append(k_channel_id)
      for k_column_name, v_column_value in v_inner_dict2.items():
        if k_column_name not in column_names_row:
          column_names_row.append(k_column_name)
        row.append(v_column_value)
        # print(f'{k_team_id} | {k_channel_id} | {k_column_name} | {v_column_value}')
      rows_arr.append(row)
    # print('- - - - - - - - - - - - -')

  # Create the pandas DataFrame
  df = pd.DataFrame(rows_arr, columns = column_names_row)
  # print(df)
  
  # Create desktop Excel file
  # df.to_excel(r'/Users/robert/desktop/test.xlsx', index = True)
  # ------------------------ Loop Through Nested Dict END ------------------------



  localhost_print_function('=========================================== job_check_db_status_overall_part_2_redis_to_pandas_df_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  job_check_db_status_overall_part_2_redis_to_pandas_df_function()
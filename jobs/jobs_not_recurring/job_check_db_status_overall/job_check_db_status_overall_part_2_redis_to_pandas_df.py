# -------------------------------------------------------------- Imports
import json
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

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


  # ------------------------ Dict Keys START ------------------------
  all_team_ids = db_check_dict.keys()
  print(all_team_ids)
  # ------------------------ Dict Keys END ------------------------



  # ------------------------ Loop Through Nested Dict START ------------------------
  for k_team_id, v_inner_dict in db_check_dict.items():
    for k_channel_id, v_inner_dict2 in v_inner_dict.items():
      for k_column_name, v_column_value in v_inner_dict2.items():
        print(f'{k_team_id} | {k_channel_id} | {k_column_name} | {v_column_value}')
    print('- - - - - - - - - - - - -')
  # ------------------------ Loop Through Nested Dict END ------------------------


  localhost_print_function('=========================================== job_check_db_status_overall_part_2_redis_to_pandas_df_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  job_check_db_status_overall_part_2_redis_to_pandas_df_function()
# -------------------------------------------------------------- Imports
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
import json
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_team_channel_combos import select_triviafy_user_login_information_table_slack_all_team_channel_combos_function

# -------------------------------------------------------------- Main Function
def job_testing_redis_specific_key_function():
  localhost_print_function('=========================================== job_testing_redis_specific_key_function START ===========================================')


  # ------------------------ Redis Delete START ------------------------
  # Connect to redis database pool (no need to close) 
  redis_connection = redis_connect_to_database_function()
  redis_keys = redis_connection.keys()

  counter = 0
  for key in redis_keys:
    if 'user-slack_' in str(key):
      # redis_connection.delete(key)
      localhost_print_function('Redis Key: {}'.format(key))
      counter += 1
  localhost_print_function(counter)
  # ------------------------ Redis Delete END ------------------------

  localhost_print_function('=========================================== job_testing_redis_specific_key_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  job_testing_redis_specific_key_function()
# -------------------------------------------------------------- Imports
import json
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function

# -------------------------------------------------------------- Main Function
def job_testing_redis_specific_key_function():
  localhost_print_function('=========================================== job_testing_redis_specific_key_function START ===========================================')


  # ------------------------ Redis Delete START ------------------------
  # Connect to redis database pool (no need to close) 
  redis_connection = redis_connect_to_database_function()
  redis_keys = redis_connection.keys()

  counter = 0
  for key in redis_keys:    
    # ------------------------ Set/Get/Delete Local Host START ------------------------
    if 'verify' in str(key):
      localhost_print_function('Redis Key: {}'.format(key))
      redis_value = redis_connection.get(key).decode('utf-8')
      localhost_print_function('Redis Value: {}'.format(redis_value))
      counter += 1
      # redis_connection.delete(key)
      print('- - -')
    # ------------------------ Set/Get/Delete Local Host END ------------------------
  
  localhost_print_function(counter)
  # ------------------------ Redis Delete END ------------------------

  localhost_print_function('=========================================== job_testing_redis_specific_key_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  job_testing_redis_specific_key_function()
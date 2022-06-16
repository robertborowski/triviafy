# -------------------------------------------------------------- Imports
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
import json
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_team_channel_combos import select_triviafy_user_login_information_table_slack_all_team_channel_combos_function

# -------------------------------------------------------------- Main Function
def job_clean_out_unused_redis_browser_keys_function():
  localhost_print_function('=========================================== job_clean_out_unused_redis_browser_keys_function START ===========================================')

  # ------------------------ DB Conection START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ DB Conection End ------------------------


  # ------------------------ Get Distinct Team Channel Combo START ------------------------
  team_channel_arr = select_triviafy_user_login_information_table_slack_all_team_channel_combos_function(postgres_connection, postgres_cursor)
  
  team_id_set = {''}
  channel_id_set = {''}

  for i in team_channel_arr:
    team_id = i[0]
    channel_id = i[1]
    if team_id not in team_id_set:
      team_id_set.add(team_id)
    if channel_id not in channel_id_set:
      channel_id_set.add(channel_id)
  
  team_id_set.remove('')
  channel_id_set.remove('')
  # ------------------------ Get Distinct Team Channel Combo END ------------------------  


  # ------------------------ DB Close Conection START ------------------------
  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ DB Close Conection END ------------------------


  # ------------------------ Redis Delete START ------------------------
  # Connect to redis database pool (no need to close)
  redis_connection = redis_connect_to_database_function()
  redis_keys = redis_connection.keys()

  counter = 0
  for key in redis_keys:
    if 'aa_foo' in str(key) or 'localhost_' in str(key):
      localhost_print_function('skipping key: {}'.format(key))
      continue
    elif 'user-slack_' in str(key):
      redis_connection.delete(key)
      redis_user_email = user_nested_dict['user_email']
      localhost_print_function('deleted logged in user from Redis. Email: {}'.format(redis_user_email))
    else:
      value = redis_connection.get(key).decode('utf-8')
      user_nested_dict = json.loads(value)
      redis_slack_team_id = user_nested_dict['user_slack_workspace_team_id']
      redis_slack_channel_id = user_nested_dict['user_slack_channel_id']
      redis_user_email = user_nested_dict['user_email']
      # ------------------------ Keep Commented Out START ------------------------
      # # Delete specific Email - Keep it commented out
      # if redis_user_email == 'abc@xyz.com':
      #   redis_connection.delete(key)
      #   localhost_print_function('deleted specific email logged in user from Redis. Email: {}'.format(redis_user_email))
      #   counter += 1
      #   localhost_print_function(counter)
      # ------------------------ Keep Commented Out END ------------------------
      if redis_slack_team_id not in team_id_set and redis_slack_channel_id not in channel_id_set:
        redis_connection.delete(key)
        localhost_print_function('deleted logged in user from Redis. Email: {}'.format(redis_user_email))
        counter += 1
        localhost_print_function(counter)
  # ------------------------ Redis Delete END ------------------------

  localhost_print_function('=========================================== job_clean_out_unused_redis_browser_keys_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  job_clean_out_unused_redis_browser_keys_function()
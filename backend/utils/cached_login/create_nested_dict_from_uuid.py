# -------------------------------------------------------------- Imports
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_one_user_uuid import select_one_user_uuid_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_all_column_names import select_all_column_names_function
import json
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.utils.cached_login.check_cookie_browser import check_cookie_browser_function

# -------------------------------------------------------------- Main Function
def create_nested_dict_from_uuid_function(user_uuid):
  localhost_print_function('=========================================== create_nested_dict_from_uuid_function START ===========================================')

  # ------------------------ Connect to Postgres START ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ Connect to Postgres END ------------------------


  # ------------------------ Get Table Columns Info START ------------------------
  table_all_column_names_arr = select_all_column_names_function(postgres_connection, postgres_cursor)
  column_names_match_arr = []
  for i in table_all_column_names_arr:    
    column_names_match_arr.append(i[0])
  # ------------------------ Get Table Columns Info END ------------------------
  
  
  # ------------------------ Loop Match Up Info START ------------------------
  one_specific_user_tuple = select_one_user_uuid_function(postgres_connection, postgres_cursor, user_uuid)
  
  # Nested Dict
  user_nested_dict = {}
  for i in range(len(column_names_match_arr)):
    if column_names_match_arr[i] == 'user_datetime_account_created':
      user_nested_dict[column_names_match_arr[i]] = one_specific_user_tuple[i].strftime("%m/%d/%Y, %H:%M:%S")
    else: 
      user_nested_dict[column_names_match_arr[i]] = one_specific_user_tuple[i]
  # ------------------------ Loop Match Up Info END ------------------------


  # ------------------------ Close Postgres connection START ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Close Postgres connection END ------------------------


  # ------------------------ Get cookie from browser START ------------------------
  get_cookie_value_from_browser = check_cookie_browser_function()
  # ------------------------ Get cookie from browser END ------------------------

  
  # ------------------------ Connect to Redis START ------------------------
  redis_connection = redis_connect_to_database_function()
  redis_connection.set(get_cookie_value_from_browser, json.dumps(user_nested_dict).encode('utf-8'))
  # ------------------------ Connect to Redis END ------------------------
  
  localhost_print_function(' ---------- 0 ---------- ')
  localhost_print_function('REDIS UPDATED!')
  localhost_print_function('- - -')
  localhost_print_function('user_nested_dict')
  localhost_print_function(user_nested_dict)
  localhost_print_function(type(user_nested_dict))
  localhost_print_function(' ---------- 0 ---------- ')

  localhost_print_function('=========================================== create_nested_dict_from_uuid_function END ===========================================')
  return user_nested_dict
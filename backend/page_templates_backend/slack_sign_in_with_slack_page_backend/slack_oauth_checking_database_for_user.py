# -------------------------------------------------------------- Imports
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_if_slack_user_authed_id_exists import select_if_slack_user_authed_id_exists_function
from backend.utils.cached_login.create_nested_dict_from_uuid import create_nested_dict_from_uuid_function

# -------------------------------------------------------------- Main Function
def slack_oauth_checking_database_for_user_function(response_authed_user_id):
  localhost_print_function('=========================================== slack_oauth_checking_database_for_user_function START ===========================================')

  # ------------------------ Connect to Postgres START ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ Connect to Postgres END ------------------------

  # Get user login info from db
  user_db_object = select_if_slack_user_authed_id_exists_function(postgres_connection, postgres_cursor, response_authed_user_id)

  # If user does not exist in db
  if user_db_object == None:
    authed_user_id_already_exists = False
    authed_user_id_signed_in_object = None
  # If user does exist in db
  else:
    user_uuid = user_db_object[0]
    user_nested_dict = create_nested_dict_from_uuid_function(user_uuid)
    authed_user_id_already_exists = True
    authed_user_id_signed_in_object = user_nested_dict


  # ------------------------ Close Postgres connection START ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Close Postgres connection END ------------------------

  localhost_print_function('=========================================== slack_oauth_checking_database_for_user_function END ===========================================')
  return authed_user_id_already_exists, authed_user_id_signed_in_object
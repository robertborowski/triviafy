# -------------------------------------------------------------- Imports
from flask import Blueprint, redirect, request, session
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
import os
from slack_sdk import WebClient
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.page_templates_backend.slack_confirm_oauth_redirect_dashboard_backend.update_db_new_user_store_obj_redis_cookie import update_db_new_user_store_obj_redis_cookie_function
from backend.page_templates_backend.slack_confirm_oauth_redirect_dashboard_backend.user_store_loggedin_data_redis import user_store_loggedin_data_redis_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import time

# -------------------------------------------------------------- App Setup
slack_confirm_oauth_redirect_dashboard_index = Blueprint("slack_confirm_oauth_redirect_dashboard_index", __name__, static_folder="static", template_folder="templates")
@slack_confirm_oauth_redirect_dashboard_index.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@slack_confirm_oauth_redirect_dashboard_index.route("/slack/confirm/oauth/redirect/dashboard/index", methods=['GET','POST'])
def slack_confirm_oauth_redirect_dashboard_index_function():
  localhost_print_function('=========================================== /slack/confirm/oauth/redirect/dashboard/index Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  # ------------------------ Check Server Running START ------------------------
  # -------------------------------------------------------------- Running on localhost
  server_env = os.environ.get('TESTING', 'false')
  # If running on localhost
  if server_env == 'true':
    # Connect to redis database pool (no need to close)
    redis_connection = redis_connect_to_database_function()

    # Get key:value from redis
    localhost_slack_state_key = 'localhost_slack_state_key'
    slack_state_value_passed_in_url = redis_connection.get(localhost_slack_state_key).decode('utf-8')

    # Get key:value from redis
    localhost_redis_browser_cookie_key = 'localhost_redis_browser_cookie_key'
    get_cookie_value_from_browser = redis_connection.get(localhost_redis_browser_cookie_key).decode('utf-8')

  # -------------------------------------------------------------- NOT running on localhost
  else:
    slack_state_value_passed_in_url = session['slack_state_uuid_value']
    get_cookie_value_from_browser = request.cookies.get('triviafy_browser_cookie')
  # ------------------------ Check Server Running END ------------------------


  # ------------------------ Slack Authentication START ------------------------
  # Set up client
  slack_bot_token = os.environ.get('SLACK_BOT_TOKEN')
  client = WebClient(token=slack_bot_token)
  # My Slack Client ID and Client Secret for authentication
  my_slack_client_id = os.environ.get('SLACK_CLIENT_ID')
  my_slack_client_secret = os.environ.get('SLACK_CLIENT_SECRET')
  # Get info from the received URL from Slack once user accepts
  auth_code_received = request.args['code']
  state_received = request.args['state']
  
  # Authorize slack app for user
  if state_received == slack_state_value_passed_in_url:
    try:
      # Slack authentication method, get response object
      authed_response_obj = client.oauth_v2_access(
        client_id = my_slack_client_id,
        client_secret = my_slack_client_secret,
        code = auth_code_received
      )
      # With the response object, update the postgres database for user
      # ------------------------ Update Postgres DB - START ------------------------
      user_nested_dict = None
      user_nested_dict = update_db_new_user_store_obj_redis_cookie_function(client, authed_response_obj)
      time.sleep(2)
      # ------------------------ Update Postgres DB - END ------------------------
      
      # if user_nested_dict != None:
      #   # ------------------------ Update Redis DB - START ------------------------
      #   user_store_in_redis_status = user_store_loggedin_data_redis_function(user_nested_dict, get_cookie_value_from_browser)
      #   localhost_print_function(user_store_in_redis_status)
      #   # ------------------------ Update Redis DB - END ------------------------
      #   time.sleep(2)
    
    except:
      # Try using time.sleep before this step
      print('- - - - - - - - -')
      print('- - - - - - - - -')
      print('- - - - - - - - -')
      print('Error while running "slack_receive_http_oauth_user" script.')
      print('- - - - - - - - -')
      print('- - - - - - - - -')
      print('- - - - - - - - -')
      return redirect("/dashboard", code=302)
    # ------------------------ Slack Authentication END ------------------------


  localhost_print_function('=========================================== /slack/confirm/oauth/redirect/dashboard/index Page END ===========================================')
  # Render the login page template, pass in the redis nested dict of all user info
  return redirect("/dashboard", code=302)
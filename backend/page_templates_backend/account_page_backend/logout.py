from flask import Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
import os

logout = Blueprint("logout", __name__, static_folder="static", template_folder="templates")

@logout.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

@logout.route("/employees/logout", methods=['GET','POST'])
def logout_function():
  print('=========================================== /employees/logout Page START ===========================================')
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')

  # Connect to redis database pool (no need to close)
  redis_connection = redis_connect_to_database_function()

  # -------------------------------------------------------------- Running on localhost
  server_env = os.environ.get('TESTING', 'false')
  # If running on localhost
  if server_env == 'true':
    try:
      # Get key:value from redis then delete row from redis
      redis_browser_cookie_key = 'localhost_redis_browser_cookie_key'
      browser_cookie_value = redis_connection.get(redis_browser_cookie_key).decode('utf-8')
      redis_connection.delete(redis_browser_cookie_key)
      redis_connection.delete(browser_cookie_value)
    except:
      print('=========================================== /employees/logout Page END ===========================================')
      return redirect("/", code=302)

  # -------------------------------------------------------------- NOT running on localhost
  else:
    get_cookie_value_from_browser = request.cookies.get('triviafy_browser_cookie')
    try:
      redis_connection.delete(get_cookie_value_from_browser)
    except:
      print('=========================================== /employees/logout Page END ===========================================')
      return redirect("/", code=302)

  print('=========================================== /employees/logout Page END ===========================================')
  return redirect("/", code=302)
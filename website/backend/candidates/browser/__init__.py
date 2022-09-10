
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_set_browser_cookie_function, redis_connect_to_database_function
from flask import Blueprint, render_template, request, make_response
import datetime
# ------------------------ imports end ------------------------


# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------


localhost_print_function('=========================================== browser __init__ START ===========================================')
# ------------------------ individual function start ------------------------
def browser_response_set_cookie_function(current_user, input_template_url):
  localhost_print_function('=========================================== browser_response_set_cookie_function START ===========================================')
  set_browser_cookie_key, set_browser_cookie_value = redis_set_browser_cookie_function()
  browser_response = make_response(render_template(input_template_url, user=current_user, users_name_to_html=current_user.first_name))
  browser_response.set_cookie(set_browser_cookie_key, set_browser_cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=60))
  redis_connection.set(set_browser_cookie_value, current_user.id.encode('utf-8'))
  localhost_print_function('=========================================== browser_response_set_cookie_function END ===========================================')
  return browser_response
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== browser __init__ END ===========================================')
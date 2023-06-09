
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_set_browser_cookie_function, redis_set_employees_browser_cookie_function, redis_connect_to_database_function
from flask import Blueprint, render_template, request, make_response
import datetime
# ------------------------ imports end ------------------------

# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual function start ------------------------
def browser_response_set_cookie_function(current_user, input_template_url):
  set_browser_cookie_key, set_browser_cookie_value = redis_set_browser_cookie_function()
  browser_response = make_response(render_template(input_template_url, user=current_user))
  browser_response.set_cookie(set_browser_cookie_key, set_browser_cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=60))
  redis_connection.set(set_browser_cookie_value, current_user.id.encode('utf-8'))
  return browser_response
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def browser_response_set_cookie_function_v2(input_template_location_url, input_current_user, input_current_user_company, input_error_message_to_html, input_candidate_categories_arr_to_html, page_dict):
  set_browser_cookie_key, set_browser_cookie_value = redis_set_browser_cookie_function()
  browser_response = make_response(render_template(input_template_location_url, user=input_current_user, users_company_name_to_html=input_current_user_company, error_message_to_html=input_error_message_to_html, candidate_categories_arr_to_html=input_candidate_categories_arr_to_html, page_dict_to_html=page_dict))
  browser_response.set_cookie(set_browser_cookie_key, set_browser_cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=60))
  redis_connection.set(set_browser_cookie_value, input_current_user.id.encode('utf-8'))
  return browser_response
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def browser_response_set_cookie_function_v3(current_user, input_template_url):
  set_browser_cookie_key, set_browser_cookie_value = redis_set_employees_browser_cookie_function()
  browser_response = make_response(render_template(input_template_url, user=current_user))
  browser_response.set_cookie(set_browser_cookie_key, set_browser_cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=60))
  redis_connection.set(set_browser_cookie_value, current_user.id.encode('utf-8'))
  return browser_response
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def browser_response_set_cookie_function_v4(current_user, input_template_url, alert_message_dict, page_dict):
  set_browser_cookie_key, set_browser_cookie_value = redis_set_browser_cookie_function()
  browser_response = make_response(render_template(input_template_url, user=current_user, alert_message_dict_to_html=alert_message_dict, page_dict_to_html=page_dict))
  browser_response.set_cookie(set_browser_cookie_key, set_browser_cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=60))
  redis_connection.set(set_browser_cookie_value, current_user.id.encode('utf-8'))
  return browser_response
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def browser_response_set_cookie_function_v5(current_user, input_template_url, page_dict):
  set_browser_cookie_key, set_browser_cookie_value = redis_set_browser_cookie_function()
  browser_response = make_response(render_template(input_template_url, page_dict_to_html=page_dict))
  browser_response.set_cookie(set_browser_cookie_key, set_browser_cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=60))
  redis_connection.set(set_browser_cookie_value, current_user.id.encode('utf-8'))
  return browser_response
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def browser_response_set_cookie_function_v6(current_user, input_template_url, page_dict):
  set_browser_cookie_key, set_browser_cookie_value = redis_set_browser_cookie_function()
  browser_response = make_response(render_template(input_template_url, user=current_user, page_dict_to_html=page_dict))
  browser_response.set_cookie(set_browser_cookie_key, set_browser_cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=60))
  redis_connection.set(set_browser_cookie_value, current_user.id.encode('utf-8'))
  return browser_response
# ------------------------ individual function end ------------------------
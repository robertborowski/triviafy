# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -Note: any pages related to authentication will not be in this file, they will be routed in the auth.py file.
# -@login_required   # this decorator says that url cannot be accessed unless the user is logged in. 
# -@login_required: <-- This decorator will bring a user to __init__ code: [login_manager.login_view = 'auth.candidates_login_page_function'] if they hit a page that requires login and they are not logged in.
# -use code: <methods=['GET', 'POST']> when you want the user to interact with the page through forms/checkbox/textbox/radio/etc.
# ------------------------ info about this file end ------------------------

# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from website import db
from website.backend.candidates.user_inputs import alert_message_default_function_v2
from website.backend.candidates.browser import browser_response_set_cookie_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
employees_views_interior = Blueprint('employees_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/dashboard')
@employees_views_interior.route('/employees/dashboard/<url_redirect_code>')
@login_required
def login_dashboard_page_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ login_dashboard_page_function START ------------------------ ')
  # ------------------------ auto redirect checks start ------------------------
  """
  -The code will always hit this dashboard on login or create account. BUT BEFORE setting the cookie on the browser, we are going to auto redirect
  users this makes the UX better so they dont have to click, read, or think, just auto redirect. The downside is that you cannot set the cookie
  unless you know for sure where the user is ending up. So the redirected page will ALSO have to include the function that sets the cookie.
  Downside is repeating code but it is not for all pages, only for the pages that auto redirect on new account creation.
  -These pages will require the template_location_url variable
  """
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'employees/interior/dashboard/index.html'
  # ------------------------ for setting cookie end ------------------------
  # ------------------------ redirect codes start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  # ------------------------ redirect codes end ------------------------
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, alert_message_dict_to_html=alert_message_dict)
  else:
    browser_response = browser_response_set_cookie_function(current_user, template_location_url)
    localhost_print_function(' ------------------------ login_dashboard_page_function END ------------------------ ')
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------
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
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_user
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from website.models import CandidatesUserObj
from website.backend.candidates.browser import browser_response_set_cookie_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
# ------------------------ imports end ------------------------


# ------------------------ function start ------------------------
views = Blueprint('views', __name__)
# ------------------------ function end ------------------------
# ------------------------ before page variables start ------------------------
cache_busting_output = create_uuid_function('css_')
# ------------------------ before page variables end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ routes not logged in start ------------------------
# ------------------------ individual route - candidates about start ------------------------
@views.route('/candidates/about')
def candidates_about_page_function():
  localhost_print_function('=========================================== candidates_about_page_function START ===========================================')
  # ------------------------ auto sign in with cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    try:
      user_id_from_redis = redis_connection.get(get_cookie_value_from_browser).decode('utf-8')
      if user_id_from_redis != None:
        user = CandidatesUserObj.query.filter_by(id=user_id_from_redis).first()
        # ------------------------ keep user logged in start ------------------------
        login_user(user, remember=True)
        # ------------------------ keep user logged in end ------------------------
        localhost_print_function('redirecting to logged in page')
        return redirect(url_for('views.dashboard_test_login_page_function'))
    except:
      pass
  # ------------------------ auto sign in with cookie end ------------------------
  localhost_print_function('=========================================== candidates_about_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/about_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates about end ------------------------

# ------------------------ individual route - candidates faq start ------------------------
@views.route('/candidates/faq')
def candidates_faq_page_function():
  localhost_print_function('=========================================== candidates_faq_page_function START ===========================================')
  # ------------------------ auto sign in with cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    try:
      user_id_from_redis = redis_connection.get(get_cookie_value_from_browser).decode('utf-8')
      if user_id_from_redis != None:
        user = CandidatesUserObj.query.filter_by(id=user_id_from_redis).first()
        # ------------------------ keep user logged in start ------------------------
        login_user(user, remember=True)
        # ------------------------ keep user logged in end ------------------------
        localhost_print_function('redirecting to logged in page')
        return redirect(url_for('views.dashboard_test_login_page_function'))
    except:
      pass
  # ------------------------ auto sign in with cookie end ------------------------
  localhost_print_function('=========================================== candidates_faq_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/faq_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates faq end ------------------------

# ------------------------ individual route - candidates index main start ------------------------
@views.route('/candidates')
def landing_index_page_function():
  localhost_print_function('=========================================== landing_index_page_function START ===========================================')
  # ------------------------ auto sign in with cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    try:
      user_id_from_redis = redis_connection.get(get_cookie_value_from_browser).decode('utf-8')
      if user_id_from_redis != None:
        user = CandidatesUserObj.query.filter_by(id=user_id_from_redis).first()
        # ------------------------ keep user logged in start ------------------------
        login_user(user, remember=True)
        # ------------------------ keep user logged in end ------------------------
        localhost_print_function('redirecting to logged in page')
        return redirect(url_for('views.dashboard_test_login_page_function'))
    except:
      pass
  # ------------------------ auto sign in with cookie end ------------------------
  localhost_print_function('=========================================== landing_index_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/index_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates index main end ------------------------

# ------------------------ individual route - candidates test library start ------------------------
@views.route('/candidates/library')
def candidates_test_library_page_function():
  localhost_print_function('=========================================== candidates_test_library_page_function START ===========================================')
  # ------------------------ auto sign in with cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    try:
      user_id_from_redis = redis_connection.get(get_cookie_value_from_browser).decode('utf-8')
      if user_id_from_redis != None:
        user = CandidatesUserObj.query.filter_by(id=user_id_from_redis).first()
        # ------------------------ keep user logged in start ------------------------
        login_user(user, remember=True)
        # ------------------------ keep user logged in end ------------------------
        localhost_print_function('redirecting to logged in page')
        return redirect(url_for('views.dashboard_test_login_page_function'))
    except:
      pass
  # ------------------------ auto sign in with cookie end ------------------------
  localhost_print_function('=========================================== candidates_test_library_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/test_library_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates test library end ------------------------

# ------------------------ individual route - candidates pricing start ------------------------
@views.route('/candidates/pricing')
def candidates_pricing_page_function():
  localhost_print_function('=========================================== candidates_pricing_page_function START ===========================================')
  # ------------------------ auto sign in with cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    try:
      user_id_from_redis = redis_connection.get(get_cookie_value_from_browser).decode('utf-8')
      if user_id_from_redis != None:
        user = CandidatesUserObj.query.filter_by(id=user_id_from_redis).first()
        # ------------------------ keep user logged in start ------------------------
        login_user(user, remember=True)
        # ------------------------ keep user logged in end ------------------------
        localhost_print_function('redirecting to logged in page')
        return redirect(url_for('views.dashboard_test_login_page_function'))
    except:
      pass
  # ------------------------ auto sign in with cookie end ------------------------
  localhost_print_function('=========================================== candidates_pricing_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/pricing_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates pricing end ------------------------

# ------------------------ individual route - candidates stand in start ------------------------
@views.route('/candidates/launch')
def candidates_stand_in_page_function():
  localhost_print_function('=========================================== candidates_stand_in_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_stand_in_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/stand_in_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates stand in end ------------------------

# ------------------------ individual route - candidates collect email start ------------------------
@views.route('/candidates/email')
def candidates_email_page_function():
  localhost_print_function('=========================================== candidates_email_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_email_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/collect_email_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates collect email end ------------------------

# ------------------------ individual route - error 404 start ------------------------
@views.route('/404')
def error_page_function():
  localhost_print_function('=========================================== error_page_function START ===========================================')
  localhost_print_function('=========================================== error_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/error_404_page_templates/index.html', user=current_user)
# ------------------------ individual route - error 404 end ------------------------

# ------------------------ individual route - privacy start ------------------------
@views.route('/privacy')
def privacy_page_function():
  localhost_print_function('=========================================== privacy_page_function START ===========================================')
  localhost_print_function('=========================================== privacy_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/privacy_policy_page_templates/index.html', user=current_user)
# ------------------------ individual route - privacy end ------------------------

# ------------------------ individual route - privacy start ------------------------
@views.route('/tos')
def terms_of_service_page_function():
  localhost_print_function('=========================================== terms_of_service_page_function START ===========================================')
  localhost_print_function('=========================================== terms_of_service_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/terms_of_service_page_templates/index.html', user=current_user)
# ------------------------ individual route - privacy end ------------------------
# ------------------------ routes not logged in end ------------------------



# ------------------------ routes logged in start ------------------------
# @login_required should be a decorator on all of the pages in this section
# ------------------------ individual route start ------------------------
# ------------------------ individual route start ------------------------
@views.route('/candidates/dashboard')
@login_required
def dashboard_test_login_page_function():
  localhost_print_function('=========================================== dashboard_test_login_page_function START ===========================================')
  # ------------------------ auto redirect checks start ------------------------
  """
  -The code will always hit this dashboard on login or create account. BUT BEFORE setting the cookie on the browser, we are going to auto redirect
  users this makes the UX better so they dont have to click, read, or think, just auto redirect. The downside is that you cannot set the cookie
  unless you know for sure where the user is ending up. So the redirected page will ALSO have to include the function that sets the cookie.
  Downside is repeating code but it is not for all pages, only for the pages that auto redirect on new account creation.
  -These pages will require the template_location_url variable
  """
  template_location_url = 'candidates_page_templates/logged_in_page_templates/dashboard_page_templates/dashboard_test_login_page_templates/index.html'
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('redirecting user to capacity selection page')
    localhost_print_function('=========================================== dashboard_test_login_page_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ auto redirect checks end ------------------------
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, users_name_to_html=current_user.first_name)
  else:
    browser_response = browser_response_set_cookie_function(current_user, template_location_url)
    localhost_print_function('=========================================== dashboard_test_login_page_function END ===========================================')
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------


# ------------------------ individual route start ------------------------
@views.route('/candidates/capacity')
@login_required
def capacity_page_function():
  localhost_print_function('=========================================== capacity_page_function START ===========================================')
  # ------------------------ auto redirect checks start ------------------------
  template_location_url = 'candidates_page_templates/logged_in_page_templates/select_candidates_per_month_page_templates/index.html'
  # ------------------------ auto redirect checks end ------------------------
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, users_name_to_html=current_user.first_name)
  else:
    browser_response = browser_response_set_cookie_function(current_user, template_location_url)
    localhost_print_function('=========================================== capacity_page_function END ===========================================')
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------
# ------------------------ routes logged in end ------------------------
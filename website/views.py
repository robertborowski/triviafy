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
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user, login_user
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from website.models import CandidatesUserObj, CandidatesDesiredLanguagesObj
from website.backend.candidates.browser import browser_response_set_cookie_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.backend.candidates.datatype_conversion_manipulation import one_col_dict_to_arr_function
from website import db
from website.backend.candidates.user_inputs import sanitize_email_function, sanitize_password_function, sanitize_create_account_text_inputs_function
from website.backend.candidates.send_emails import send_email_template_function
from werkzeug.security import generate_password_hash
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
  localhost_print_function('=========================================== candidates_about_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/about_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates about end ------------------------

# ------------------------ individual route - candidates faq start ------------------------
@views.route('/candidates/faq')
def candidates_faq_page_function():
  localhost_print_function('=========================================== candidates_faq_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_faq_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/faq_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates faq end ------------------------

# ------------------------ individual route - candidates index main start ------------------------
@views.route('/candidates')
def landing_index_page_function():
  localhost_print_function('=========================================== landing_index_page_function START ===========================================')
  localhost_print_function('=========================================== landing_index_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/index_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates index main end ------------------------

# ------------------------ individual route - candidates test library start ------------------------
@views.route('/candidates/library')
def candidates_test_library_page_function():
  localhost_print_function('=========================================== candidates_test_library_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_test_library_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/test_library_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates test library end ------------------------

# ------------------------ individual route - candidates pricing start ------------------------
@views.route('/candidates/pricing')
def candidates_pricing_page_function():
  localhost_print_function('=========================================== candidates_pricing_page_function START ===========================================')
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

# ------------------------ individual route - candidates about start ------------------------
@views.route('/candidates/reset', methods=['GET', 'POST'])
def candidates_forgot_password_page_function():
  localhost_print_function('=========================================== candidates_forgot_password_page_function START ===========================================')  
  forgot_password_error_statement = ''
  if request.method == 'POST':
    # ------------------------ post request sent start ------------------------
    ui_email = request.form.get('forgot_password_page_ui_email')
    # ------------------------ post request sent end ------------------------
    # ------------------------ sanitize/check user input email start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email)
    if ui_email_cleaned == False:
      forgot_password_error_statement = 'Please enter a valid work email.'
    # ------------------------ sanitize/check user input email end ------------------------
    # ------------------------ check if user email exists in db start ------------------------
    user_exists = CandidatesUserObj.query.filter_by(email=ui_email).first()
    if user_exists:
      forgot_password_error_statement = 'Password reset link sent to email.'
      # ------------------------ send email with token url start ------------------------
      serializer_token_obj = CandidatesUserObj.get_reset_token_function(self=user_exists)
      output_email = ui_email
      output_subject_line = 'Password Reset - Triviafy'
      output_message_content = f"To reset your password, visit the following link: https://triviafy.com/candidates/reset/{serializer_token_obj} \n\nThis link will expire after 30 minutes.\nIf you did not make this request then simply ignore this email and no changes will be made."
      send_email_template_function(output_email, output_subject_line, output_message_content)
      # ------------------------ send email with token url end ------------------------
    else:
      forgot_password_error_statement = 'Password reset link sent to email.'
      pass
    # ------------------------ check if user email exists in db end ------------------------
  localhost_print_function('=========================================== candidates_forgot_password_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/forgot_password_page_templates/index.html', user=current_user, error_message_to_html = forgot_password_error_statement)
# ------------------------ individual route - candidates about end ------------------------


# ------------------------ individual route - candidates about start ------------------------
@views.route('/candidates/reset/<token>', methods=['GET', 'POST'])
def candidates_reset_forgot_password_page_function(token):
  localhost_print_function('=========================================== candidates_reset_forgot_password_page_function START ===========================================')
  if current_user.is_authenticated:
    return redirect(url_for('views.candidates_pricing_page_function'))
  reset_password_error_statement = ''
  user_obj_from_token = CandidatesUserObj.verify_reset_token_function(token)
  if user_obj_from_token is None:
    reset_password_error_statement = 'That is an invalid or expired token'
    localhost_print_function('=========================================== candidates_reset_forgot_password_page_function END ===========================================')
    return render_template('candidates_page_templates/not_logged_in_page_templates/forgot_password_page_templates/index.html', user=current_user, error_message_to_html = reset_password_error_statement)
  if request.method == 'POST':
    reset_password_error_statement = ''
    # ------------------------ get inputs from form start ------------------------
    ui_password = request.form.get('reset_forgot_password_page_ui_password')
    ui_password_confirmed = request.form.get('reset_forgot_password_page_ui_password_confirmed')
    # ------------------------ get inputs from form end ------------------------
    # ------------------------ check match start ------------------------
    if ui_password != ui_password_confirmed:
      reset_password_error_statement = 'Passwords do not match.'
    # ------------------------ check match end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_cleaned = sanitize_password_function(ui_password)
    if ui_password_cleaned == False:
      reset_password_error_statement = 'Password is not valid.'
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_confirmed_cleaned = sanitize_password_function(ui_password_confirmed)
    if ui_password_confirmed_cleaned == False:
      reset_password_error_statement = 'Password is not valid.'
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ update db start ------------------------
    if reset_password_error_statement == '':
      user_obj_from_token.password = generate_password_hash(ui_password, method="sha256")
      db.session.commit()
      return redirect(url_for('views.dashboard_test_login_page_function'))
    # ------------------------ update db end ------------------------
  localhost_print_function('=========================================== candidates_reset_forgot_password_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/forgot_password_page_templates/reset_forgot_password_page_templates/index.html', user=current_user, error_message_to_html = reset_password_error_statement)
# ------------------------ individual route - candidates about end ------------------------
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
  template_location_url = 'candidates_page_templates/logged_in_page_templates/dashboard_page_templates/index.html'
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== dashboard_test_login_page_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== dashboard_test_login_page_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ auto redirect checks end ------------------------
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, users_company_name_to_html=current_user.company_name)
  else:
    browser_response = browser_response_set_cookie_function(current_user, template_location_url)
    localhost_print_function('=========================================== dashboard_test_login_page_function END ===========================================')
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------


# ------------------------ individual route start ------------------------
@views.route('/candidates/capacity', methods=['GET', 'POST'])
@login_required
def capacity_page_function():
  localhost_print_function('=========================================== capacity_page_function START ===========================================')
  # ------------------------ capacity selection start ------------------------
  if request.method == 'POST':
    ui_capacity_selected = request.form.get('capacity_page_ui_capacity_selected')
    ui_desired_languages = request.form.get('capacity_page_ui_desired_languages')
    # ------------------------ postman checks start ------------------------
    try:
      if len(ui_capacity_selected) != 2:
        ui_capacity_selected = None
    except:
      ui_capacity_selected = None
    # ------------------------ postman checks end ------------------------
    # ------------------------ valid input check start ------------------------
    query_result_arr_of_dicts = select_general_function('select_all_capacity_options')
    capacity_options_arr = one_col_dict_to_arr_function(query_result_arr_of_dicts)
    if ui_capacity_selected not in capacity_options_arr:
      ui_capacity_selected = None
    # ------------------------ valid input check end ------------------------
    # ------------------------ sanitize/check ui_desired_languages start ------------------------
    if len(ui_desired_languages) > 20:
      ui_desired_languages = None
    ui_desired_languages_cleaned = sanitize_create_account_text_inputs_function(ui_desired_languages)
    if ui_desired_languages_cleaned == False:
      ui_desired_languages = None
    # ------------------------ sanitize/check ui_desired_languages end ------------------------
    # ------------------------ update db start ------------------------
    if ui_capacity_selected != None and ui_desired_languages != None:
      current_user.capacity_id_fk = ui_capacity_selected
      db.session.commit()
      # ------------------------ create new user in db start ------------------------
      insert_new_row = CandidatesDesiredLanguagesObj(
        id=create_uuid_function('langs_'),
        created_timestamp=create_timestamp_function(),
        user_id_fk=current_user.id,
        desired_languages=ui_desired_languages
      )
      db.session.add(insert_new_row)
      db.session.commit()
      # ------------------------ create new user in db end ------------------------
      return redirect(url_for('views.dashboard_test_login_page_function'))
    # ------------------------ update db end ------------------------
  # ------------------------ capacity selection end ------------------------
  # ------------------------ auto redirect checks start ------------------------
  template_location_url = 'candidates_page_templates/logged_in_page_templates/capacity_select_page_templates/index.html'
  # ------------------------ auto redirect checks end ------------------------
  # ------------------------ latest_language_selection start ------------------------
  curr_user_id = current_user.id
  try:
    query_result_desired_languages_obj = CandidatesDesiredLanguagesObj.query.filter(CandidatesDesiredLanguagesObj.user_id_fk == curr_user_id).order_by(CandidatesDesiredLanguagesObj.created_timestamp.desc()).first()
    user_id_fk_desired_languages = query_result_desired_languages_obj.desired_languages
  except:
    user_id_fk_desired_languages = None
  # ------------------------ latest_language_selection end ------------------------
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, users_company_name_to_html=current_user.company_name, user_id_fk_desired_languages_to_html = user_id_fk_desired_languages)
  else:
    browser_response = browser_response_set_cookie_function(current_user, template_location_url)
    localhost_print_function('=========================================== capacity_page_function END ===========================================')
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------
# ------------------------ routes logged in end ------------------------
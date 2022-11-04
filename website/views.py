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
from website.models import CandidatesUserObj, CandidatesDesiredLanguagesObj, CandidatesUploadedCandidatesObj, CandidatesAssessmentsCreatedObj, CandidatesRequestLanguageObj, CandidatesScheduleObj, CandidatesEmailSentObj, CandidatesAssessmentGradedObj, CandidatesCapacityOptionsObj, CandidatesStripeCheckoutSessionObj, CandidatesCreatedQuestionsObj
from website.backend.candidates.browser import browser_response_set_cookie_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.backend.candidates.datatype_conversion_manipulation import one_col_dict_to_arr_function
from website import db
from website.backend.candidates.user_inputs import sanitize_email_function, sanitize_password_function, sanitize_create_account_text_inputs_function, sanitize_create_account_text_inputs_large_function, validate_upload_candidate_function, sanitize_loop_check_if_exists_within_arr_function, sanitize_check_if_str_exists_within_arr_function, check_if_question_id_arr_exists_function, sanitize_candidate_ui_answer_text_function
from website.backend.candidates.send_emails import send_email_template_function
from werkzeug.security import generate_password_hash
import pandas as pd
from website.backend.candidates.string_manipulation import all_question_candidate_categories_sorted_function
from website.backend.candidates.sqlalchemy_manipulation import pull_desired_languages_arr_function
from website.backend.candidates.dict_manipulation import question_arr_of_dicts_manipulations_function, create_assessment_info_dict_function, map_user_answers_to_questions_dict_function, backend_store_question_answers_dict_function, grade_assessment_answers_dict_function
from website.backend.candidates.datetime_manipulation import next_x_days_function, times_arr_function, expired_assessment_check_function
import datetime
import json
import stripe
import os
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
# ------------------------ individual route start ------------------------
@views.route('/candidates/about')
def candidates_about_page_function():
  localhost_print_function('=========================================== candidates_about_page_function START ===========================================')  
  localhost_print_function('=========================================== candidates_about_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/about_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/faq')
def candidates_faq_page_function():
  localhost_print_function('=========================================== candidates_faq_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_faq_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/faq_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates')
def landing_index_page_function():
  localhost_print_function('=========================================== landing_index_page_function START ===========================================')
  localhost_print_function('=========================================== landing_index_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/index_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/library')
def candidates_test_library_page_function():
  localhost_print_function('=========================================== candidates_test_library_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_test_library_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/test_library_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/pricing')
def candidates_pricing_page_function():
  localhost_print_function('=========================================== candidates_pricing_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_pricing_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/pricing_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/launch')
def candidates_stand_in_page_function():
  localhost_print_function('=========================================== candidates_stand_in_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_stand_in_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/stand_in_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/email')
def candidates_email_page_function():
  localhost_print_function('=========================================== candidates_email_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_email_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/collect_email_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/404')
def error_page_function():
  localhost_print_function('=========================================== error_page_function START ===========================================')
  localhost_print_function('=========================================== error_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/error_404_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/privacy')
def privacy_page_function():
  localhost_print_function('=========================================== privacy_page_function START ===========================================')
  localhost_print_function('=========================================== privacy_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/privacy_policy_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/tos')
def terms_of_service_page_function():
  localhost_print_function('=========================================== terms_of_service_page_function START ===========================================')
  localhost_print_function('=========================================== terms_of_service_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/terms_of_service_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
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
# ------------------------ individual route end ------------------------


# ------------------------ individual route start ------------------------
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
# ------------------------ individual route end ------------------------
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
  # ------------------------ delete all assessments that have been started by this user so far but abandoned start ------------------------
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr=None).delete()
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr='').delete()
  db.session.commit()
  # ------------------------ delete all assessments that have been started by this user so far but abandoned end ------------------------
  # ------------------------ get users total uploaded candidates start ------------------------
  current_user_uploaded_emails_arr = CandidatesUploadedCandidatesObj.query.filter_by(user_id_fk=current_user.id).all()
  len_current_user_uploaded_emails_arr = len(current_user_uploaded_emails_arr)
  # ------------------------ get users total uploaded candidates end ------------------------
  # ------------------------ get users total assessments created start ------------------------
  current_user_assessments_created_arr = CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id).all()
  len_current_user_assessments_created_arr = len(current_user_assessments_created_arr)
  # ------------------------ get users total assessments created end ------------------------
  # ------------------------ get users total schedules created start ------------------------
  current_user_schedules_created_arr = CandidatesScheduleObj.query.filter_by(user_id_fk=current_user.id).all()
  len_current_user_schedules_created_arr = len(current_user_schedules_created_arr)
  # ------------------------ get users total schedules created end ------------------------
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user = current_user, users_company_name_to_html = current_user.company_name, len_current_user_uploaded_emails_arr_to_html = len_current_user_uploaded_emails_arr, len_current_user_assessments_created_arr_to_html=len_current_user_assessments_created_arr, len_current_user_schedules_created_arr_to_html=len_current_user_schedules_created_arr)
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

# ------------------------ individual route start ------------------------
@views.route('/candidates/subscription/success')
@login_required
def candidates_subscription_success_function():
  localhost_print_function('=========================================== candidates_subscription_success_function START ===========================================')
  # ------------------------ get from db start ------------------------
  db_checkout_session_obj = CandidatesStripeCheckoutSessionObj.query.filter_by(fk_user_id=current_user.id).order_by(CandidatesStripeCheckoutSessionObj.created_timestamp.desc()).first()
  # ------------------------ get from db end ------------------------
  # ------------------------ if not found start ------------------------
  if db_checkout_session_obj == None or db_checkout_session_obj == '' or db_checkout_session_obj == False:
    localhost_print_function('=========================================== candidates_subscription_success_function END ===========================================')
    return redirect(url_for('views.dashboard_test_login_page_function'))
  # ------------------------ if not found end ------------------------
  # ------------------------ get desired start ------------------------
  fk_checkout_session_id = db_checkout_session_obj.fk_checkout_session_id
  # ------------------------ get desired end ------------------------
  # ------------------------ stripe lookup start ------------------------
  stripe_checkout_session_obj = stripe.checkout.Session.retrieve(fk_checkout_session_id)
  # ------------------------ if not found start ------------------------
  if stripe_checkout_session_obj == None:
    localhost_print_function('=========================================== candidates_subscription_success_function END ===========================================')
    return redirect(url_for('views.dashboard_test_login_page_function'))
  # ------------------------ if not found end ------------------------
  stripe_customer_id = stripe_checkout_session_obj.customer
  stripe_subscription_id = stripe_checkout_session_obj.subscription
  # ------------------------ stripe lookup end ------------------------
  # ------------------------ update db start ------------------------
  user_obj = CandidatesUserObj.query.filter_by(id=current_user.id).first()
  user_obj.fk_stripe_customer_id = stripe_customer_id
  user_obj.fk_stripe_subscription_id = stripe_subscription_id
  db.session.commit()
  # ------------------------ update db end ------------------------
  # ------------------------ email self start ------------------------
  try:
    output_to_email = 'robert@triviafy.com'
    output_subject = f'New Subscription - Triviafy Candidates'
    output_body = f"Hi there,\n\nNew user subscribed: {user_obj.email} \n\nBest,\nTriviafy"
    send_email_template_function(output_to_email, output_subject, output_body)
  except:
    pass
  # ------------------------ email self end ------------------------
  localhost_print_function('=========================================== candidates_subscription_success_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/subscription_page_templates/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/account', methods=['GET', 'POST'])
@login_required
def candidates_account_settings_function():
  localhost_print_function('=========================================== candidates_account_settings_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_account_settings_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_account_settings_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ delete all assessments that have been started by this user so far but abandoned start ------------------------
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr=None).delete()
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr='').delete()
  db.session.commit()
  # ------------------------ delete all assessments that have been started by this user so far but abandoned end ------------------------
  # ------------------------ pull user info start ------------------------
  user_account_created_timestamp = current_user.created_timestamp
  user_account_created_str = user_account_created_timestamp.strftime('%m/%Y')
  # ------------------------ pull user info end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  user_obj = CandidatesUserObj.query.filter_by(id=current_user.id).first()
  fk_stripe_subscription_id = user_obj.fk_stripe_subscription_id
  stripe_subscription_obj = ''
  stripe_subscription_obj_status = 'not active'
  stripe_current_period_end_datetime_str = ''
  try:
    # ------------------------ stripe subscription object start ------------------------
    stripe_subscription_obj = stripe.Subscription.retrieve(fk_stripe_subscription_id)
    # ------------------------ stripe subscription object end ------------------------
    stripe_subscription_obj_status = stripe_subscription_obj.status
    stripe_current_period_end_timestamp = stripe_subscription_obj.current_period_end
    stripe_current_period_end_datetime_str = datetime.datetime.utcfromtimestamp(stripe_current_period_end_timestamp).strftime('%m/%d/%Y')
    # ------------------------ get plan name start ------------------------
    stripe_user_subscription_price_id_fk = stripe_subscription_obj.plan.id
    db_capacity_obj = CandidatesCapacityOptionsObj.query.filter_by(fk_stripe_price_id=stripe_user_subscription_price_id_fk).first()
    current_stripe_capacity = db_capacity_obj.id
    user_obj = CandidatesUserObj.query.filter_by(id=current_user.id).first()
    current_users_capacity = user_obj.capacity_id_fk
    if current_users_capacity != current_stripe_capacity:
      # ------------------------ update row in db user start ------------------------
      user_obj.capacity_id_fk = current_stripe_capacity
      db.session.commit()
      # ------------------------ update row in db user end ------------------------
  except:
    pass
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ if subscription not paid start ------------------------
  user_sub_active = False
  if stripe_subscription_obj_status == 'active':
    user_sub_active = True
  # ------------------------ if subscription not paid end ------------------------
  # ------------------------ get plan name start ------------------------
  user_obj = CandidatesUserObj.query.filter_by(id=current_user.id).first()
  user_obj_capacity_id = user_obj.capacity_id_fk
  if user_obj_capacity_id == '1m':
    user_obj_capacity_id = 'Basic'
  if user_obj_capacity_id == '2m':
    user_obj_capacity_id = 'Professional'
  if user_obj_capacity_id == '3m':
    user_obj_capacity_id = 'Premium'
  # ------------------------ get plan name end ------------------------
  # ------------------------ if post data start ------------------------
  if request.method == 'POST':
    ui_capacity_selected = request.form.get('capacity_page_ui_capacity_selected')
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
    # ------------------------ redirect if invalid start ------------------------
    if ui_capacity_selected == None:
      localhost_print_function('=========================================== candidates_account_settings_function END ===========================================')
      return redirect(url_for('views.dashboard_test_login_page_function'))
    # ------------------------ redirect if invalid end ------------------------
    if ui_capacity_selected != None:
      # ------------------------ db get price id start ------------------------
      db_capacity_obj = CandidatesCapacityOptionsObj.query.filter_by(id=ui_capacity_selected).first()
      fk_stripe_price_id = db_capacity_obj.fk_stripe_price_id
      # ------------------------ db get price id end ------------------------
      # ------------------------ stripe checkout start ------------------------
      try:
        checkout_session = stripe.checkout.Session.create(
          line_items=[
            {
            'price': fk_stripe_price_id,
            'quantity': 1,
            },
          ],
          mode='subscription',
          success_url='https://triviafy.com/candidates/subscription/success',
          cancel_url='https://triviafy.com/candidates/account',
          metadata={
            'fk_user_id': current_user.id
          }
        )
        # ------------------------ create db row start ------------------------
        # This is so I can easily get the customer id and subscription id in a future lookup
        checkout_session_id = checkout_session.id
        current_user_id = current_user.id
        new_checkout_session_obj = CandidatesStripeCheckoutSessionObj(
          id = create_uuid_function('checkout_'),
          created_timestamp = create_timestamp_function(),
          fk_checkout_session_id = checkout_session_id,
          fk_user_id = current_user_id
        )
        db.session.add(new_checkout_session_obj)
        db.session.commit()
        # ------------------------ create db row end ------------------------
        # ------------------------ for presentation start ------------------------
        user_obj = CandidatesUserObj.query.filter_by(id=current_user.id).first()
        user_obj_capacity_id = user_obj.capacity_id_fk
        if user_obj_capacity_id == '1m':
          user_obj_capacity_id = 'Basic'
        if user_obj_capacity_id == '2m':
          user_obj_capacity_id = 'Professional'
        if user_obj_capacity_id == '3m':
          user_obj_capacity_id = 'Premium'
        # ------------------------ for presentation end ------------------------
      except Exception as e:
        return str(e)
      localhost_print_function('=========================================== candidates_account_settings_function END ===========================================')
      return redirect(checkout_session.url, code=303)
      # ------------------------ stripe checkout end ------------------------
  # ------------------------ if post data end ------------------------
  localhost_print_function('=========================================== candidates_account_settings_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/account_page_templates/index.html', user=current_user, users_company_name_to_html=current_user.company_name, user_email_to_html=current_user.email, user_account_created_str_to_html=user_account_created_str,stripe_subscription_obj_status_to_html=stripe_subscription_obj_status,user_sub_active_to_html=user_sub_active,stripe_current_period_end_datetime_str_to_html=stripe_current_period_end_datetime_str,user_obj_capacity_id_to_html=user_obj_capacity_id)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/upload', methods=['GET', 'POST'])
@login_required
def candidates_upload_emails_function():
  localhost_print_function('=========================================== candidates_upload_emails_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_upload_emails_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_upload_emails_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ delete all assessments that have been started by this user so far but abandoned start ------------------------
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr=None).delete()
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr='').delete()
  db.session.commit()
  # ------------------------ delete all assessments that have been started by this user so far but abandoned end ------------------------
  candidate_upload_error_statement = ''
  candidate_upload_success_statement = ''
  # ------------------------ get users total uploaded candidates start ------------------------
  current_user_uploaded_emails_arr = CandidatesUploadedCandidatesObj.query.filter_by(user_id_fk=current_user.id).all()
  len_current_user_uploaded_emails_arr = len(current_user_uploaded_emails_arr)
  # ------------------------ get users total uploaded candidates end ------------------------
  if request.method == 'POST':
    # ------------------------ form results start ------------------------
    try:
      ui_csv_file_uploaded = request.files['file']
    except:
      ui_csv_file_uploaded = None
    ui_email = request.form.get('candidate_upload_page_ui_email')
    # ------------------------ form results end ------------------------
    # ------------------------ ui_email individual start ------------------------
    if ui_email != None:
      candidate_upload_error_statement, candidate_upload_success_statement = validate_upload_candidate_function(db, current_user, ui_email, 'individual')
    # ------------------------ ui_email individual end ------------------------
    # ------------------------ ui_email bulk start ------------------------
    if ui_csv_file_uploaded != None:
      try:
        df_csv_data = pd.read_csv(ui_csv_file_uploaded)
        for i, r in df_csv_data.iterrows():
          ui_email = r[0]
          candidate_upload_error_statement, candidate_upload_success_statement = validate_upload_candidate_function(db, current_user, ui_email, 'bulk')
      except:
        candidate_upload_error_statement = 'uploaded file must be .csv format'
    # ------------------------ ui_email bulk end ------------------------
  localhost_print_function('=========================================== candidates_upload_emails_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/candidates_page_templates/candidates_upload_page_templates/index.html', user=current_user, users_company_name_to_html = current_user.company_name, len_current_user_uploaded_emails_arr_to_html = len_current_user_uploaded_emails_arr, error_message_to_html=candidate_upload_error_statement, success_message_to_html=candidate_upload_success_statement)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/analytics', methods=['GET', 'POST'])
@login_required
def candidates_analytics_function():
  localhost_print_function('=========================================== candidates_analytics_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_analytics_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_analytics_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ delete all assessments that have been started by this user so far but abandoned start ------------------------
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr=None).delete()
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr='').delete()
  db.session.commit()
  # ------------------------ delete all assessments that have been started by this user so far but abandoned end ------------------------
  # ------------------------ pull all candidates start ------------------------
  current_user_uploaded_emails_arr = CandidatesUploadedCandidatesObj.query.filter_by(user_id_fk=current_user.id).all()
  all_candidates_arr_of_dicts = []
  for i in current_user_uploaded_emails_arr:
    all_candidates_dict = {}
    all_candidates_dict['email'] = i.email
    # ------------------------ get candidate stats start ------------------------
    db_assessment_graded_obj = CandidatesAssessmentGradedObj.query.filter_by(candidate_email=i.email).all()
    if db_assessment_graded_obj == None:
      all_candidates_dict['total_assessments'] = 0
      all_candidates_dict['total_correct_answers'] = 0
      all_candidates_dict['total_correct_percent'] = '0%'
    else:
      # ------------------------ set variables start ------------------------
      total_assessments = 0
      total_correct_answers = 0
      total_correct_percent = 0
      total_correct_percent_counter = 0
      # ------------------------ set variables end ------------------------
      # ------------------------ loop add start ------------------------
      for i_assessment_obj in db_assessment_graded_obj:
        total_assessments += 1
        total_correct_answers += i_assessment_obj.correct_count
        total_correct_percent += i_assessment_obj.final_score
        total_correct_percent_counter += 1
      # ------------------------ loop add end ------------------------
      # ------------------------ assign result start ------------------------
      all_candidates_dict['total_assessments'] = total_assessments
      all_candidates_dict['total_correct_answers'] = total_correct_answers
      # ------------------------ divide by 0 error start ------------------------
      try:
        total_correct_percent_float = (total_correct_percent / total_correct_percent_counter) * 100
        total_correct_percent_str = str(total_correct_percent_float)[0:2] + '%'
        all_candidates_dict['total_correct_percent'] = total_correct_percent_str
      except:
        total_correct_percent_float = (total_correct_percent / 1) * 100
        total_correct_percent_str = str(total_correct_percent_float)[0:2] + '%'
        all_candidates_dict['total_correct_percent'] = total_correct_percent
      # ------------------------ divide by 0 error end ------------------------
      # ------------------------ assign result end ------------------------
    # ------------------------ get candidate stats end ------------------------
    all_candidates_arr_of_dicts.append(all_candidates_dict)
  # ------------------------ pull all candidates end ------------------------
  localhost_print_function('=========================================== candidates_analytics_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/candidates_page_templates/candidates_analytics_page_templates/index.html', user=current_user, users_company_name_to_html = current_user.company_name, all_candidates_arr_of_dicts_to_html=all_candidates_arr_of_dicts)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/create/question', methods=['GET', 'POST'])
@login_required
def candidates_create_question_function():
  localhost_print_function('=========================================== candidates_create_question_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_create_question_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_create_question_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ delete all assessments that have been started by this user so far but abandoned start ------------------------
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr=None).delete()
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr='').delete()
  db.session.commit()
  # ------------------------ delete all assessments that have been started by this user so far but abandoned end ------------------------
  if request.method == 'POST':
    pass
  localhost_print_function('=========================================== candidates_create_question_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/create_question/index.html', user=current_user, users_company_name_to_html=current_user.company_name)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessments/dashboard', methods=['GET', 'POST'])
@login_required
def candidates_assessments_dashboard_function():
  localhost_print_function('=========================================== candidates_assessments_dashboard_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_assessments_dashboard_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_assessments_dashboard_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ delete all assessments that have been started by this user so far but abandoned start ------------------------
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr=None).delete()
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr='').delete()
  db.session.commit()
  # ------------------------ delete all assessments that have been started by this user so far but abandoned end ------------------------
  localhost_print_function('=========================================== candidates_assessments_dashboard_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/assessments_page_templates/assessments_dashboard_page_templates/index.html', user=current_user, users_company_name_to_html = current_user.company_name)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessments/analytics', methods=['GET', 'POST'])
@login_required
def candidates_assessments_analytics_function():
  localhost_print_function('=========================================== candidates_assessments_analytics_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_assessments_analytics_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_assessments_analytics_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ delete all assessments that have been started by this user so far but abandoned start ------------------------
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr=None).delete()
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr='').delete()
  db.session.commit()
  # ------------------------ delete all assessments that have been started by this user so far but abandoned end ------------------------
  # ------------------------ pull all assessments start ------------------------
  current_user_assessments_created_arr = CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id).all()
  all_assessments_arr_of_dicts = []
  for i in current_user_assessments_created_arr:
    all_assessments_dict = {}
    all_assessments_dict['assessment_name'] = i.assessment_name
    # ------------------------ pull info schedules start ------------------------
    db_schedule_obj = CandidatesScheduleObj.query.filter_by(user_id_fk=current_user.id, assessment_name=i.assessment_name).all()
    # ------------------------ set variables start ------------------------
    candidates_pending = 0
    candidates_completed = 0
    # ------------------------ set variables end ------------------------
    for i_schedule_obj in db_schedule_obj:
      if i_schedule_obj.candidate_status == 'Pending':
        candidates_pending += 1
      elif i_schedule_obj.candidate_status == 'Completed':
        candidates_completed += 1
    all_assessments_dict['candidates_pending'] = candidates_pending
    all_assessments_dict['candidates_completed'] = candidates_completed
    # ------------------------ pull info schedules end ------------------------
    all_assessments_arr_of_dicts.append(all_assessments_dict)
  # ------------------------ pull all assessments end ------------------------
  localhost_print_function('=========================================== candidates_assessments_analytics_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/assessments_page_templates/assessments_analytics_page_templates/index.html', user=current_user, users_company_name_to_html = current_user.company_name, all_assessments_arr_of_dicts_to_html=all_assessments_arr_of_dicts)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessment/new', methods=['GET', 'POST'])
@login_required
def candidates_assessment_create_new_function():
  localhost_print_function('=========================================== candidates_assessment_create_new_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_assessment_create_new_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_assessment_create_new_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ delete all assessments that have been started by this user so far but abandoned start ------------------------
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr=None).delete()
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr='').delete()
  db.session.commit()
  # ------------------------ delete all assessments that have been started by this user so far but abandoned end ------------------------
  # ------------------------ pull all categories associated with candidates start ------------------------
  query_result_arr_of_dicts = select_general_function('select_all_candidate_categories_chosen')
  candidate_categories_arr = all_question_candidate_categories_sorted_function(query_result_arr_of_dicts)
  # ------------------------ pull all categories associated with candidates end ------------------------
  # ------------------------ pull all categories requested start ------------------------
  requested_languages_obj = CandidatesRequestLanguageObj.query.filter_by(approved_to_view=True).all()
  requested_languages_arr = pull_desired_languages_arr_function(requested_languages_obj)
  # ------------------------ pull all categories requested end ------------------------
  # ------------------------ combine lists categories exist and requested start ------------------------
  for i in requested_languages_arr:
    if i not in candidate_categories_arr:
      candidate_categories_arr.append(i)
  candidate_categories_arr = sorted(candidate_categories_arr)
  # ------------------------ combine lists categories exist and requested end ------------------------
  # ------------------------ break down array for html columns start ------------------------
  len_candidate_categories_arr = len(candidate_categories_arr)
  rows_per_col = int((len_candidate_categories_arr / 3) + 1)
  candidate_categories_arr_1 = candidate_categories_arr[:rows_per_col]
  candidate_categories_arr_2 = candidate_categories_arr[rows_per_col:rows_per_col*2]
  candidate_categories_arr_3 = candidate_categories_arr[rows_per_col*2:]
  # ------------------------ break down array for html columns end ------------------------
  create_assessment_error_statement = ''
  trial_name_attempt = ''
  # ------------------------ post method hit start ------------------------
  if request.method == 'POST':
    # ------------------------ get form user inputs start ------------------------
    ui_assessment_name = request.form.get('create_assessment_page_ui_name')
    ui_desired_languages_checkboxes_arr = request.form.getlist('testLabelAdded')
    # ------------------------ get form user inputs end ------------------------
    # ------------------------ sanitize/check user inputs start ------------------------
    # ------------------------ sanitize/check name start ------------------------
    ui_assessment_name_cleaned = sanitize_create_account_text_inputs_large_function(ui_assessment_name)
    if ui_assessment_name_cleaned == False:
      create_assessment_error_statement = 'Please fill out all required fields.'
    # ------------------------ sanitize/check name end ------------------------
    # ------------------------ check if assessment name already exists for user start ------------------------
    if ui_assessment_name_cleaned != False:
      user_assessment_name_already_exists = CandidatesAssessmentsCreatedObj.query.filter_by(assessment_name=ui_assessment_name,user_id_fk=current_user.id).first()
      if user_assessment_name_already_exists != None:
        ui_assessment_name_cleaned = False
        create_assessment_error_statement = f'Assessment name "{ui_assessment_name}" already exists.'
    # ------------------------ check if assessment name already exists for user end ------------------------
    # ------------------------ sanitize/check desired languages start ------------------------
    ui_desired_languages_checkboxes_arr = sanitize_loop_check_if_exists_within_arr_function(ui_desired_languages_checkboxes_arr, candidate_categories_arr)
    if ui_desired_languages_checkboxes_arr == [] or ui_desired_languages_checkboxes_arr == False:
      create_assessment_error_statement = 'Please fill out all required fields.'
      trial_name_attempt = ui_assessment_name
    ui_desired_languages_checkboxes_str = ''
    if ui_desired_languages_checkboxes_arr != False:
      ui_desired_languages_checkboxes_str = ','.join(ui_desired_languages_checkboxes_arr)
    # ------------------------ sanitize/check desired languages end ------------------------
    # ------------------------ sanitize/check user inputs end ------------------------
    # ------------------------ create new assessment in db start ------------------------
    if ui_assessment_name_cleaned != False and ui_desired_languages_checkboxes_arr != False and ui_desired_languages_checkboxes_arr != []:
      new_row = CandidatesAssessmentsCreatedObj(
        id=create_uuid_function('assessment_'),
        created_timestamp=create_timestamp_function(),
        user_id_fk=current_user.id,
        assessment_name=ui_assessment_name,
        desired_languages_arr = ui_desired_languages_checkboxes_str,
        total_questions = 10,
        delivery_type = 'default',
        question_ids_arr = None
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ create new assessment in db end ------------------------
      localhost_print_function('=========================================== candidates_assessment_create_new_function END ===========================================')
      return redirect(url_for('views.candidates_assessment_select_questions_function', url_assessment_name=ui_assessment_name))
  # ------------------------ post method hit end ------------------------
  localhost_print_function('=========================================== candidates_assessment_create_new_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/assessments_page_templates/assessments_create_new_page_templates/index.html', user=current_user, users_company_name_to_html = current_user.company_name, error_message_to_html=create_assessment_error_statement, candidate_categories_arr_1_to_html=candidate_categories_arr_1, candidate_categories_arr_2_to_html=candidate_categories_arr_2, candidate_categories_arr_3_to_html=candidate_categories_arr_3, trial_name_attempt_to_html=trial_name_attempt)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessment/new/questions/<url_assessment_name>', methods=['GET', 'POST'])
@login_required
def candidates_assessment_select_questions_function(url_assessment_name):
  localhost_print_function('=========================================== candidates_assessment_select_questions_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_assessment_select_questions_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_assessment_select_questions_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ invalid url_assessment_name start ------------------------
  if url_assessment_name == False or url_assessment_name == None or url_assessment_name == '':
    localhost_print_function('=========================================== candidates_assessment_select_questions_function END ===========================================')
    return redirect(url_for('views.dashboard_test_login_page_function'))
  # ------------------------ invalid url_assessment_name end ------------------------
  select_questions_error_statement = ''
  # ------------------------ get assessment obj details start ------------------------
  db_assessment_obj = CandidatesAssessmentsCreatedObj.query.filter_by(assessment_name=url_assessment_name,user_id_fk=current_user.id).first()
  if db_assessment_obj == None:
    localhost_print_function('=========================================== candidates_assessment_select_questions_function END ===========================================')
    return redirect(url_for('views.dashboard_test_login_page_function'))
  db_assessment_obj_id = db_assessment_obj.id
  db_assessment_obj_name = db_assessment_obj.assessment_name
  db_assessment_obj_desired_langs = db_assessment_obj.desired_languages_arr
  db_assessment_question_ids_arr = db_assessment_obj.question_ids_arr
  # ------------------------ get assessment obj details end ------------------------
  # ------------------------ individual redirect start ------------------------
  # if questions were already selected for quiz
  if db_assessment_question_ids_arr != None and db_assessment_question_ids_arr != '' and (len(db_assessment_question_ids_arr) != 0 and len(db_assessment_question_ids_arr) != 1):
    localhost_print_function('=========================================== candidates_assessment_select_questions_function END ===========================================')
    return redirect(url_for('views.dashboard_test_login_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ post method hit start ------------------------
  if request.method == 'POST':
    ui_select_question_checkbox_arr = request.form.getlist('ui_select_question_checkbox')
    # ------------------------ postman incorrect submission start ------------------------
    if len(ui_select_question_checkbox_arr) != 10:
      localhost_print_function('=========================================== candidates_assessment_select_questions_function END ===========================================')
      return redirect(url_for('views.dashboard_test_login_page_function'))
    # ------------------------ postman incorrect submission end ------------------------
    # ------------------------ make sure that all ids provided actually exist in db start ------------------------
    question_ids_actually_exist_check = check_if_question_id_arr_exists_function(ui_select_question_checkbox_arr)
    if question_ids_actually_exist_check == False:
      localhost_print_function('=========================================== candidates_assessment_select_questions_function END ===========================================')
      return redirect(url_for('views.dashboard_test_login_page_function'))
    # ------------------------ make sure that all ids provided actually exist in db end ------------------------
    # ------------------------ update row in db start ------------------------
    ui_select_question_checkbox_str = ','.join(ui_select_question_checkbox_arr)
    try:
      db_assessment_obj.question_ids_arr = ui_select_question_checkbox_str
      db.session.commit()
    except:
      localhost_print_function('error cannot update row')
      pass
    # ------------------------ update row in db end ------------------------
    # ------------------------ email self start ------------------------
    try:
      output_to_email = 'robert@triviafy.com'
      output_subject = f'Candidates - Triviafy New Assessment Created'
      output_body = f"Hi there,\n\nNew assessment created for \n\nBest,\nTriviafy"
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
    # ------------------------ email self end ------------------------
    localhost_print_function('=========================================== candidates_assessment_select_questions_function END ===========================================')
    return redirect(url_for('views.candidates_assessment_sucessfully_created_function'))
  # ------------------------ post method hit end ------------------------
  # ------------------------ prepare where statement start ------------------------
  where_clause_arr = []
  desired_langs_arr = db_assessment_obj_desired_langs.split(',')
  master_where_statement = ''
  for i in range(len(desired_langs_arr)):
    if i == (len(desired_langs_arr) - 1):
      master_where_statement += f"(question_categories_list LIKE '%{desired_langs_arr[i]}%' AND question_categories_list LIKE '%Candidates%')"
    else:
      master_where_statement += f"(question_categories_list LIKE '%{desired_langs_arr[i]}%' AND question_categories_list LIKE '%Candidates%') OR "
  where_clause_arr.append(master_where_statement)
  # ------------------------ prepare where statement end ------------------------
  # ------------------------ pull question obj from db start ------------------------
  query_result_arr_of_dicts = select_general_function('select_all_questions_for_x_categories', where_clause_arr[0])
  query_result_arr_of_dicts = question_arr_of_dicts_manipulations_function(query_result_arr_of_dicts)
  # ------------------------ pull question obj from db end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  user_obj = CandidatesUserObj.query.filter_by(id=current_user.id).first()
  fk_stripe_subscription_id = user_obj.fk_stripe_subscription_id
  stripe_subscription_obj = ''
  stripe_subscription_obj_status = 'not active'
  try:
    stripe_subscription_obj = stripe.Subscription.retrieve(fk_stripe_subscription_id)
    stripe_subscription_obj_status = stripe_subscription_obj.status
  except:
    pass
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ if subscription not paid start ------------------------
  user_sub_active = False
  if stripe_subscription_obj_status == 'active':
    user_sub_active = True
  if stripe_subscription_obj_status != 'active':
    for i_dict in query_result_arr_of_dicts:
      i_dict['question_answers_list'] = ''
  # ------------------------ if subscription not paid end ------------------------
  localhost_print_function('=========================================== candidates_assessment_select_questions_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/assessments_page_templates/assessments_create_new_page_templates/assessments_select_questions_page_templates/index.html', user=current_user, users_company_name_to_html=current_user.company_name, error_message_to_html=select_questions_error_statement, query_result_arr_of_dicts_to_html=query_result_arr_of_dicts, user_sub_active_to_html=user_sub_active)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessment/new/success', methods=['GET'])
@login_required
def candidates_assessment_sucessfully_created_function():
  localhost_print_function('=========================================== candidates_assessment_sucessfully_created_function START ===========================================')
  localhost_print_function('=========================================== candidates_assessment_sucessfully_created_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/assessments_page_templates/assessments_create_new_page_templates/assessments_successfully_created_page_templates/index.html', user=current_user, users_company_name_to_html=current_user.company_name)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessment/view/<url_assessment_name>', methods=['GET', 'POST'])
@login_required
def candidates_assessment_view_specific_function(url_assessment_name):
  localhost_print_function('=========================================== candidates_assessment_view_specific_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_assessment_view_specific_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_assessment_view_specific_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ invalid url_assessment_name start ------------------------
  if url_assessment_name == False or url_assessment_name == None or url_assessment_name == '':
    localhost_print_function('=========================================== candidates_assessment_view_specific_function END ===========================================')
    return redirect(url_for('views.dashboard_test_login_page_function'))
  # ------------------------ invalid url_assessment_name end ------------------------
  # ------------------------ pull assessment info start ------------------------
  db_assessment_obj = CandidatesAssessmentsCreatedObj.query.filter_by(assessment_name=url_assessment_name,user_id_fk=current_user.id).first()
  # ------------------------ pull assessment info end ------------------------
  # ------------------------ assign assessment info to dict start ------------------------
  assessment_info_dict = create_assessment_info_dict_function(db_assessment_obj)
  # ------------------------ assign assessment info to dict end ------------------------
  # ------------------------ check if user paid latest month start ------------------------
  user_paid_latest_month = False
  # ------------------------ check if user paid latest month end ------------------------
  # ------------------------ remove answers for non paying users start ------------------------
  if user_paid_latest_month == False:
    for i in assessment_info_dict['questions_arr_of_dicts']:
      i['question_answers_list'] = None
  # ------------------------ remove answers for non paying users end ------------------------
  localhost_print_function('=========================================== candidates_assessment_view_specific_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/assessments_page_templates/assessments_view_specific_page_templates/index.html', user=current_user, users_company_name_to_html=current_user.company_name, assessment_info_dict_to_html=assessment_info_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessment/results/<url_assessment_name>', methods=['GET', 'POST'])
@login_required
def candidates_assessment_results_specific_function(url_assessment_name):
  localhost_print_function('=========================================== candidates_assessment_results_specific_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_assessment_results_specific_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_assessment_results_specific_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ invalid url_assessment_name start ------------------------
  if url_assessment_name == False or url_assessment_name == None or url_assessment_name == '':
    localhost_print_function('=========================================== candidates_assessment_results_specific_function END ===========================================')
    return redirect(url_for('views.dashboard_test_login_page_function'))
  # ------------------------ invalid url_assessment_name end ------------------------
  # ------------------------ set variables start ------------------------
  assessment_name_title = url_assessment_name
  all_candidates_arr_of_dicts = []
  assessment_info_dict = {}
  emails_tracked_set = {'a'}
  # ------------------------ set variables end ------------------------
  # ------------------------ pull db info schedule start ------------------------
  db_schedule_obj = CandidatesScheduleObj.query.filter_by(assessment_name=url_assessment_name,user_id_fk=current_user.id).all()
  for i_schedule_obj in db_schedule_obj:
    i_email = i_schedule_obj.candidates
    if i_email not in emails_tracked_set:
      emails_tracked_set.add(i_email)
      assessment_info_dict = {}
      assessment_info_dict['email'] = i_email
      total_schedules_pending = 0
      total_schedules_completed = 0
      # ------------------------ pull db info schedule candidate specific start ------------------------
      db_schedule_email_specific_obj = CandidatesScheduleObj.query.filter_by(assessment_name=url_assessment_name,user_id_fk=current_user.id,candidates=i_email).all()
      for i_schedule_email_specific_obj in db_schedule_email_specific_obj:
        if i_schedule_email_specific_obj.candidate_status == 'Pending':
          total_schedules_pending += 1
        elif i_schedule_email_specific_obj.candidate_status == 'Completed':
          total_schedules_completed += 1
      assessment_info_dict['total_schedules_pending'] = total_schedules_pending
      assessment_info_dict['total_schedules_completed'] = total_schedules_completed
      # ------------------------ pull db info schedule candidate specific end ------------------------
      # ------------------------ pull db info graded candidate specific start ------------------------
      db_assessments_email_specific_obj = CandidatesAssessmentGradedObj.query.filter_by(assessment_name=url_assessment_name,created_assessment_user_id_fk=current_user.id,candidate_email=i_email).all()
      total_correct_count = 0
      total_final_score = 0
      total_final_score_counter = 0
      average_final_score = 0
      for i_assessment_email_specific_obj in db_assessments_email_specific_obj:
        total_final_score_counter += 1
        total_correct_count += i_assessment_email_specific_obj.correct_count
        total_final_score += i_assessment_email_specific_obj.final_score
      assessment_info_dict['total_correct_count'] = total_correct_count
      try:
        average_final_score = (total_final_score / total_final_score_counter) * 100
        average_final_score = str(average_final_score)[0:2] + '%'
        assessment_info_dict['average_final_score'] = average_final_score
      except:
        average_final_score = (total_final_score / 1) * 100
        average_final_score = str(average_final_score)[0:2] + '%'
        assessment_info_dict['average_final_score'] = average_final_score
      # ------------------------ pull db info graded candidate specific end ------------------------
      all_candidates_arr_of_dicts.append(assessment_info_dict)
  # ------------------------ pull db info schedule end ------------------------
  emails_tracked_set.remove('a')
  # ------------------------ remove answers for non paying users end ------------------------
  localhost_print_function('=========================================== candidates_assessment_results_specific_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/assessments_page_templates/assessments_analytics_page_templates/assessments_results_page_templates/index.html', user=current_user, users_company_name_to_html=current_user.company_name, all_candidates_arr_of_dicts_to_html=all_candidates_arr_of_dicts, assessment_name_title_to_html=assessment_name_title)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/candidate/results/<url_candidate_email>', methods=['GET', 'POST'])
@login_required
def candidates_candidate_results_specific_function(url_candidate_email):
  localhost_print_function('=========================================== candidates_candidate_results_specific_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_candidate_results_specific_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_candidate_results_specific_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ invalid url_candidate_email start ------------------------
  if url_candidate_email == False or url_candidate_email == None or url_candidate_email == '':
    localhost_print_function('=========================================== candidates_candidate_results_specific_function END ===========================================')
    return redirect(url_for('views.dashboard_test_login_page_function'))
  # ------------------------ invalid url_assessment_name end ------------------------
  # ------------------------ set variables start ------------------------
  all_candidate_assessments_arr_of_dicts = []
  assessment_info_dict = {}
  assessment_tracked_set = {'a'}
  # ------------------------ set variables end ------------------------
  # ------------------------ pull db info schedule start ------------------------
  db_schedule_obj = CandidatesScheduleObj.query.filter_by(candidates=url_candidate_email,user_id_fk=current_user.id).all()
  for i_schedule_obj in db_schedule_obj:
    i_assessment_id_fk = i_schedule_obj.assessment_id_fk
    if i_assessment_id_fk not in assessment_tracked_set:
      assessment_tracked_set.add(i_assessment_id_fk)
      assessment_info_dict = {}
      assessment_info_dict['assessment_id_fk'] = i_assessment_id_fk
      assessment_info_dict['assessment_name'] = i_schedule_obj.assessment_name
      total_schedules_pending = 0
      total_schedules_completed = 0
      # ------------------------ pull db info schedule candidate specific start ------------------------
      db_schedule_email_specific_obj = CandidatesScheduleObj.query.filter_by(candidates=url_candidate_email,user_id_fk=current_user.id,assessment_id_fk=i_assessment_id_fk).all()
      for i_schedule_email_specific_obj in db_schedule_email_specific_obj:
        if i_schedule_email_specific_obj.candidate_status == 'Pending':
          total_schedules_pending += 1
        elif i_schedule_email_specific_obj.candidate_status == 'Completed':
          total_schedules_completed += 1
      assessment_info_dict['total_schedules_pending'] = total_schedules_pending
      assessment_info_dict['total_schedules_completed'] = total_schedules_completed
      # ------------------------ pull db info schedule candidate specific end ------------------------
      # ------------------------ pull db info graded candidate specific start ------------------------
      db_assessments_email_specific_obj = CandidatesAssessmentGradedObj.query.filter_by(candidate_email=url_candidate_email,created_assessment_user_id_fk=current_user.id,assessment_id_fk=i_assessment_id_fk).all()
      total_correct_count = 0
      total_final_score = 0
      total_final_score_counter = 0
      average_final_score = 0
      for i_assessment_email_specific_obj in db_assessments_email_specific_obj:
        total_final_score_counter += 1
        total_correct_count += i_assessment_email_specific_obj.correct_count
        total_final_score += i_assessment_email_specific_obj.final_score
      assessment_info_dict['total_correct_count'] = total_correct_count
      try:
        average_final_score = (total_final_score / total_final_score_counter) * 100
        average_final_score = str(average_final_score)[0:2] + '%'
        assessment_info_dict['average_final_score'] = average_final_score
      except:
        average_final_score = (total_final_score / 1) * 100
        average_final_score = str(average_final_score)[0:2] + '%'
        assessment_info_dict['average_final_score'] = average_final_score
      # ------------------------ pull db info graded candidate specific end ------------------------
      all_candidate_assessments_arr_of_dicts.append(assessment_info_dict)
  assessment_tracked_set.remove('a')
  # ------------------------ pull db info schedule end ------------------------
  localhost_print_function('=========================================== candidates_candidate_results_specific_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/candidates_page_templates/candidates_view_specific_page_templates/index.html', user=current_user, users_company_name_to_html=current_user.company_name, all_candidate_assessments_arr_of_dicts_to_html=all_candidate_assessments_arr_of_dicts, email_title_to_html=url_candidate_email)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/schedule', methods=['GET', 'POST'])
@login_required
def candidates_schedule_dashboard_function():
  localhost_print_function('=========================================== candidates_schedule_dashboard_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_schedule_dashboard_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_schedule_dashboard_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ delete all assessments that have been started by this user so far but abandoned start ------------------------
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr=None).delete()
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr='').delete()
  db.session.commit()
  # ------------------------ delete all assessments that have been started by this user so far but abandoned end ------------------------
  # ------------------------ remove answers for non paying users end ------------------------
  localhost_print_function('=========================================== candidates_schedule_dashboard_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/schedule_page_templates/schedule_dashboard_page_templates/index.html', user=current_user, users_company_name_to_html=current_user.company_name)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/schedule/new', methods=['GET', 'POST'])
@login_required
def candidates_schedule_create_new_function():
  localhost_print_function('=========================================== candidates_schedule_create_new_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_schedule_create_new_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_schedule_create_new_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ messages start ------------------------
  success_message_schedule = ''
  error_message_schedule = ''
  # ------------------------ messages end ------------------------
  # ------------------------ pull all user assessments start ------------------------
  current_user_assessments_created_arr = CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id).order_by(CandidatesAssessmentsCreatedObj.assessment_name).all()
  current_user_assessment_names_arr = []
  for i in current_user_assessments_created_arr:
    current_user_assessment_names_arr.append(i.assessment_name)
  current_user_assessment_names_arr = sorted(current_user_assessment_names_arr)
  # ------------------------ pull all user assessments end ------------------------
  # ------------------------ pull all user candidates start ------------------------
  current_user_candidates_uploaded_arr = CandidatesUploadedCandidatesObj.query.filter_by(user_id_fk=current_user.id).order_by(CandidatesUploadedCandidatesObj.email).all()
  current_user_candidates_arr = []
  for i in current_user_candidates_uploaded_arr:
    current_user_candidates_arr.append(i.email)
  current_user_candidates_arr = sorted(current_user_candidates_arr)
  # ------------------------ pull all user candidates end ------------------------
  # ------------------------ pull all available dates, times, timezones start ------------------------
  next_x_days_arr = next_x_days_function()
  times_arr, timezone_arr = times_arr_function()
  # ------------------------ pull all available dates, times, timezones end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  user_obj = CandidatesUserObj.query.filter_by(id=current_user.id).first()
  fk_stripe_subscription_id = user_obj.fk_stripe_subscription_id
  stripe_subscription_obj = ''
  stripe_subscription_obj_status = 'not active'
  try:
    stripe_subscription_obj = stripe.Subscription.retrieve(fk_stripe_subscription_id)
    stripe_subscription_obj_status = stripe_subscription_obj.status
  except:
    pass
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ if subscription not paid start ------------------------
  user_sub_active = False
  if stripe_subscription_obj_status == 'active':
    user_sub_active = True
    pass
  if stripe_subscription_obj_status != 'active':
    db_schedule_obj = CandidatesScheduleObj.query.filter_by(user_id_fk=current_user.id).all()
    if len(db_schedule_obj) <= 3:
      current_user_candidates_arr = [user_obj.email]
    else:
      current_user_candidates_arr = []
  # ------------------------ if subscription not paid end ------------------------
  # ------------------------ post triggered start ------------------------
  if request.method == 'POST':
    # ------------------------ get user inputs start ------------------------
    ui_schedule_assessment_selected = request.form.get('ui_schedule_assessment_selected')       # str
    ui_schedule_candidates_selected = request.form.getlist('ui_schedule_candidates_selected')   # list of str
    ui_schedule_date_selected = request.form.get('ui_schedule_date_selected')                   # str
    ui_schedule_time_selected = request.form.get('ui_schedule_time_selected')                   # str
    ui_schedule_timezone_selected = request.form.get('ui_schedule_timezone_selected')           # str
    # ------------------------ get user inputs end ------------------------
    # ------------------------ verify user inputs start ------------------------
    all_ui_verified_correct = True
    ui_schedule_assessment_selected_check = sanitize_check_if_str_exists_within_arr_function(ui_schedule_assessment_selected, current_user_assessment_names_arr)
    ui_schedule_candidates_selected_check = sanitize_loop_check_if_exists_within_arr_function(ui_schedule_candidates_selected, current_user_candidates_arr)
    ui_schedule_date_selected_check = sanitize_check_if_str_exists_within_arr_function(ui_schedule_date_selected, next_x_days_arr)
    ui_schedule_time_selected_check = sanitize_check_if_str_exists_within_arr_function(ui_schedule_time_selected, times_arr)
    ui_schedule_timezone_selected_check = sanitize_check_if_str_exists_within_arr_function(ui_schedule_timezone_selected, timezone_arr)
    if ui_schedule_assessment_selected_check == False or ui_schedule_candidates_selected_check == False or ui_schedule_date_selected_check == False or ui_schedule_time_selected_check == False or ui_schedule_timezone_selected_check == False:
      error_message_schedule = 'Please fill out all fields.'
      all_ui_verified_correct = False
    # ------------------------ verify user inputs end ------------------------
    # ------------------------ insert to db start ------------------------
    if all_ui_verified_correct == True:
      # ------------------------ get assessment id based on name and user id fk start ------------------------
      db_assessment_obj = CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id, assessment_name=ui_schedule_assessment_selected).first()
      db_assessment_obj_assessment_id = db_assessment_obj.id
      # ------------------------ get assessment id based on name and user id fk end ------------------------
      for i in ui_schedule_candidates_selected:
        new_row = CandidatesScheduleObj(
          id = create_uuid_function('schedule_'),
          created_timestamp = create_timestamp_function(),
          user_id_fk = current_user.id,
          assessment_id_fk = db_assessment_obj_assessment_id,
          assessment_name = ui_schedule_assessment_selected,
          candidates = i,
          send_date = ui_schedule_date_selected,
          send_time = ui_schedule_time_selected,
          send_timezone = ui_schedule_timezone_selected,
          candidate_status = 'Pending',
          expiring_url = create_uuid_function('expire_')
        )
        db.session.add(new_row)
        db.session.commit()
      success_message_schedule = 'Schedule created!'
    # ------------------------ insert to db end ------------------------
  # ------------------------ post triggered end ------------------------
  localhost_print_function('=========================================== candidates_schedule_create_new_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/schedule_page_templates/schedule_create_new_page_templates/index.html', user=current_user, users_company_name_to_html=current_user.company_name, current_user_assessment_names_arr_to_html=current_user_assessment_names_arr, current_user_candidates_arr_to_html=current_user_candidates_arr, next_x_days_arr_to_html=next_x_days_arr, times_arr_to_html=times_arr, timezone_arr_to_html=timezone_arr, success_message_to_html=success_message_schedule, error_message_to_html=error_message_schedule,user_sub_active_to_html=user_sub_active)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/schedule/now', methods=['GET', 'POST'])
@login_required
def candidates_schedule_create_now_function():
  localhost_print_function('=========================================== candidates_schedule_create_now_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_schedule_create_now_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_schedule_create_now_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ messages start ------------------------
  success_message_schedule = ''
  error_message_schedule = ''
  # ------------------------ messages end ------------------------
  # ------------------------ pull all user assessments start ------------------------
  current_user_assessments_created_arr = CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id).order_by(CandidatesAssessmentsCreatedObj.assessment_name).all()
  current_user_assessment_names_arr = []
  for i in current_user_assessments_created_arr:
    current_user_assessment_names_arr.append(i.assessment_name)
  current_user_assessment_names_arr = sorted(current_user_assessment_names_arr)
  # ------------------------ pull all user assessments end ------------------------
  # ------------------------ pull all user candidates start ------------------------
  current_user_candidates_uploaded_arr = CandidatesUploadedCandidatesObj.query.filter_by(user_id_fk=current_user.id).order_by(CandidatesUploadedCandidatesObj.email).all()
  current_user_candidates_arr = []
  for i in current_user_candidates_uploaded_arr:
    current_user_candidates_arr.append(i.email)
  current_user_candidates_arr = sorted(current_user_candidates_arr)
  # ------------------------ pull all user candidates end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  user_obj = CandidatesUserObj.query.filter_by(id=current_user.id).first()
  fk_stripe_subscription_id = user_obj.fk_stripe_subscription_id
  stripe_subscription_obj = ''
  stripe_subscription_obj_status = 'not active'
  try:
    stripe_subscription_obj = stripe.Subscription.retrieve(fk_stripe_subscription_id)
    stripe_subscription_obj_status = stripe_subscription_obj.status
  except:
    pass
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ if subscription not paid start ------------------------
  user_sub_active = False
  if stripe_subscription_obj_status == 'active':
    user_sub_active = True
    pass
  if stripe_subscription_obj_status != 'active':
    db_schedule_obj = CandidatesScheduleObj.query.filter_by(user_id_fk=current_user.id).all()
    if len(db_schedule_obj) <= 3:
      current_user_candidates_arr = [user_obj.email]
    else:
      current_user_candidates_arr = []
  # ------------------------ if subscription not paid end ------------------------
  # ------------------------ post triggered start ------------------------
  if request.method == 'POST':
    # ------------------------ get user inputs start ------------------------
    ui_schedule_assessment_selected = request.form.get('ui_schedule_assessment_selected')       # str
    ui_schedule_candidates_selected = request.form.getlist('ui_schedule_candidates_selected')   # list of str
    # ------------------------ get user inputs end ------------------------
    # ------------------------ verify user inputs start ------------------------
    all_ui_verified_correct = True
    ui_schedule_assessment_selected_check = sanitize_check_if_str_exists_within_arr_function(ui_schedule_assessment_selected, current_user_assessment_names_arr)
    ui_schedule_candidates_selected_check = sanitize_loop_check_if_exists_within_arr_function(ui_schedule_candidates_selected, current_user_candidates_arr)
    if ui_schedule_assessment_selected_check == False or ui_schedule_candidates_selected_check == False:
      error_message_schedule = 'Please fill out all fields.'
      all_ui_verified_correct = False
    # ------------------------ verify user inputs end ------------------------
    # ------------------------ insert to db start ------------------------
    if all_ui_verified_correct == True:
      # ------------------------ get assessment id based on name and user id fk start ------------------------
      db_assessment_obj = CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id, assessment_name=ui_schedule_assessment_selected).first()
      db_assessment_obj_assessment_id = db_assessment_obj.id
      # ------------------------ get assessment id based on name and user id fk end ------------------------
      for i_email in ui_schedule_candidates_selected:
        expiring_url_i_created = create_uuid_function('expire_')
        new_row = CandidatesScheduleObj(
          id = create_uuid_function('schedule_'),
          created_timestamp = create_timestamp_function(),
          user_id_fk = current_user.id,
          assessment_id_fk = db_assessment_obj_assessment_id,
          assessment_name = ui_schedule_assessment_selected,
          candidates = i_email,
          send_date = 'Immediate',
          send_time = 'Immediate',
          send_timezone = 'Immediate',
          candidate_status = 'Pending',
          expiring_url = expiring_url_i_created
        )
        db.session.add(new_row)
        db.session.commit()
        # ------------------------ insert to db end ------------------------
        # ------------------------ send email start ------------------------
        output_to_email = i_email
        output_subject = f'Triviafy Candidate Assessment: {ui_schedule_assessment_selected}'
        output_body = f"Hi there,\n\nYour Triviafy candidate assessment is ready!\nThe following link will expire 1 hour from the time you receive this email.\n\nPlease visit the following link to complete your assessment: https://triviafy.com/candidates/assessment/{expiring_url_i_created} \n\nBest,\nTriviafy"
        send_email_template_function(output_to_email, output_subject, output_body)
        # ------------------------ send email end ------------------------
        # ------------------------ insert email to db start ------------------------
        new_row_email = CandidatesEmailSentObj(
          id = create_uuid_function('email_test_'),
          created_timestamp = create_timestamp_function(),
          from_user_id_fk = current_user.id,
          to_email = output_to_email,
          assessment_expiring_url_fk = expiring_url_i_created,
          subject = output_subject,
          body = output_body
        )
        db.session.add(new_row_email)
        db.session.commit()
        # ------------------------ insert email to db end ------------------------
      success_message_schedule = 'Assessment email sent!'
  # ------------------------ post triggered end ------------------------
  localhost_print_function('=========================================== candidates_schedule_create_now_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/schedule_page_templates/schedule_create_now_page_templates/index.html', user=current_user, users_company_name_to_html=current_user.company_name, current_user_assessment_names_arr_to_html=current_user_assessment_names_arr, current_user_candidates_arr_to_html=current_user_candidates_arr, success_message_to_html=success_message_schedule, error_message_to_html=error_message_schedule,user_sub_active_to_html=user_sub_active)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/schedule/analytics', methods=['GET', 'POST'])
@login_required
def candidates_schedule_analytics_function():
  localhost_print_function('=========================================== candidates_schedule_analytics_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_schedule_analytics_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_schedule_analytics_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ delete all assessments that have been started by this user so far but abandoned start ------------------------
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr=None).delete()
  CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=current_user.id,question_ids_arr='').delete()
  db.session.commit()
  # ------------------------ delete all assessments that have been started by this user so far but abandoned end ------------------------
  # ------------------------ pull schedules start ------------------------
  current_user_schedules_obj = CandidatesScheduleObj.query.filter_by(user_id_fk=current_user.id).order_by(CandidatesScheduleObj.created_timestamp).all()
  all_schedules_arr_of_dicts = []
  for i in current_user_schedules_obj:
    all_assessments_dict = {}
    all_assessments_dict['created_timestamp'] = i.created_timestamp.strftime('%m-%d-%Y')
    all_assessments_dict['assessment_name'] = i.assessment_name
    all_assessments_dict['candidates'] = i.candidates
    all_assessments_dict['send_date'] = i.send_date
    all_assessments_dict['send_time'] = i.send_time
    all_assessments_dict['send_timezone'] = i.send_timezone
    all_assessments_dict['candidate_status'] = i.candidate_status
    all_schedules_arr_of_dicts.append(all_assessments_dict)
  # ------------------------ pull schedules end ------------------------
  localhost_print_function('=========================================== candidates_schedule_analytics_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/schedule_page_templates/schedule_analytics_page_templates/index.html', user=current_user, users_company_name_to_html=current_user.company_name, all_schedules_arr_of_dicts_to_html=all_schedules_arr_of_dicts)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessment/invalid')
def candidates_assessment_invalid_function():
  localhost_print_function('=========================================== candidates_assessment_invalid_function START ===========================================')
  localhost_print_function('=========================================== candidates_assessment_invalid_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/assessments_page_templates/assessment_not_found/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessment/early')
def candidates_assessment_early_function():
  localhost_print_function('=========================================== candidates_assessment_early_function START ===========================================')
  localhost_print_function('=========================================== candidates_assessment_early_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/assessments_page_templates/assessment_early/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessment/completed/success')
def candidates_assessment_completed_success_function():
  localhost_print_function('=========================================== candidates_assessment_completed_success_function START ===========================================')
  localhost_print_function('=========================================== candidates_assessment_completed_success_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/assessments_page_templates/assessment_completed_success/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessment/closed')
def candidates_assessment_closed_function():
  localhost_print_function('=========================================== candidates_assessment_closed_function START ===========================================')
  localhost_print_function('=========================================== candidates_assessment_closed_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/assessments_page_templates/assessment_closed/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessment/<url_assessment_expiring>', methods=['GET', 'POST'])
def candidates_assessment_expiring_function(url_assessment_expiring):
  localhost_print_function('=========================================== candidates_assessment_expiring_function START ===========================================')
  # ------------------------ invalid url_assessment_name start ------------------------
  if url_assessment_expiring == False or url_assessment_expiring == None or url_assessment_expiring == '':
    localhost_print_function('=========================================== candidates_assessment_expiring_function END ===========================================')
    return redirect(url_for('views.candidates_assessment_invalid_function'))
  # ------------------------ invalid url_assessment_name end ------------------------
  # ------------------------ check if answers already submitted start ------------------------
  db_already_graded_obj = CandidatesAssessmentGradedObj.query.filter_by(assessment_expiring_url_fk=url_assessment_expiring).first()
  if db_already_graded_obj != None:
    localhost_print_function('=========================================== candidates_assessment_expiring_function END ===========================================')
    return redirect(url_for('views.candidates_assessment_closed_function'))
  # ------------------------ check if answers already submitted end ------------------------
  # ------------------------ expire check based on email send datetime start ------------------------
  db_email_obj = CandidatesEmailSentObj.query.filter_by(assessment_expiring_url_fk=url_assessment_expiring).order_by(CandidatesEmailSentObj.created_timestamp.desc()).first()
  # ------------------------ check if url exists start ------------------------
  if db_email_obj == None:
    localhost_print_function('=========================================== candidates_assessment_expiring_function END ===========================================')
    return redirect(url_for('views.candidates_assessment_invalid_function'))
  # ------------------------ check if url exists end ------------------------
  email_sent_timestamp = db_email_obj.created_timestamp      # type: datetime.datetime
  # ------------------------ expire check based on email send datetime end ------------------------
  # ------------------------ check if schedule id expired start ------------------------
  expired_assessment_check, assessment_not_open_yet_check = expired_assessment_check_function(email_sent_timestamp)
  if assessment_not_open_yet_check == True:
    localhost_print_function('=========================================== candidates_assessment_expiring_function END ===========================================')
    return redirect(url_for('views.candidates_assessment_early_function'))
  if expired_assessment_check == True:
    localhost_print_function('=========================================== candidates_assessment_expiring_function END ===========================================')
    return redirect(url_for('views.candidates_assessment_invalid_function'))
  # ------------------------ check if schedule id expired end ------------------------
  # ------------------------ pull schedule info start ------------------------
  db_schedule_obj = CandidatesScheduleObj.query.filter_by(expiring_url=url_assessment_expiring).first()
  # ------------------------ pull schedule info end ------------------------
  # ------------------------ check if url exists start ------------------------
  if db_schedule_obj == None:
    localhost_print_function('=========================================== candidates_assessment_expiring_function END ===========================================')
    return redirect(url_for('views.candidates_assessment_invalid_function'))
  # ------------------------ check if url exists end ------------------------
  # ------------------------ pull desired schedule info start ------------------------
  db_schedule_obj_user_id_fk = db_schedule_obj.user_id_fk
  db_schedule_obj_assessment_id_fk = db_schedule_obj.assessment_id_fk
  db_schedule_obj_candidate_email = db_schedule_obj.candidates
  db_schedule_obj_assessment_name = db_schedule_obj.assessment_name
  # ------------------------ pull desired schedule info end ------------------------
  # ------------------------ pull assessment info start ------------------------
  db_assessment_obj = CandidatesAssessmentsCreatedObj.query.filter_by(id=db_schedule_obj_assessment_id_fk).first()
  # ------------------------ pull assessment info end ------------------------
  # ------------------------ check if url exists start ------------------------
  if db_assessment_obj == None:
    localhost_print_function('=========================================== candidates_assessment_expiring_function END ===========================================')
    return redirect(url_for('views.candidates_assessment_invalid_function'))
  # ------------------------ check if url exists end ------------------------
  # ------------------------ assign assessment info to dict start ------------------------
  assessment_info_dict = create_assessment_info_dict_function(db_assessment_obj)
  # ------------------------ assign assessment info to dict end ------------------------
  # ------------------------ store answers in backend for later reference start ------------------------
  backend_store_question_answers_dict = backend_store_question_answers_dict_function(assessment_info_dict)
  # ------------------------ store answers in backend for later reference end ------------------------
  # ------------------------ remove answers for candidate start ------------------------
  for i in assessment_info_dict['questions_arr_of_dicts']:
    i['question_answers_list'] = None
  # ------------------------ remove answers for candidate end ------------------------
  # ------------------------ pull user info for company name start ------------------------
  db_user_obj = CandidatesUserObj.query.filter_by(id=db_schedule_obj_user_id_fk).first()
  if db_user_obj == None:
    localhost_print_function('=========================================== candidates_assessment_expiring_function END ===========================================')
    return redirect(url_for('views.candidates_assessment_invalid_function'))
  db_user_obj_company_name = db_user_obj.company_name
  # ------------------------ pull user info for company name end ------------------------
  # ------------------------ post triggered start ------------------------
  ui_answers_error_statement = ''
  if request.method == 'POST':
    # ------------------------ ui candidate answers original start ------------------------
    candidate_ui_question_answer_1 = request.form.get('candidate_ui_question_answer_1')
    candidate_ui_question_answer_2 = request.form.get('candidate_ui_question_answer_2')
    candidate_ui_question_answer_3 = request.form.get('candidate_ui_question_answer_3')
    candidate_ui_question_answer_4 = request.form.get('candidate_ui_question_answer_4')
    candidate_ui_question_answer_5 = request.form.get('candidate_ui_question_answer_5')
    candidate_ui_question_answer_6 = request.form.get('candidate_ui_question_answer_6')
    candidate_ui_question_answer_7 = request.form.get('candidate_ui_question_answer_7')
    candidate_ui_question_answer_8 = request.form.get('candidate_ui_question_answer_8')
    candidate_ui_question_answer_9 = request.form.get('candidate_ui_question_answer_9')
    candidate_ui_question_answer_10 = request.form.get('candidate_ui_question_answer_10')
    # ------------------------ ui candidate answers original end ------------------------
    # ------------------------ sanitize ui answers start ------------------------
    candidate_ui_question_answer_1_checked = sanitize_candidate_ui_answer_text_function(candidate_ui_question_answer_1)
    candidate_ui_question_answer_2_checked = sanitize_candidate_ui_answer_text_function(candidate_ui_question_answer_2)
    candidate_ui_question_answer_3_checked = sanitize_candidate_ui_answer_text_function(candidate_ui_question_answer_3)
    candidate_ui_question_answer_4_checked = sanitize_candidate_ui_answer_text_function(candidate_ui_question_answer_4)
    candidate_ui_question_answer_5_checked = sanitize_candidate_ui_answer_text_function(candidate_ui_question_answer_5)
    candidate_ui_question_answer_6_checked = sanitize_candidate_ui_answer_text_function(candidate_ui_question_answer_6)
    candidate_ui_question_answer_7_checked = sanitize_candidate_ui_answer_text_function(candidate_ui_question_answer_7)
    candidate_ui_question_answer_8_checked = sanitize_candidate_ui_answer_text_function(candidate_ui_question_answer_8)
    candidate_ui_question_answer_9_checked = sanitize_candidate_ui_answer_text_function(candidate_ui_question_answer_9)
    candidate_ui_question_answer_10_checked = sanitize_candidate_ui_answer_text_function(candidate_ui_question_answer_10)
    # ------------------------ sanitize ui answers end ------------------------
    # ------------------------ check if invalid inputs start ------------------------
    if candidate_ui_question_answer_1_checked == False or candidate_ui_question_answer_2_checked == False or candidate_ui_question_answer_3_checked == False or candidate_ui_question_answer_4_checked == False or candidate_ui_question_answer_5_checked == False or candidate_ui_question_answer_6_checked == False or candidate_ui_question_answer_7_checked == False or candidate_ui_question_answer_8_checked == False or candidate_ui_question_answer_9_checked == False or candidate_ui_question_answer_10_checked == False:
      ui_answers_error_statement = 'Please answer all questions.'
    # ------------------------ check if invalid inputs end ------------------------
    # ------------------------ add user answers to assessment arr of dict start ------------------------
    assessment_info_dict = map_user_answers_to_questions_dict_function(assessment_info_dict, candidate_ui_question_answer_1, candidate_ui_question_answer_2, candidate_ui_question_answer_3, candidate_ui_question_answer_4, candidate_ui_question_answer_5, candidate_ui_question_answer_6, candidate_ui_question_answer_7, candidate_ui_question_answer_8, candidate_ui_question_answer_9, candidate_ui_question_answer_10)
    # ------------------------ add user answers to assessment arr of dict end ------------------------
    # ------------------------ only start grading if all valid answers provided start ------------------------
    if candidate_ui_question_answer_1_checked != False and candidate_ui_question_answer_2_checked != False and candidate_ui_question_answer_3_checked != False and candidate_ui_question_answer_4_checked != False and candidate_ui_question_answer_5_checked != False and candidate_ui_question_answer_6_checked != False and candidate_ui_question_answer_7_checked != False and candidate_ui_question_answer_8_checked != False and candidate_ui_question_answer_9_checked != False and candidate_ui_question_answer_10_checked != False:
      # ------------------------ reassign correct answers back to dict start ------------------------
      for i_dict in assessment_info_dict['questions_arr_of_dicts']:
        i_question_uuid = i_dict['question_uuid']
        answer_list_lookup = backend_store_question_answers_dict[i_question_uuid]
        i_dict['question_answers_list'] = answer_list_lookup
      # ------------------------ reassign correct answers back to dict end ------------------------
      # ------------------------ grading function start ------------------------
      assessment_info_dict = grade_assessment_answers_dict_function(assessment_info_dict)
      # ------------------------ grading function end ------------------------
      # ------------------------ insert db start ------------------------
      ui_total_correct_answers = assessment_info_dict['ui_total_correct_answers']
      ui_final_score = assessment_info_dict['ui_final_score']
      try:
        new_row_graded = CandidatesAssessmentGradedObj(
          id = create_uuid_function('graded_'),
          created_timestamp = create_timestamp_function(),
          candidate_email = db_schedule_obj_candidate_email,
          assessment_name = db_schedule_obj_assessment_name,
          assessment_id_fk = assessment_info_dict['id'],
          created_assessment_user_id_fk = db_schedule_obj_user_id_fk,
          assessment_expiring_url_fk = url_assessment_expiring,
          correct_count = ui_total_correct_answers,
          final_score = ui_final_score,
          assessment_obj = json.dumps(assessment_info_dict)
        )
        db.session.add(new_row_graded)
        db.session.commit()
      except:
        pass
      # ------------------------ insert db end ------------------------
      # ------------------------ update row in db schedule start ------------------------
      try:
        db_schedule_obj = CandidatesScheduleObj.query.filter_by(expiring_url=url_assessment_expiring).first()
        db_schedule_obj.candidate_status = 'Completed'
        db.session.commit()
      except:
        localhost_print_function('error cannot update row')
        pass
      # ------------------------ update row in db schedule end ------------------------
      localhost_print_function('=========================================== candidates_assessment_expiring_function END ===========================================')
      return redirect(url_for('views.candidates_assessment_completed_success_function'))
    # ------------------------ only start grading if all valid answers provided end ------------------------
  # ------------------------ post triggered end ------------------------
  localhost_print_function('=========================================== candidates_assessment_expiring_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/assessments_page_templates/assessment_candidate_test/index.html', users_company_name_to_html=db_user_obj_company_name, error_message_to_html=ui_answers_error_statement, assessment_info_dict_to_html=assessment_info_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/assessment/<url_email>/<url_assessment_name>', methods=['GET', 'POST'])
@login_required
def candidates_assessment_i_answers_function(url_email, url_assessment_name):
  localhost_print_function('=========================================== candidates_assessment_i_answers_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_assessment_i_answers_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_assessment_i_answers_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ invalid url_candidate_email start ------------------------
  if url_email == False or url_email == None or url_email == '' or url_assessment_name == False or url_assessment_name == None or url_assessment_name == '':
    localhost_print_function('=========================================== candidates_assessment_i_answers_function END ===========================================')
    return redirect(url_for('views.dashboard_test_login_page_function'))
  # ------------------------ invalid url_assessment_name end ------------------------
  # ------------------------ pull assessment graded obj start ------------------------
  db_assessment_graded_obj = CandidatesAssessmentGradedObj.query.filter_by(created_assessment_user_id_fk=current_user.id,candidate_email=url_email,assessment_name=url_assessment_name).order_by(CandidatesAssessmentGradedObj.created_timestamp.desc()).first()
  # ------------------------ pull assessment graded obj end ------------------------
  # ------------------------ redirect if no obj found start ------------------------
  if db_assessment_graded_obj == None:
    localhost_print_function('=========================================== candidates_assessment_i_answers_function END ===========================================')
    return redirect(url_for('views.dashboard_test_login_page_function'))
  # ------------------------ redirect if no obj found end ------------------------
  ui_answers_error_statement = ''
  assessment_info_dict = json.loads(db_assessment_graded_obj.assessment_obj)
  # ------------------------ stripe subscription status check start ------------------------
  user_obj = CandidatesUserObj.query.filter_by(id=current_user.id).first()
  fk_stripe_subscription_id = user_obj.fk_stripe_subscription_id
  stripe_subscription_obj = ''
  stripe_subscription_obj_status = 'not active'
  try:
    stripe_subscription_obj = stripe.Subscription.retrieve(fk_stripe_subscription_id)
    stripe_subscription_obj_status = stripe_subscription_obj.status
  except:
    pass
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ if subscription not paid start ------------------------
  user_sub_active = False
  if stripe_subscription_obj_status == 'active':
    user_sub_active = True
  if stripe_subscription_obj_status != 'active':
    for i_dict in assessment_info_dict['questions_arr_of_dicts']:
      i_dict['question_answers_list'] = ''
  # ------------------------ if subscription not paid end ------------------------
  localhost_print_function('=========================================== candidates_assessment_i_answers_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/candidates_page_templates/candidates_view_specific_page_templates/candidates_view_specific_answers_page_templates/index.html', error_message_to_html=ui_answers_error_statement, users_company_name_to_html = current_user.company_name, user_email_to_html=url_email, assessment_info_dict_to_html=assessment_info_dict,user_sub_active_to_html=user_sub_active)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views.route('/candidates/request', methods=['GET', 'POST'])
@login_required
def candidates_categories_request_function():
  localhost_print_function('=========================================== candidates_categories_request_function START ===========================================')
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_capacity_chosen')
  check_capacity_selected_value = query_result_arr_of_dicts[0]['capacity_id_fk']
  if check_capacity_selected_value == None or len(check_capacity_selected_value) == 0:
    localhost_print_function('=========================================== candidates_categories_request_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ individual redirect start ------------------------
  query_result_arr_of_dicts = select_general_function('select_if_desired_languages_captured')
  try:
    check_desired_languages_value = query_result_arr_of_dicts[0]['desired_languages']
  except:
    check_desired_languages_value = None
  if check_desired_languages_value == None or len(check_desired_languages_value) == 0:
    localhost_print_function('=========================================== candidates_categories_request_function END ===========================================')
    return redirect(url_for('views.capacity_page_function'))
  # ------------------------ individual redirect end ------------------------
  # ------------------------ if post method hit start ------------------------
  ui_request_error_statement = ''
  ui_request_success_statement = ''
  ui_requested = ''
  if request.method == 'POST':
    ui_requested = request.form.get('ui_requested')
    ui_requested = sanitize_candidate_ui_answer_text_function(ui_requested)
    if ui_requested == False:
      ui_request_error_statement = 'Please submit in correct format.'
    # ------------------------ create new user in db start ------------------------
    insert_new_row = CandidatesDesiredLanguagesObj(
      id=create_uuid_function('langs_'),
      created_timestamp=create_timestamp_function(),
      user_id_fk=current_user.id,
      desired_languages=ui_requested
    )
    db.session.add(insert_new_row)
    db.session.commit()
    # ------------------------ create new user in db end ------------------------
    ui_request_success_statement = 'Thank you, we will email you once the questions are available.'
  # ------------------------ if post method hit end ------------------------
  localhost_print_function('=========================================== candidates_categories_request_function END ===========================================')
  return render_template('candidates_page_templates/logged_in_page_templates/request_categories_page_templates/index.html', user=current_user, users_company_name_to_html=current_user.company_name, ui_requested_to_html=ui_requested, error_message_to_html=ui_request_error_statement, success_message_to_html=ui_request_success_statement)
# ------------------------ individual route end ------------------------
# ------------------------ routes logged in end ------------------------
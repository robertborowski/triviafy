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
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from website import db
from website.backend.candidates.user_inputs import alert_message_default_function_v2
from website.backend.candidates.browser import browser_response_set_cookie_function_v4, browser_response_set_cookie_function_v5
from website.models import GroupObj, ActivityASettingsObj, ActivityATestObj, UserDesiredCategoriesObj, ActivityACreatedQuestionsObj, ActivityATestGradedObj, UserObj, StripePaymentOptionsObj, EmailSentObj, StripeCheckoutSessionObj, ActivityAGroupQuestionsUsedObj, UserFeatureRequestObj, UserSignupFeedbackObj, UserCelebrateObj, ActivityBCreatedQuestionsObj, ActivityBGroupQuestionsUsedObj, ActivityBTestGradedObj, ActivityBTestObj
from website.backend.candidates.autogeneration import question_choices_function
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function, categories_tuple_function
from website.backend.candidates.datetime_manipulation import days_times_timezone_arr_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.backend.candidates.string_manipulation import all_employee_question_categories_sorted_function
from website.backend.candidates.user_inputs import sanitize_char_count_1_function, sanitize_create_question_options_function, sanitize_create_question_categories_function, sanitize_create_question_question_function, sanitize_create_question_option_e_function, sanitize_create_question_answer_function, get_special_characters_function
from website.backend.candidates.send_emails import send_email_template_function
import os
from website.backend.candidates.quiz import grade_quiz_function, pull_question_function, create_activity_function, compare_candence_vs_previous_quiz_function_v2
import json
from datetime import datetime
from website.backend.candidates.stripe import check_stripe_subscription_status_function_v2, convert_current_period_end_function
import stripe
from website.backend.candidates.datatype_conversion_manipulation import one_col_dict_to_arr_function
from website.backend.candidates.test_backend import get_test_winner
from website.backend.candidates.aws_manipulation import candidates_change_uploaded_image_filename_function, candidates_user_upload_image_checks_aws_s3_function
from website.backend.candidates.string_manipulation import breakup_email_function, capitalize_all_words_function
from website.backend.candidates.lists import get_team_building_activities_list_function, get_month_days_years_function, get_favorite_questions_function, get_marketing_list_function, get_dashboard_accordian_function, get_activity_a_products_function, get_activity_b_products_function
from website.backend.candidates.pull_create_logic import pull_create_group_obj_function, pull_latest_activity_test_obj_function, user_must_have_group_id_function, pull_create_activity_settings_obj_function, pull_group_obj_function, get_total_activity_closed_count_function
from website.backend.candidates.activity_supporting import activity_dashboard_function, activity_live_function, turn_activity_auto_on_function, dashboard_celebrations_function, get_all_teammate_ids_function
from website.backend.candidates.emailing import email_share_with_team_function
from website.backend.candidates.onboarding import onboarding_checks_function
from website.backend.candidates.settings_supporting import activity_settings_prep_function, activity_settings_post_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
employees_views_interior = Blueprint('employees_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/dashboard', methods=['GET', 'POST'])
@employees_views_interior.route('/dashboard/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def login_dashboard_page_function(url_redirect_code=None):
  # ------------------------ auto redirect checks start ------------------------
  """
  -The code will always hit this dashboard on login or create account. BUT BEFORE setting the cookie on the browser, we are going to auto redirect
  users this makes the UX better so they dont have to click, read, or think, just auto redirect. The downside is that you cannot set the cookie
  unless you know for sure where the user is ending up. So the redirected page will ALSO have to include the function that sets the cookie.
  Downside is repeating code but it is not for all pages, only for the pages that auto redirect on new account creation.
  -These pages will require the template_location_url variable
  """
  # ------------------------ onboarding checks start ------------------------
  onbaording_status = onboarding_checks_function(current_user)
  if onbaording_status == 'verify':
    return redirect(url_for('employees_views_interior.verify_email_function'))
  if onbaording_status == 'name':
    return redirect(url_for('employees_views_interior.employees_feedback_name_function'))
  if onbaording_status == 'primary':
    return redirect(url_for('employees_views_interior.employees_feedback_primary_function'))
  if onbaording_status == 'secondary':
    return redirect(url_for('employees_views_interior.employees_feedback_secondary_function'))
  if onbaording_status == 'birthday':
    return redirect(url_for('employees_views_interior.employees_feedback_year_month_function', url_feedback_code='birthday'))
  if onbaording_status == 'job_start_date':
    return redirect(url_for('employees_views_interior.employees_feedback_year_month_function', url_feedback_code='job_start_date'))
  if onbaording_status == 'marketing':
    return redirect(url_for('employees_views_interior.employees_feedback_marketing_function'))
  # ------------------------ onboarding checks end ------------------------
  # ------------------------ check if share with team email has been sent start ------------------------
  email_share_with_team_function(current_user)
  # ------------------------ check if share with team email has been sent end ------------------------
  # ------------------------ redirect codes start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  # ------------------------ redirect codes end ------------------------
  # ------------------------ page dict start ------------------------
  page_dict = {}
  # ------------------------ page dict end ------------------------
  # ------------------------ user must have a group id start ------------------------
  user_must_have_group_id_function(current_user)
  # ------------------------ user must have a group id end ------------------------
  # ------------------------ pull/create group start ------------------------
  db_group_obj = pull_create_group_obj_function(current_user)
  # ------------------------ pull/create group end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['group_stripe_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ free trial over redirect start ------------------------
  if page_dict['group_stripe_status'] != 'active':
    total_closed_count = get_total_activity_closed_count_function(current_user)
    if total_closed_count >= 2:
      return redirect(url_for('employees_views_interior.account_function', url_redirect_code='e25'))
  # ------------------------ free trial over redirect end ------------------------
  # ------------------------ dashboard supporting start ------------------------
  redirect_code, page_dict = activity_dashboard_function(current_user, page_dict, 'trivia', 'activity_type_a')
  if redirect_code == 'dashboard':
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ dashboard supporting end ------------------------
  # ------------------------ dashboard supporting start ------------------------
  redirect_code, page_dict = activity_dashboard_function(current_user, page_dict, 'picture_quiz', 'activity_type_a')
  if redirect_code == 'dashboard':
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ dashboard supporting end ------------------------
  # ------------------------ dashboard supporting start ------------------------
  redirect_code, page_dict = activity_dashboard_function(current_user, page_dict, 'icebreakers', 'activity_type_b')
  if redirect_code == 'dashboard':
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ dashboard supporting end ------------------------
  # ------------------------ dashboard supporting start ------------------------
  redirect_code, page_dict = dashboard_celebrations_function(current_user, page_dict)
  if redirect_code == 'dashboard':
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ dashboard supporting end ------------------------
  # ------------------------ subscription only activities start ------------------------
  if page_dict['group_stripe_status'] == 'active':
    pass
  # ------------------------ subscription only activities end ------------------------
  # ------------------------ get collapse list start ------------------------
  page_dict['activity_a_accordian_arr'], page_dict['activity_b_accordian_arr'] = get_dashboard_accordian_function()
  # ------------------------ get collapse list end ------------------------
  # ------------------------ if post start ------------------------
  if request.method == 'POST':
    try:
      # ------------------------ pull and assign to dict start ------------------------
      on_off_dict = {}
      # ------------------------ activity_type_a start ------------------------
      for i_index in range(len(page_dict['activity_a_accordian_arr'])):
        i_activity = page_dict['activity_a_accordian_arr'][i_index][1]
        i_activity_html = i_activity.capitalize()
        on_off_dict[i_activity] = request.form.get('flexActivity'+i_activity_html)
      # ------------------------ activity_type_a end ------------------------
      # ------------------------ activity_type_b start ------------------------
      for i_index in range(len(page_dict['activity_b_accordian_arr'])):
        i_activity = page_dict['activity_b_accordian_arr'][i_index][1]
        i_activity_html = i_activity.capitalize()
        on_off_dict[i_activity] = request.form.get('flexActivity'+i_activity_html)
      # ------------------------ activity_type_b end ------------------------
      # ------------------------ pull and assign to dict end ------------------------
      db_group_obj = pull_group_obj_function(current_user)
      # ------------------------ update db start ------------------------
      on_off_change_occured = False
      for k,v in on_off_dict.items():
        if k in db_group_obj.__table__.columns:
          if v == 'on' and getattr(db_group_obj, k) != True:
            setattr(db_group_obj, k, True)
            on_off_change_occured = True
          elif v == None and getattr(db_group_obj, k) != False:
            setattr(db_group_obj, k, False)
            on_off_change_occured = True
      if on_off_change_occured == True:
        db.session.commit()
    except:
      pass
    # ------------------------ update db end ------------------------
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ if post end ------------------------
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'employees/interior/dashboard/index.html'
  # ------------------------ for setting cookie end ------------------------
  localhost_print_function(' ------------- 100-dashboard start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-dashboard end ------------- ')
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, alert_message_dict_to_html=alert_message_dict, page_dict_to_html=page_dict)
  else:
    browser_response = browser_response_set_cookie_function_v4(current_user, template_location_url, alert_message_dict, page_dict)
    localhost_print_function(' ------------------------ login_dashboard_page_function END ------------------------ ')
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/verify/success/<url_verification_code>')
@employees_views_interior.route('/employees/verify/success/<url_verification_code>/<url_redirect_code>')
@login_required
def verification_code_clicked_function(url_redirect_code=None, url_verification_code=None):
  localhost_print_function(' ------------------------ verification_code_clicked_function start ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ verification start ------------------------
  if url_verification_code == None:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  redis_uuid_value = ''
  try:
    redis_uuid_value = redis_connection.get(url_verification_code).decode('utf-8')
  except:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  db_user_obj = UserObj.query.filter_by(id=redis_uuid_value).first()
  db_user_obj.verified_email = True
  db.session.commit()
  redis_connection.delete(url_verification_code)
  # ------------------------ verification end ------------------------
  localhost_print_function(' ------------------------ verification_code_clicked_function end ------------------------ ')
  return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s9'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/verify', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/verify/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def verify_email_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ verify_email_function start ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  page_dict['user_email'] = current_user.email
  output_subject = f'Verify Email: {current_user.email}'
  # ------------------------ check if verify email already sent start ------------------------
  db_email_obj = EmailSentObj.query.filter_by(to_email=current_user.email,subject=output_subject).first()
  # ------------------------ check if verify email already sent end ------------------------
  if db_email_obj == None or db_email_obj == []:
    # ------------------------ verification code store in redis start ------------------------
    verification_code = create_uuid_function('verify_')
    redis_connection.set(verification_code, current_user.id.encode('utf-8'))
    # ------------------------ verification code store in redis end ------------------------
    # ------------------------ auto send first email to employee start ------------------------
    guessed_name = breakup_email_function(current_user.email)
    try:
      output_to_email = current_user.email
      output_body = ''
      # ------------------------ get environment start ------------------------
      server_env = os.environ.get('TESTING', 'false')
      # ------------------------ get environment end ------------------------
      # ------------------------ localhost start ------------------------
      if server_env == 'true':
        output_body = f"<p>Hi {guessed_name},</p>\
                        <p>Please click the link below to verify your email address.</p>\
                        <p>Verify email link: http://127.0.0.1:80/employees/verify/success/{verification_code}</p>\
                        <p style='margin:0;'>Best,</p>\
                        <p style='margin:0;'>Triviafy Support Team</p>"
      # ------------------------ localhost end ------------------------
      # ------------------------ production start ------------------------
      else:
        output_body = f"<p>Hi {guessed_name},</p>\
                        <p>Please click the link below to verify your email address.</p>\
                        <p>Verify email link: https://triviafy.com/employees/verify/success/{verification_code}</p>\
                        <p style='margin:0;'>Best,</p>\
                        <p style='margin:0;'>Triviafy Support Team</p>"
      # ------------------------ production end ------------------------
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
    # ------------------------ auto send first email to employee end ------------------------
    # ------------------------ insert email to db start ------------------------
    try:
      new_row_email = EmailSentObj(
        id = create_uuid_function('email_'),
        created_timestamp = create_timestamp_function(),
        from_user_id_fk = current_user.id,
        to_email = output_to_email,
        subject = output_subject,
        body = output_body
      )
      db.session.add(new_row_email)
      db.session.commit()
    except:
      pass
    # ------------------------ insert email to db end ------------------------
  # ------------------------ resend email start ------------------------
  if request.method == 'POST':
    # ------------------------ delete all existing redis keys for this uuid start ------------------------
    redis_keys = redis_connection.keys()
    for i_key in redis_keys:    
      if 'verify' in str(i_key):
        redis_value = redis_connection.get(i_key).decode('utf-8')
        if redis_value == current_user.id:
          redis_connection.delete(i_key)
    # ------------------------ delete all existing redis keys for this uuid end ------------------------
    # ------------------------ create new verification key start ------------------------
    new_verification_code = create_uuid_function('verify_')
    redis_connection.set(new_verification_code, current_user.id.encode('utf-8'))
    # ------------------------ create new verification key end ------------------------
    # ------------------------ send email start ------------------------
    guessed_name = breakup_email_function(current_user.email)
    try:
      output_to_email = current_user.email
      output_body = ''
      # ------------------------ get environment start ------------------------
      server_env = os.environ.get('TESTING', 'false')
      # ------------------------ get environment end ------------------------
      # ------------------------ localhost start ------------------------
      if server_env == 'true':
        output_body = f"<p>Hi {guessed_name},</p>\
                      <p>Please click the link below to verify your email address.</p>\
                      <p>Verify email link: http://127.0.0.1:80/employees/verify/success/{new_verification_code}</p>\
                      <p style='margin:0;'>Best,</p>\
                      <p style='margin:0;'>Triviafy Support Team</p>"
      # ------------------------ localhost end ------------------------
      # ------------------------ production start ------------------------
      else:
        output_body = f"<p>Hi {guessed_name},</p>\
                        <p>Please click the link below to verify your email address.</p>\
                        <p>Verify email link: https://triviafy.com/employees/verify/success/{new_verification_code}</p>\
                        <p style='margin:0;'>Best,</p>\
                        <p style='margin:0;'>Triviafy Support Team</p>"
      # ------------------------ production end ------------------------
      send_email_template_function(output_to_email, output_subject, output_body)
      # ------------------------ insert email to db start ------------------------
      try:
        new_row_email = EmailSentObj(
          id = create_uuid_function('email_'),
          created_timestamp = create_timestamp_function(),
          from_user_id_fk = current_user.id,
          to_email = output_to_email,
          subject = output_subject,
          body = output_body
        )
        db.session.add(new_row_email)
        db.session.commit()
      except:
        pass
      # ------------------------ insert email to db end ------------------------
    except:
      pass
    # ------------------------ send email end ------------------------
    pass
  # ------------------------ resend email end ------------------------
  localhost_print_function(' ------------------------ verify_email_function end ------------------------ ')
  return render_template('employees/interior/verify_email/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/create/activity')
@employees_views_interior.route('/create/activity/')
@employees_views_interior.route('/create/activity/<url_activity_type>')
@employees_views_interior.route('/create/activity/<url_activity_type>/')
@employees_views_interior.route('/create/activity/<url_activity_type>/<url_activity_code>')
@employees_views_interior.route('/create/activity/<url_activity_type>/<url_activity_code>/')
@login_required
def create_new_activity_function(url_activity_code=None, url_activity_type=None):
  # ------------------------ if no activity error start ------------------------
  if url_activity_code == None or url_activity_code == '' or url_activity_type == None or url_activity_type == '':
    return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e24'))
  # ------------------------ if no activity error end ------------------------
  # ------------------------ turn on auto start stop start ------------------------
  turn_activity_auto_on_function(current_user,url_activity_code)
  # ------------------------ turn on auto start stop end ------------------------
  # ------------------------ pull latest activity start ------------------------
  db_tests_obj = pull_latest_activity_test_obj_function(current_user,url_activity_code, url_activity_type)
  # ------------------------ pull latest activity end ------------------------
  # ------------------------ if none yet created then create immediately + redirect start ------------------------
  if db_tests_obj == None:
    create_activity_function(current_user=current_user, activity_code=url_activity_code, activity_type=url_activity_type, immediate=True)
    return redirect(url_for('employees_views_interior.activity_contest_function', url_activity_code=url_activity_code, url_activity_type=url_activity_type))
  # ------------------------ if none yet created then create immediately + redirect end ------------------------
  else:
    activity_cadence_check = compare_candence_vs_previous_quiz_function_v2(current_user, db_tests_obj, url_activity_code, url_activity_type)
    if activity_cadence_check == True:
      create_activity_function(current_user=current_user, activity_code=url_activity_code, activity_type=url_activity_type)
      return redirect(url_for('employees_views_interior.activity_contest_function', url_activity_code=url_activity_code, url_activity_type=url_activity_type))
  return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/request', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/request/<url_activity_code>', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/request/<url_activity_code>/<url_redirect_code>', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/request/<url_redirect_code>/<url_activity_code>', methods=['GET', 'POST'])
@login_required
def employees_categories_request_function(url_redirect_code=None, url_activity_code=None):
  localhost_print_function(' ------------------------ employees_categories_request_function START ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ pull/create latest test start ------------------------
  user_group_id = GroupObj.query.filter_by(fk_company_name=current_user.company_name).order_by(GroupObj.created_timestamp.desc()).first()
  db_tests_obj = ActivityATestObj.query.filter_by(fk_group_id=user_group_id.public_group_id,product='trivia').order_by(ActivityATestObj.created_timestamp.desc()).first()
  first_activity_check = False
  if db_tests_obj == None or db_tests_obj == []:
    pass
  else:
    first_activity_check = True
  page_dict[url_activity_code+'_first_created'] = first_activity_check
  # ------------------------ pull/create latest test end ------------------------
  # ------------------------ if post method hit start ------------------------
  ui_requested = ''
  if request.method == 'POST':
    ui_requested = request.form.get('ui_requested')
    ui_requested = sanitize_char_count_1_function(ui_requested)
    if ui_requested == False:
      return redirect(url_for('employees_views_interior.employees_categories_request_function', url_redirect_code='e5'))
    else:
      # ------------------------ create new user in db start ------------------------
      insert_new_row = UserDesiredCategoriesObj(
        id=create_uuid_function('cat_'),
        created_timestamp=create_timestamp_function(),
        user_id_fk=current_user.id,
        desired_categories=ui_requested
      )
      db.session.add(insert_new_row)
      db.session.commit()
      # ------------------------ create new user in db end ------------------------
      # ------------------------ email self start ------------------------
      try:
        output_to_email = os.environ.get('TRIVIAFY_NOTIFICATIONS_EMAIL')
        output_subject = f'Triviafy - Employees Requested Category - {current_user.email}'
        output_body = f"Hi there,\n\nRequester: {current_user.email}\nRequested: '{ui_requested}'\n\nBest,\nTriviafy"
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self end ------------------------
      return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s1'))
  # ------------------------ if post method hit end ------------------------
  localhost_print_function(' ------------------------ employees_categories_request_function END ------------------------ ')
  return render_template('employees/interior/request_categories/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/activity/settings/<url_activity_type>', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/settings/<url_activity_type>/', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/settings/<url_activity_type>/<url_activity_code>', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/settings/<url_activity_type>/<url_activity_code>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def activity_settings_function(url_activity_code=None, url_redirect_code=None, url_activity_type=None):
  # ------------------------ if no activity error start ------------------------
  if url_activity_code == None or url_activity_code == '' or url_activity_type == None or url_activity_type == '':
    return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e24'))
  # ------------------------ if no activity error end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ activity type start ------------------------
  page_dict['url_activity_type'] = url_activity_type
  # ------------------------ activity type end ------------------------
  # ------------------------ get current group settings start ------------------------
  db_activity_settings_obj = pull_create_activity_settings_obj_function(current_user, url_activity_code, url_activity_type)
  db_activity_settings_dict = arr_of_dict_all_columns_single_item_function(db_activity_settings_obj)
  # ------------------------ get current group settings end ------------------------
  # ------------------------ settings prep start ------------------------
  page_dict = activity_settings_prep_function(page_dict, url_activity_code, db_activity_settings_dict, url_activity_type)
  # ------------------------ settings prep end ------------------------
  if request.method == 'POST':
    ui_selected_categories = []
    try:
      # ------------------------ get ui start ------------------------
      ui_start_day = request.form.get('radio_start_day')
      ui_start_time = request.form.get('radio_start_time')
      ui_end_day = request.form.get('radio_end_day')
      ui_end_time = request.form.get('radio_end_time')
      ui_timezone = request.form.get('radio_timezone')
      ui_cadence = request.form.get('radio_candence')
      ui_total_questions = request.form.get('radio_total_questions')
      ui_question_type = request.form.get('radio_question_type')
      ui_select_all_categories = request.form.get('flexSwitchCheckDefault_02')
      ui_selected_categories = request.form.getlist('uiSelectedCategories')
      # ------------------------ get ui end ------------------------
    except:
      pass
    # ------------------------ settings post start ------------------------
    post_result, page_dict = activity_settings_post_function(page_dict, url_activity_code, url_activity_type, db_activity_settings_obj, db_activity_settings_dict, ui_start_day, ui_start_time, ui_end_day, ui_end_time, ui_timezone, ui_cadence, ui_total_questions, ui_question_type, ui_select_all_categories, ui_selected_categories)
    if post_result == 'dropdown_error':
      return redirect(url_for('employees_views_interior.activity_settings_function', url_activity_code=url_activity_code, url_redirect_code='e6'))
    if post_result == 'category_error':
      return redirect(url_for('employees_views_interior.activity_settings_function', url_activity_code=url_activity_code, url_redirect_code='e6'))
    if post_result == 'select_error':
      return redirect(url_for('employees_views_interior.activity_settings_function', url_activity_code=url_activity_code, url_redirect_code='e7'))
    if post_result == 'overlap_error':
      return redirect(url_for('employees_views_interior.activity_settings_function', url_activity_code=url_activity_code, url_redirect_code='e8'))
    if post_result == 'success_code':
      return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s2'))
    if post_result == 'no_change':
      return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='i1'))
    # ------------------------ settings post end ------------------------
  localhost_print_function(' ------------- 100-settings start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-settings end ------------- ')
  return render_template('employees/interior/schedule/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/activity/settings/default')
@employees_views_interior.route('/activity/settings/default/')
@employees_views_interior.route('/activity/settings/default/<url_activity_type>')
@employees_views_interior.route('/activity/settings/default/<url_activity_type>/')
@employees_views_interior.route('/activity/settings/default/<url_activity_type>/<url_activity_code>')
@employees_views_interior.route('/activity/settings/default/<url_activity_type>/<url_activity_code>/')
@login_required
def activity_default_settings_function(url_activity_code=None, url_activity_type=None):
  # ------------------------ if no activity error start ------------------------
  if url_activity_code == None or url_activity_code == '' or url_activity_type == None or url_activity_type == '':
    return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e24'))
  # ------------------------ if no activity error end ------------------------
  try:
    db_activity_settings_obj = pull_create_activity_settings_obj_function(current_user, url_activity_code, url_activity_type)
    db_activity_settings_obj.timezone = 'EST'
    db_activity_settings_obj.start_day = 'Monday'
    db_activity_settings_obj.start_time = '12 PM'
    db_activity_settings_obj.end_day = 'Thursday'
    db_activity_settings_obj.end_time = '1 PM'
    db_activity_settings_obj.cadence = 'Weekly'
    if url_activity_type == 'activity_type_a':
      db_activity_settings_obj.total_questions = 10
      db_activity_settings_obj.question_type = 'Mixed'
    db.session.commit()
  except:
    pass
  return redirect(url_for('employees_views_interior.activity_settings_function', url_activity_code=url_activity_code, url_activity_type=url_activity_type, url_redirect_code='s11'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>/replace/<url_test_id>/<url_question_number>', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>/replace/<url_test_id>/<url_question_number>/', methods=['GET', 'POST'])
@login_required
def employees_test_id_replace_question_function(url_activity_code=None, url_test_id=None, url_question_number=None, url_activity_type=None):
  localhost_print_function(' ------------------------ employees_test_id_replace_question_function START ------------------------ ')
  # ------------------------ redirect start ------------------------
  if url_activity_code == None or url_test_id == None or url_test_id == '' or url_question_number == None or url_question_number == '':
    return redirect(url_for('employees_views_interior.activity_contest_function', url_activity_type=url_activity_type))
  # ------------------------ redirect end ------------------------
  # ------------------------ get group latest test start ------------------------
  db_tests_obj = ActivityATestObj.query.filter_by(fk_group_id=current_user.group_id,product=url_activity_code).order_by(ActivityATestObj.created_timestamp.desc()).first()
  db_tests_dict = arr_of_dict_all_columns_single_item_function(db_tests_obj)
  # ------------------------ get group latest test end ------------------------
  # ------------------------ identify question to replace start ------------------------
  question_ids_str_current = db_tests_dict['question_ids']
  question_ids_str_current_arr = question_ids_str_current.split(',')
  question_id_to_replace = question_ids_str_current_arr[int(url_question_number)-1]
  # ------------------------ identify question to replace end ------------------------
  # ------------------------ get new question never asked before start ------------------------
  categories = db_tests_dict['categories']
  new_question_id = pull_question_function(current_user.group_id, categories, url_activity_code)
  # ------------------------ get new question never asked before end ------------------------
  # ------------------------ replace id in test table start ------------------------
  question_ids_str_replaced = question_ids_str_current.replace(question_id_to_replace, new_question_id)
  try:
    db_tests_obj.question_ids = question_ids_str_replaced
    db.session.commit()
  except:
    pass
  # ------------------------ replace id in test table end ------------------------
  # ------------------------ replace id in question asked table start ------------------------
  db_question_used_obj = ActivityAGroupQuestionsUsedObj.query.filter_by(fk_group_id=current_user.group_id, fk_test_id=db_tests_obj.id, fk_question_id=question_id_to_replace,product=url_activity_code).first()
  try:
    db_question_used_obj.fk_question_id = new_question_id
    db.session.commit()
  except:
    pass
  # ------------------------ replace id in question asked table end ------------------------
  # ------------------------ check if old question graded/remove start ------------------------
  try:
    db_test_graded_obj = ActivityATestGradedObj.query.filter_by(fk_group_id=current_user.group_id, fk_test_id=db_tests_obj.id,product=url_activity_code).all()
    for i_obj in db_test_graded_obj:
      db_test_graded_dict = arr_of_dict_all_columns_single_item_function(i_obj)
      tracking_ids_arr_of_dicts = json.loads(db_test_graded_dict['test_obj'])
      for i in range(len(tracking_ids_arr_of_dicts)):
        current_question_id = tracking_ids_arr_of_dicts[i]['id']
        if current_question_id == question_id_to_replace:
          tracking_ids_arr_of_dicts.pop(i)
          break
      i_obj.test_obj = json.dumps(tracking_ids_arr_of_dicts)
      db.session.commit()
  except:
    pass
  # ------------------------ check if old question graded/remove end ------------------------
  localhost_print_function(' ------------------------ employees_test_id_replace_question_function end ------------------------ ')
  return redirect(url_for('employees_views_interior.activity_contest_function', url_test_id=url_test_id, url_question_number=url_question_number, url_redirect_code='e23', url_activity_code=url_activity_code, url_activity_type='activity_type_a'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>/', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>/<url_test_id>', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>/<url_test_id>/', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>/<url_test_id>/<url_question_number>', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>/<url_test_id>/<url_question_number>/', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>/<url_test_id>/<url_question_number>/<url_initial_page_load>', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>/<url_test_id>/<url_question_number>/<url_initial_page_load>/', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>/<url_test_id>/<url_question_number>/<url_initial_page_load>/<url_redirect_code>', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>/<url_test_id>/<url_question_number>/<url_redirect_code>', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/<url_activity_type>/<url_activity_code>/<url_test_id>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def activity_contest_function(url_redirect_code=None, url_test_id=None, url_question_number=None, url_initial_page_load=None, url_activity_code=None, url_activity_type=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['group_stripe_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ activity a live start ------------------------
  page_dict, function_result = activity_live_function(page_dict, current_user, url_test_id, url_question_number, url_initial_page_load, url_activity_code, url_activity_type)
  if function_result == 'no_activity':
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  if function_result == 'init_activity':
    return redirect(url_for('employees_views_interior.activity_contest_function', url_test_id=page_dict['latest_test_id'], url_question_number='1', url_initial_page_load='init', url_activity_code=url_activity_code, url_activity_type=url_activity_type))
  if function_result == 'replace_activity':
    return redirect(url_for('employees_views_interior.activity_settings_function', url_redirect_code='e22', url_activity_code=url_activity_code, url_activity_type=url_activity_type))
  if function_result == 'redirect_earliest_unanswered':
    return redirect(url_for('employees_views_interior.activity_contest_function', url_test_id=url_test_id, url_question_number=page_dict['earliest_unanswered_question_number'], url_activity_code=url_activity_code, url_activity_type=url_activity_type))
  if function_result == 'redirect_earliest_unanswered':
    return redirect(url_for('employees_views_interior.activity_contest_function', url_test_id=page_dict['latest_test_id'], url_question_number='1', url_activity_type=url_activity_type))
  # ------------------------ activity a live end ------------------------
  if page_dict['view_as_archive'] == False: # no user inputs should be accepted since this test is closed.
    # ------------------------ ui post start ------------------------
    if request.method == 'POST':
      # ------------------------ activity_type_a start ------------------------
      if url_activity_type == 'activity_type_a':
        # ------------------------ user input start ------------------------
        ui_answer = ''
        ui_answer_is_correct = False
        db_tests_obj = ActivityATestObj.query.filter_by(id=url_test_id).first()
        # ------------------------ user input - fill in the blank start ------------------------
        if page_dict['db_question_dict']['desired_question_type'] == 'Fill in the blank':
          ui_answer = request.form.get('ui_answer_fitb')
          # ------------------------ validate ui start ------------------------
          if len(ui_answer) < 1 or len(ui_answer) > 280:
            return redirect(url_for('employees_views_interior.activity_contest_function', url_test_id=url_test_id, url_question_number=str(url_question_number), url_redirect_code='e6', url_activity_type=url_activity_type))
          # ------------------------ validate ui end ------------------------
          # ------------------------ grade ui start ------------------------
          grade_quiz_function(ui_answer, url_test_id, db_tests_obj.total_questions, url_question_number, page_dict['db_question_dict'], current_user.id, current_user.group_id, url_activity_code)
          # ------------------------ grade ui end ------------------------
        # ------------------------ user input - fill in the blank end ------------------------
        # ------------------------ user input - multiple choice start ------------------------
        if page_dict['db_question_dict']['desired_question_type'] == 'Multiple choice':
          ui_answer = request.form.get('ui_answer_mcq')
          # ------------------------ validate ui start ------------------------
          allowed_answers_arr = ['a', 'b', 'c', 'd', 'e']
          if ui_answer.lower() not in allowed_answers_arr:
            return redirect(url_for('employees_views_interior.activity_contest_function', url_test_id=url_test_id, url_question_number=str(url_question_number), url_redirect_code='e6', url_activity_type=url_activity_type))
          # ------------------------ validate ui start ------------------------
          # ------------------------ grade ui start ------------------------
          grade_quiz_function(ui_answer, url_test_id, db_tests_obj.total_questions, url_question_number, page_dict['db_question_dict'], current_user.id, current_user.group_id, url_activity_code)
          # ------------------------ grade ui end ------------------------
        # ------------------------ user input - multiple choice end ------------------------
        # ------------------------ user input end ------------------------
        if page_dict['next_question_number'] == 'submit':
          # ------------------------ pull latest graded start ------------------------
          db_test_grading_obj = ActivityATestGradedObj.query.filter_by(fk_test_id=url_test_id, fk_user_id=current_user.id,product=url_activity_code).first()
          db_test_grading_dict = arr_of_dict_all_columns_single_item_function(db_test_grading_obj)
          # ------------------------ pull latest graded end ------------------------
          if db_test_grading_dict['total_questions'] == db_test_grading_dict['graded_count']:
            return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s4'))
          else:
            unanswered_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
            for i in json.loads(db_test_grading_dict['test_obj']):
              already_answered_question_number = str(i['question_number'])
              if already_answered_question_number in unanswered_arr:
                unanswered_arr.remove(already_answered_question_number)
            return redirect(url_for('employees_views_interior.activity_contest_function', url_test_id=url_test_id, url_question_number=unanswered_arr[0], url_activity_type=url_activity_type, url_activity_code=url_activity_code))
        else:
          return redirect(url_for('employees_views_interior.activity_contest_function', url_test_id=url_test_id, url_question_number=str(int(url_question_number)+1), url_activity_code=url_activity_code, url_activity_type=url_activity_type))
      # ------------------------ activity_type_a end ------------------------
      # ------------------------ activity_type_b start ------------------------
      if url_activity_type == 'activity_type_b':
        # ------------------------ get user inputs start ------------------------
        ui_answer = request.form.get('ui_answer')
        # ------------------------ get user inputs end ------------------------
        # ------------------------ sanatize inputs start ------------------------
        if len(ui_answer) < 1 or len(ui_answer) > 500:
          return redirect(url_for('employees_views_interior.activity_contest_function', url_redirect_code='e19', url_test_id=url_test_id, url_activity_code=url_activity_code, url_activity_type=url_activity_type))
        special_characters_arr = get_special_characters_function()
        for i in ui_answer:
          if i in special_characters_arr:
            return redirect(url_for('employees_views_interior.activity_contest_function', url_redirect_code='e18', url_test_id=url_test_id, url_activity_code=url_activity_code, url_activity_type=url_activity_type))
        # ------------------------ sanatize inputs end ------------------------
        # ------------------------ pull latest answer if exists + replace start ------------------------
        db_test_grading_obj = ActivityBTestGradedObj.query.filter_by(fk_test_id=url_test_id, fk_user_id=current_user.id).first()
        if db_test_grading_obj != None and db_test_grading_obj != '':
          db_test_grading_obj.test_obj = ui_answer
          db.session.commit()
        # ------------------------ pull latest answer if exists + replace end ------------------------
        # ------------------------ insert to db start ------------------------
        if db_test_grading_obj == None or db_test_grading_obj == '':
          # ------------------------ insert to db start ------------------------
          try:
            new_row = ActivityBTestGradedObj(
              id = create_uuid_function('testg_'),
              created_timestamp = create_timestamp_function(),
              fk_group_id = current_user.group_id,
              fk_user_id = current_user.id,
              fk_test_id = url_test_id,
              status = 'complete',
              test_obj = ui_answer,
              product = url_activity_code
            )
            db.session.add(new_row)
            db.session.commit()
          except:
            pass
          # ------------------------ insert to db end ------------------------
        # ------------------------ insert to db end ------------------------
        return redirect(url_for('employees_views_interior.activity_contest_function', url_redirect_code='s12', url_test_id=url_test_id, url_activity_code=url_activity_code, url_activity_type=url_activity_type))
      # ------------------------ activity_type_b end ------------------------
    # ------------------------ ui post end ------------------------
  localhost_print_function(' ------------- 100-activity start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-activity end ------------- ')
  if url_activity_type == 'activity_type_a':
    return render_template('employees/interior/activity_type_a/index.html', page_dict_to_html=page_dict)
  elif url_activity_type == 'activity_type_b':
    return render_template('employees/interior/activity_type_b/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/archive')
@employees_views_interior.route('/archive/<url_redirect_code>')
@login_required
def activity_archive_function(url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ pull all tests for group start ------------------------
  all_tests_obj_arr = []
  db_tests_a_obj = ActivityATestObj.query.filter_by(fk_group_id=current_user.group_id,status='Closed').order_by(ActivityATestObj.created_timestamp.desc()).all()
  all_tests_obj_arr.append(db_tests_a_obj)
  db_tests_b_obj = ActivityBTestObj.query.filter_by(fk_group_id=current_user.group_id,status='Closed').order_by(ActivityBTestObj.created_timestamp.desc()).all()
  all_tests_obj_arr.append(db_tests_b_obj)
  # ------------------------ pull all tests for group end ------------------------
  # ------------------------ turn sql obj into arr of dicts start ------------------------
  tests_arr_of_dicts = []
  for_range_len_index_arr = ['activity_type_a','activity_type_b']
  for i_count in range(len(all_tests_obj_arr)):
    for i_obj in all_tests_obj_arr[i_count]:
      i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
      i_dict['url_activity_type'] = for_range_len_index_arr[i_count]
      tests_arr_of_dicts.append(i_dict)
  # ------------------------ turn sql obj into arr of dicts end ------------------------
  # ------------------------ loop through tests and assign variables per test start ------------------------
  total_tests = len(tests_arr_of_dicts)
  current_test = total_tests
  for i in tests_arr_of_dicts:
    i['test_number'] = current_test
    i['test_winner'], i['test_winner_score'] = get_test_winner(i['id'])
    current_test -= 1
  page_dict['tests_arr_of_dicts'] = tests_arr_of_dicts
  # ------------------------ loop through tests and assign variables per test end ------------------------
  localhost_print_function(' ------------- 100-archive start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-archive end ------------- ')
  return render_template('employees/interior/activity_archive/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/leaderboard')
@employees_views_interior.route('/leaderboard/<url_redirect_code>')
@login_required
def group_leaderboard_function(url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ get current users from company start ------------------------
  users_arr_of_dicts = []
  db_users_obj = UserObj.query.filter_by(group_id=current_user.group_id).order_by(UserObj.email.asc()).all()
  for i in db_users_obj:
    i_dict = {}
    user_id = i.id
    user_name = i.name
    # ------------------------ get total correct start ------------------------
    total_correct = int(0)
    db_test_grading_obj = ActivityATestGradedObj.query.filter_by(fk_user_id=user_id).all()
    for j in db_test_grading_obj:
      # ------------------------ check if test is closed start ------------------------
      db_tests_obj = ActivityATestObj.query.filter_by(id=j.fk_test_id).first()
      if db_tests_obj.status == 'Closed':
        total_correct += int(j.correct_count)
      # ------------------------ check if test is closed end ------------------------
    # ------------------------ get total correct end ------------------------
    i_dict['user_id'] = user_id
    i_dict['user_name'] = user_name
    i_dict['total_correct'] = total_correct
    i_dict['total_wins'] = int(0)
    users_arr_of_dicts.append(i_dict)
  # ------------------------ get current users from company end ------------------------
  # ------------------------ pull all tests for group start ------------------------
  db_tests_obj = ActivityATestObj.query.filter_by(fk_group_id=current_user.group_id).order_by(ActivityATestObj.created_timestamp.desc()).all()
  # ------------------------ pull all tests for group end ------------------------
  # ------------------------ pull test winner start ------------------------
  for i in db_tests_obj:
    test_winner, test_winner_score = get_test_winner(i.id, True)
    for j in users_arr_of_dicts:
      if j['user_id'] == test_winner:
        j['total_wins'] += int(1)
        break
  # ------------------------ pull test winner end ------------------------
  page_dict['users_arr_of_dicts'] = users_arr_of_dicts
  return render_template('employees/interior/leaderboard/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/celebrations')
@employees_views_interior.route('/celebrations/<url_redirect_code>')
@login_required
def activity_celebrations_function(url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ pull all teammates start ------------------------
  teammates_arr_of_dict = []
  teammate_ids_arr = []
  db_teammates_obj = UserObj.query.filter_by(group_id=current_user.group_id).all()
  for i_obj in db_teammates_obj:
    i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
    teammates_arr_of_dict.append(i_dict)
    teammate_ids_arr.append(i_dict['id'])
  # ------------------------ pull all teammates end ------------------------
  # ------------------------ pull all team celebrations start ------------------------
  db_celebrations_obj = UserCelebrateObj.query.filter_by(fk_group_id=current_user.group_id).all()
  # ------------------------ pull all team celebrations end ------------------------
  # ------------------------ data for table start ------------------------
  query_celebrations_arr_of_dicts = []
  for i_celebrate_obj in db_celebrations_obj:
    i_celebrate_dict = arr_of_dict_all_columns_single_item_function(i_celebrate_obj)
    for i_user_dict in teammates_arr_of_dict:
      if i_celebrate_dict['fk_user_id'] == i_user_dict['id']:
        i_celebrate_dict['name'] = i_user_dict['name']
    query_celebrations_arr_of_dicts.append(i_celebrate_dict)
  page_dict['query_celebrations_arr_of_dicts'] = query_celebrations_arr_of_dicts
  # ------------------------ data for table end ------------------------
  localhost_print_function(' ------------- 100-celebrations start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-celebrations end ------------- ')
  return render_template('employees/interior/celebrations/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/subscription/success')
@employees_views_interior.route('/employees/subscription/success/')
@login_required
def employees_subscription_success_function():
  localhost_print_function(' ------------------------ employees_subscription_success_function start ------------------------ ')
  # ------------------------ get from db start ------------------------
  db_checkout_session_obj = StripeCheckoutSessionObj.query.filter_by(fk_user_id=current_user.id,status='draft').order_by(StripeCheckoutSessionObj.created_timestamp.desc()).first()
  # ------------------------ get from db end ------------------------
  # ------------------------ if not found start ------------------------
  if db_checkout_session_obj == None or db_checkout_session_obj == '' or db_checkout_session_obj == False:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ if not found end ------------------------
  # ------------------------ get desired start ------------------------
  fk_checkout_session_id = db_checkout_session_obj.fk_checkout_session_id
  # ------------------------ get desired end ------------------------
  # ------------------------ stripe lookup start ------------------------
  stripe_checkout_session_obj = stripe.checkout.Session.retrieve(fk_checkout_session_id)
  # ------------------------ if not found start ------------------------
  if stripe_checkout_session_obj == None:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ if not found end ------------------------
  # ------------------------ if not finalized start ------------------------
  stripe_checkout_session_payment_status = stripe_checkout_session_obj.payment_status
  if stripe_checkout_session_payment_status != 'paid':
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ if not finalized end ------------------------
  stripe_customer_id = stripe_checkout_session_obj.customer
  employees_fk_stripe_subscription_id = stripe_checkout_session_obj.subscription
  # ------------------------ stripe lookup end ------------------------
  # ------------------------ update db start ------------------------
  user_obj = UserObj.query.filter_by(id=current_user.id).first()
  user_obj.fk_stripe_customer_id = stripe_customer_id
  user_obj.employees_fk_stripe_subscription_id = employees_fk_stripe_subscription_id
  db_checkout_session_obj.status = 'final'
  db.session.commit()
  # ------------------------ update db end ------------------------
  # ------------------------ email self start ------------------------
  try:
    output_to_email = os.environ.get('TRIVIAFY_NOTIFICATIONS_EMAIL')
    output_subject = f'New Subscription - {user_obj.email}'
    output_body = f"Hi there,\n\nNew user subscribed: {user_obj.email} \n\nBest,\nTriviafy"
    send_email_template_function(output_to_email, output_subject, output_body)
  except:
    pass
  # ------------------------ email self end ------------------------
  localhost_print_function(' ------------------------ employees_subscription_success_function end ------------------------ ')
  return redirect(url_for('employees_views_interior.account_function', url_redirect_code='s5'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/account', methods=['GET', 'POST'])
@employees_views_interior.route('/account/', methods=['GET', 'POST'])
@employees_views_interior.route('/account/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def account_function(url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['group_stripe_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ get current plan from stripe start ------------------------
  current_plan_type = 'Free'
  stripe_current_period_end = ''
  if stripe_subscription_obj_status == 'not active':
    pass
  if stripe_subscription_obj_status == 'active':
    try:
      stripe_subscription_obj = stripe.Subscription.retrieve(current_user.employees_fk_stripe_subscription_id)
      stripe_current_period_end = convert_current_period_end_function(stripe_subscription_obj)
      stripe_subscription_current_price_id = stripe_subscription_obj.plan.id
      db_capacity_obj = StripePaymentOptionsObj.query.filter_by(fk_stripe_price_id=stripe_subscription_current_price_id).first()
      current_plan_type = db_capacity_obj.name
    except:
      current_plan_type = 'Free'
  page_dict['stripe_current_plan_type'] = current_plan_type
  page_dict['stripe_current_period_end'] = stripe_current_period_end
  # ------------------------ get current plan from stripe end ------------------------
  # ------------------------ get current user info start ------------------------
  page_dict['current_user_email'] = current_user.email
  page_dict['current_user_company_name'] = current_user.company_name
  # ------------------------ get current user info end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    # ------------------------ post uiMessage start ------------------------
    ui_message = request.form.get('uiMessage')
    if ui_message != None and ui_message != '' and ui_message != []:
      ui_message = sanitize_create_question_options_function(ui_message)
      if ui_message == False:
        return redirect(url_for('employees_views_interior.account_function', url_redirect_code='e6'))
      else:
        # ------------------------ email self start ------------------------
        try:
          output_to_email = os.environ.get('TRIVIAFY_SUPPORT_EMAIL')
          output_subject = f'Triviafy - Contact Message From: {current_user.email}'
          output_body = f"Hi there,\n\nFrom: {current_user.email}\nMessage: {ui_message}\n\nBest,\nTriviafy"
          send_email_template_function(output_to_email, output_subject, output_body)
        except:
          pass
        # ------------------------ email self end ------------------------
        # ------------------------ insert email to db start ------------------------
        try:
          new_row_email = EmailSentObj(
            id = create_uuid_function('email_'),
            created_timestamp = create_timestamp_function(),
            from_user_id_fk = current_user.id,
            to_email = output_to_email,
            subject = output_subject,
            body = output_body
          )
          db.session.add(new_row_email)
          db.session.commit()
        except:
          pass
        # ------------------------ insert email to db end ------------------------
        return redirect(url_for('employees_views_interior.account_function', url_redirect_code='s1'))
    # ------------------------ post uiMessage end ------------------------
    # ------------------------ post uiSubscriptionSelected start ------------------------
    # ------------------------ delete all previous checkout drafts start ------------------------
    StripeCheckoutSessionObj.query.filter_by(fk_user_id=current_user.id,status='draft').delete()
    # ------------------------ delete all previous checkout drafts end ------------------------
    ui_subscription_selected = request.form.get('uiSubscriptionSelected')
    # ------------------------ postman checks start ------------------------
    try:
      if len(ui_subscription_selected) != 2:
        ui_subscription_selected = None
    except:
      ui_subscription_selected = None
    # ------------------------ postman checks end ------------------------
    # ------------------------ valid input check start ------------------------
    query_result_arr_of_dicts = select_general_function('select_all_capacity_options_employees')
    capacity_options_arr = one_col_dict_to_arr_function(query_result_arr_of_dicts)
    if ui_subscription_selected not in capacity_options_arr:
      ui_subscription_selected = None
    # ------------------------ valid input check end ------------------------
    if ui_subscription_selected != None:
      # ------------------------ db get price id start ------------------------
      db_capacity_obj = StripePaymentOptionsObj.query.filter_by(id=ui_subscription_selected).first()
      server_env = os.environ.get('TESTING', 'false')
      fk_stripe_price_id = ''
      if server_env == 'true':
        fk_stripe_price_id = db_capacity_obj.fk_stripe_price_id_testing
      else:
        fk_stripe_price_id = db_capacity_obj.fk_stripe_price_id
      # ------------------------ db get price id end ------------------------
      # ------------------------ stripe checkout start ------------------------
      try:
        checkout_session = None
        # ------------------------ localhost testing start ------------------------
        if server_env == 'true':
          checkout_session = stripe.checkout.Session.create(
            line_items=[
              {
              'price': fk_stripe_price_id,
              'quantity': 1,
              },
            ],
            mode='subscription',
            success_url='http://127.0.0.1:80/employees/subscription/success',
            cancel_url='http://127.0.0.1:80/account',
            metadata={
              'fk_user_id': current_user.id
            }
          )
        # ------------------------ localhost testing end ------------------------
        # ------------------------ production start ------------------------
        else:
          checkout_session = stripe.checkout.Session.create(
            line_items=[
              {
              'price': fk_stripe_price_id,
              'quantity': 1,
              },
            ],
            mode='subscription',
            success_url='https://triviafy.com/employees/subscription/success',
            cancel_url='https://triviafy.com/account',
            metadata={
              'fk_user_id': current_user.id
            }
          )
        # ------------------------ production end ------------------------
        # ------------------------ create db row start ------------------------
        # This is so I can easily get the customer id and subscription id in a future lookup
        checkout_session_id = checkout_session.id
        current_user_id = current_user.id
        new_checkout_session_obj = StripeCheckoutSessionObj(
          id = create_uuid_function('echeck_'),
          created_timestamp = create_timestamp_function(),
          fk_checkout_session_id = checkout_session_id,
          fk_user_id = current_user_id,
          status = 'draft'
        )
        db.session.add(new_checkout_session_obj)
        db.session.commit()
        # ------------------------ create db row end ------------------------
      except Exception as e:
        return str(e)
      # ------------------------ this line of code is needed to actually redirec to stripe checkout page start ------------------------
      return redirect(checkout_session.url, code=303)
      # ------------------------ this line of code is needed to actually redirec to stripe checkout page end ------------------------
    # ------------------------ post uiSubscriptionSelected end ------------------------
  # ------------------------ post end ------------------------
  return render_template('employees/interior/account/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/feature', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feature/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feature/<url_feature_request_code>', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feature/<url_feature_request_code>/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feature/<url_feature_request_code>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_feature_function(url_redirect_code=None, url_feature_request_code=None):
  localhost_print_function(' ------------------------ employees_feature_function START ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['group_stripe_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ non subscribed users should not see this page start ------------------------
  if page_dict['group_stripe_status'] != 'active' or url_feature_request_code == None:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e13'))
  # ------------------------ non subscribed users should not see this page end ------------------------
  # ------------------------ set feature request start ------------------------
  page_dict['url_feature_request_code'] = url_feature_request_code
  # ------------------------ set feature request end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    acceptable_arr = ['access_custom_questions', 'access_employee_surveys', 'access_ice_breakers', 'access_personality_tests', 'access_pre_employment_testing']
    ui_feature_request = request.form.get('ui_feature_request')
    if ui_feature_request not in acceptable_arr:
      return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s1'))
    if ui_feature_request in acceptable_arr:
      db_feature_requested_obj = UserFeatureRequestObj.query.filter_by(fk_user_id=current_user.id, feature_requested=ui_feature_request).first()
      if db_feature_requested_obj == None or db_feature_requested_obj == []:
        # ------------------------ insert email to db start ------------------------
        try:
          db_groups_obj = GroupObj.query.filter_by(fk_company_name=current_user.company_name).first()
          new_row = UserFeatureRequestObj(
            id = create_uuid_function('feature_'),
            created_timestamp = create_timestamp_function(),
            fk_user_id = current_user.id,
            fk_group_id = db_groups_obj.public_group_id,
            feature_requested = ui_feature_request
          )
          db.session.add(new_row)
          db.session.commit()
          return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s1'))
        except:
          pass
        # ------------------------ insert email to db end ------------------------
      else:
        return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='i3'))
  # ------------------------ post end ------------------------
  localhost_print_function(' ------------------------ employees_feature_function END ------------------------ ')
  return render_template('employees/interior/feature/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/activity/create/question', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/create/question/', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/create/question/<url_activity_type>', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/create/question/<url_activity_type>/', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/create/question/<url_activity_type>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_questions_function(url_redirect_code=None, url_activity_type=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ variables start ------------------------
  page_dict['url_activity_type'] = url_activity_type
  # ------------------------ variables end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['group_stripe_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ redirect if not subscribed start ------------------------
  if page_dict['group_stripe_status'] != 'active':
    return redirect(url_for('employees_views_interior.account_function', url_redirect_code='e14'))
  # ------------------------ redirect if not subscribed end ------------------------
  # ------------------------ delete all in progress questions start ------------------------
  db_drafted_questions_obj = None
  if page_dict['url_activity_type'] == 'activity_type_a':
    db_drafted_questions_obj = ActivityACreatedQuestionsObj.query.filter_by(fk_group_id=current_user.group_id,submission='draft').first()
  if db_drafted_questions_obj != None and db_drafted_questions_obj != []:
    if page_dict['url_activity_type'] == 'activity_type_a':
      ActivityACreatedQuestionsObj.query.filter_by(fk_group_id=current_user.group_id,submission='draft').delete()
    db.session.commit()
    return redirect(url_for('employees_views_interior.employees_questions_function'))
  # ------------------------ delete all in progress questions end ------------------------
  # ------------------------ pull all created questions by group start ------------------------
  db_activity_created_questions_obj = None
  if page_dict['url_activity_type'] == 'activity_type_a':
    db_activity_created_questions_obj = ActivityACreatedQuestionsObj.query.filter_by(fk_group_id=current_user.group_id).all()
  if page_dict['url_activity_type'] == 'activity_type_b':
    db_activity_created_questions_obj = ActivityBCreatedQuestionsObj.query.filter_by(fk_group_id=current_user.group_id).all()
  group_created_questions_arr_of_dicts = []
  for i_obj in db_activity_created_questions_obj:
    i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
    # ------------------------ append creator email start ------------------------
    db_user_obj = UserObj.query.filter_by(id=i_dict['fk_user_id']).first()
    i_dict['created_by_email'] = db_user_obj.email
    # ------------------------ append creator email end ------------------------
    # ------------------------ append asked status start ------------------------
    i_dict['question_used_status'] = 'Include in future quiz'
    db_used_obj = None
    if page_dict['url_activity_type'] == 'activity_type_a':
      db_used_obj = ActivityAGroupQuestionsUsedObj.query.filter_by(fk_question_id=i_dict['id'], fk_group_id=current_user.group_id).first()
    if page_dict['url_activity_type'] == 'activity_type_b':
      db_used_obj = ActivityBGroupQuestionsUsedObj.query.filter_by(fk_question_id=i_dict['id'], fk_group_id=current_user.group_id).first()
    if db_used_obj != None and db_used_obj != []:
      i_dict['question_used_status'] = 'Included in past quiz'
    # ------------------------ append asked status end ------------------------
    # ------------------------ shorten question start ------------------------
    if page_dict['url_activity_type'] == 'activity_type_b':
      i_dict['question'] = i_dict['question'][:30]+'...'
    # ------------------------ shorten question end ------------------------
    group_created_questions_arr_of_dicts.append(i_dict)
  page_dict['group_created_questions_arr_of_dicts'] = group_created_questions_arr_of_dicts
  page_dict['total_group_created_questions_arr_of_dicts'] = len(group_created_questions_arr_of_dicts)
  # ------------------------ pull all created questions by group end ------------------------
  # ------------------------ for setting cookie end ------------------------
  localhost_print_function(' ------------- 100-create question dashboard start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-create question dashboard end ------------- ')
  return render_template('employees/interior/create_question/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/activity/create/question/<url_activity_type>/draft', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/create/question/<url_activity_type>/draft/', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/create/question/<url_activity_type>/draft/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_question_draft_function(url_redirect_code=None, url_activity_type=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ variables start ------------------------
  if url_activity_type == None:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  page_dict['url_activity_type'] = url_activity_type
  # ------------------------ variables end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['group_stripe_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ redirect if not subscribed start ------------------------
  if page_dict['group_stripe_status'] != 'active':
    return redirect(url_for('employees_views_interior.account_function', url_redirect_code='e14'))
  # ------------------------ redirect if not subscribed end ------------------------
  # ------------------------ get products start ------------------------
  page_dict['products_list'] = get_activity_b_products_function()
  # ------------------------ get products end ------------------------
  page_dict['is_submission'] = True
  page_dict['is_view'] = False
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    # ------------------------ get user inputs start ------------------------
    ui_custom_question = request.form.get('ui_custom_question')
    ui_products_selected = request.form.getlist('ui_products_selected')   # list of str
    # ------------------------ get user inputs end ------------------------
    # ------------------------ sanatize inputs start ------------------------
    if len(ui_custom_question) <= 1 or len(ui_custom_question) > 150:
      return redirect(url_for('employees_views_interior.employees_question_draft_function', url_redirect_code='e19'))
    special_characters_arr = get_special_characters_function()
    for i in ui_custom_question:
      if i in special_characters_arr:
        return redirect(url_for('employees_views_interior.employees_question_draft_function', url_redirect_code='e18'))
    # ------------------------ sanatize inputs end ------------------------
    # ------------------------ error catch check start ------------------------
    if ui_products_selected == None or ui_products_selected == []:
      return redirect(url_for('employees_views_interior.employees_question_draft_function', url_redirect_code='e15'))
    for i_product in ui_products_selected:
      if i_product not in page_dict['products_list']:
        return redirect(url_for('employees_views_interior.employees_question_draft_function', url_redirect_code='e15'))
    final_products_str = ''
    if len(ui_products_selected) == 1:
      final_products_str = ui_products_selected[0]
    if len(ui_products_selected) > 1:
      final_products_str = ','.join(ui_products_selected)
    # ------------------------ error catch check end ------------------------
    # ------------------------ insert to db start ------------------------
    new_row = ActivityBCreatedQuestionsObj(
      id = create_uuid_function('custq_'),
      created_timestamp = create_timestamp_function(),
      fk_user_id = current_user.id,
      fk_group_id = current_user.group_id,
      question = ui_custom_question,
      product = final_products_str,
      status = False
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ insert to db end ------------------------
    return redirect(url_for('employees_views_interior.employees_questions_function', url_activity_type=page_dict['url_activity_type']))
  # ------------------------ submission end ------------------------
  localhost_print_function(' ------------- 100-create question creation start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-create question creation end ------------- ')
  return render_template('employees/interior/create_question/activity_b/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/activity/create/question/<url_activity_type>/view/<url_question_id>', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/create/question/<url_activity_type>/view/<url_question_id>/', methods=['GET', 'POST'])
@employees_views_interior.route('/activity/create/question/<url_activity_type>/view/<url_question_id>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_question_view_function(url_redirect_code=None, url_activity_type=None, url_question_id=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ variables start ------------------------
  if url_activity_type == None or url_question_id ==None:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  page_dict['url_activity_type'] = url_activity_type
  page_dict['url_question_id'] = url_question_id
  # ------------------------ variables end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['group_stripe_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ redirect if not subscribed start ------------------------
  if page_dict['group_stripe_status'] != 'active':
    return redirect(url_for('employees_views_interior.account_function', url_redirect_code='e14'))
  # ------------------------ redirect if not subscribed end ------------------------
  # ------------------------ get question obj start ------------------------
  page_dict['is_submission'] = False
  page_dict['is_view'] = True
  if page_dict['url_activity_type'] == 'activity_type_b':
    db_question_obj = ActivityBCreatedQuestionsObj.query.filter_by(id=page_dict['url_question_id']).first()
    if db_question_obj == None or db_question_obj == []:
      return redirect(url_for('employees_views_interior.employees_question_view_function', url_redirect_code='e16'))
    page_dict['question_info_dict'] = arr_of_dict_all_columns_single_item_function(db_question_obj)
  # ------------------------ get question obj end ------------------------
  localhost_print_function(' ------------- 100-create question view start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-create question view end ------------- ')
  return render_template('employees/interior/create_question/activity_b/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/custom/question', methods=['GET', 'POST'])
@employees_views_interior.route('/custom/question/', methods=['GET', 'POST'])
@employees_views_interior.route('/custom/question/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_create_question_v3_function(url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['group_stripe_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ redirect if not subscribed start ------------------------
  if page_dict['group_stripe_status'] != 'active':
    return redirect(url_for('employees_views_interior.account_function', url_redirect_code='e14'))
  # ------------------------ redirect if not subscribed end ------------------------
  page_dict['user_company_name'] = current_user.company_name
  # ------------------------ get products start ------------------------
  page_dict['products_list'] = get_activity_a_products_function()
  # ------------------------ get products end ------------------------
  # ------------------------ post start ------------------------
  if request.method == 'POST':
    # ------------------------ get user inputs start ------------------------
    ui_title = request.form.get('ui_create_question_title')             # str
    ui_categories = request.form.get('ui_create_question_categories')   # str
    ui_question = request.form.get('ui_create_question_question')       # str
    ui_option_a = request.form.get('ui_create_question_option_a')       # str
    ui_option_b = request.form.get('ui_create_question_option_b')       # str
    ui_option_c = request.form.get('ui_create_question_option_c')       # str
    ui_option_d = request.form.get('ui_create_question_option_d')       # str
    ui_option_e = request.form.get('ui_create_question_option_e')       # str
    ui_answer = request.form.get('ui_create_question_answer')           # str
    ui_answer_fitb = request.form.get('ui_create_question_answer_fitb')      # str
    ui_products_selected = request.form.getlist('ui_products_selected')   # list of str
    # ------------------------ get user inputs end ------------------------
    # ------------------------ sanitize user inputs start ------------------------
    if ui_option_e == None or ui_option_e.strip() == '':
      ui_option_e = None
    ui_title_checked = sanitize_create_question_categories_function(ui_title)
    ui_categories_checked = sanitize_create_question_categories_function(ui_categories)
    ui_question_checked = sanitize_create_question_question_function(ui_question)
    ui_option_a_checked = sanitize_create_question_options_function(ui_option_a)
    ui_option_b_checked = sanitize_create_question_options_function(ui_option_b)
    ui_option_c_checked = sanitize_create_question_options_function(ui_option_c)
    ui_option_d_checked = sanitize_create_question_options_function(ui_option_d)
    ui_option_e_checked = sanitize_create_question_option_e_function(ui_option_e)
    ui_answer_checked = sanitize_create_question_answer_function(ui_answer)
    ui_answer_fitb_checked = sanitize_create_question_options_function(ui_answer_fitb)
    # ------------------------ sanitize user inputs end ------------------------
    # ------------------------ error catch check start ------------------------
    if ui_option_e == None and ui_answer_checked.lower() == 'e':
      page_error_statement = 'Invalid answer choice'
      return redirect(url_for('employees_views_interior.employees_create_question_v3_function', url_redirect_code='e15'))
    if ui_title_checked == False or ui_categories_checked == False or ui_question_checked == False or ui_option_a_checked == False or ui_option_b_checked == False or ui_option_c_checked == False or ui_option_d_checked == False or ui_option_e_checked == False or ui_answer_checked == False or ui_answer_fitb_checked == False :
      return redirect(url_for('employees_views_interior.employees_create_question_v3_function', url_redirect_code='e15'))
    # ------------------------ error catch check end ------------------------
    # ------------------------ error catch check start ------------------------
    if ui_products_selected == None or ui_products_selected == []:
      return redirect(url_for('employees_views_interior.employees_create_question_v3_function', url_redirect_code='e15'))
    for i_product in ui_products_selected:
      if i_product not in page_dict['products_list']:
        return redirect(url_for('employees_views_interior.employees_create_question_v3_function', url_redirect_code='e15'))
    final_products_str = ''
    if len(ui_products_selected) == 1:
      final_products_str = ui_products_selected[0]
    if len(ui_products_selected) > 1:
      final_products_str = ','.join(ui_products_selected)
    # ------------------------ error catch check end ------------------------
    # ------------------------ define variable for insert start ------------------------
    final_id = create_uuid_function('questionid_')
    # ------------------------ define variable for insert end ------------------------
    # ------------------------ ui uploaded image start ------------------------
    create_question_uploaded_image_aws_url = ''
    create_question_uploaded_image_uuid = ''
    try:
      if request.files:
        if "filesize" in request.cookies:
          # ------------------------ ui file start ------------------------
          image = request.files["ui_image_upload"]
          # ------------------------ ui file end ------------------------
          # ------------------------ if no image attached start ------------------------
          if image.filename == '' or image.filename == ' ' or image.filename == None:
            pass
          # ------------------------ if no image attached end ------------------------
          # ------------------------ if image attached start ------------------------
          else:
            # Keep track of the original filename that someone is uploading
            create_question_upload_image_original_filename = image.filename
            # Create image uuid to store in aws
            create_question_uploaded_image_uuid = '_user_uploaded_image_' + final_id
            # Change the name of the image from whatever the user uploaded to the question uuid as name
            image = candidates_change_uploaded_image_filename_function(image, create_question_uploaded_image_uuid)
            # Get image filesize
            file_size = request.cookies["filesize"]
            # Check and upload the user file image
            user_image_upload_status = candidates_user_upload_image_checks_aws_s3_function(image, file_size)
            if user_image_upload_status != False:
              # Finalize image variables
              create_question_uploaded_image_aws_url = 'https://' + os.environ.get('AWS_TRIVIAFY_BUCKET_NAME') + '.s3.' + os.environ.get('AWS_TRIVIAFY_REGION') + '.amazonaws.com/' + image.filename
          # ------------------------ if image attached end ------------------------
    except:
      localhost_print_function('did not upload img')
      pass
    # ------------------------ ui uploaded image end ------------------------
    # ------------------------ add to db start ------------------------
    try:
      db_groups_obj = GroupObj.query.filter_by(fk_company_name=current_user.company_name).first()
      # ------------------------ append answers start ------------------------
      concat_ui_answer = ui_answer.upper() + ', ' + ui_answer_fitb.lower()
      # ------------------------ append answers end ------------------------
      new_row = ActivityACreatedQuestionsObj(
        id = final_id,
        created_timestamp=create_timestamp_function(),
        fk_user_id = current_user.id,
        status = False,
        categories = ui_categories,
        title = ui_title,
        question = ui_question,
        option_a = ui_option_a,
        option_b = ui_option_b,
        option_c = ui_option_c,
        option_d = ui_option_d,
        option_e = ui_option_e,
        answer = concat_ui_answer,
        aws_image_uuid = create_question_uploaded_image_uuid,
        aws_image_url = create_question_uploaded_image_aws_url,
        submission = 'draft',
        product = final_products_str,
        fk_group_id = db_groups_obj.public_group_id
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      localhost_print_function('did not create question in db')
      pass
    # ------------------------ add to db end ------------------------
    # ------------------------ redirect start ------------------------
    return redirect(url_for('employees_views_interior.employees_preview_question_function', url_question_id=final_id))
    # ------------------------ redirect end ------------------------
  # ------------------------ post end ------------------------
  return render_template('employees/interior/create_question/v3/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/questions/preview', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/questions/preview/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/questions/preview/<url_question_id>', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/questions/preview/<url_question_id>/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/questions/preview/<url_question_id>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_preview_question_function(url_redirect_code=None, url_question_id=None):
  localhost_print_function(' ------------------------ employees_preview_question_function START ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['group_stripe_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ redirect if not subscribed start ------------------------
  if page_dict['group_stripe_status'] != 'active':
    return redirect(url_for('employees_views_interior.account_function', url_redirect_code='e14'))
  # ------------------------ redirect if not subscribed end ------------------------
  # ------------------------ redirect if question id none start ------------------------
  if url_question_id == None:
    return redirect(url_for('employees_views_interior.employees_questions_function', url_redirect_code='e16'))
  # ------------------------ redirect if question id none end ------------------------
  page_dict['user_company_name'] = current_user.company_name
  page_dict['user_company_name'] = page_dict['user_company_name'].lower().capitalize()
  # ------------------------ get latest custom question start ------------------------
  db_question_obj = ActivityACreatedQuestionsObj.query.filter_by(id=url_question_id).first()
  if db_question_obj == None or db_question_obj == []:
    return redirect(url_for('employees_views_interior.employees_questions_function', url_redirect_code='e16'))
  # ------------------------ get latest custom question end ------------------------
  page_dict['current_question_is_draft'] = False
  if db_question_obj.submission == 'draft':
    page_dict['current_question_is_draft'] = True
  # ------------------------ build latest dict start ------------------------
  page_dict['question_info_dict'] = arr_of_dict_all_columns_single_item_function(db_question_obj)
  page_dict['question_info_dict']['categories'] = categories_tuple_function(page_dict['question_info_dict']['categories'])
  # ------------------------ build latest dict end ------------------------
  if request.method == 'POST':
    if db_question_obj.submission == 'draft':
      db_question_obj.submission = 'submitted'
      db.session.commit()
      # ------------------------ email self start ------------------------
      if current_user.email != os.environ.get('PERSONAL_EMAIL') and current_user.email != os.environ.get('RUN_TEST_EMAIL'):
        try:
          output_to_email = os.environ.get('TRIVIAFY_NOTIFICATIONS_EMAIL')
          output_subject = f'Employees: Custom Question by {current_user.email}'
          output_body = f"Hi there,\n\nNew custom question created by {current_user.email} \n\nBest,\nTriviafy"
          send_email_template_function(output_to_email, output_subject, output_body)
        except:
          pass
      # ------------------------ email self end ------------------------
    return redirect(url_for('employees_views_interior.employees_questions_function', url_activity_type='activity_type_a'))
  localhost_print_function(' ------------------------ employees_preview_question_function END ------------------------ ')
  return render_template('employees/interior/create_question/preview/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/feedback/primary', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/primary/', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/primary/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_feedback_primary_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_feedback_primary_function START ------------------------ ')
  # ------------------------ check if already answered start ------------------------
  feedback_primary_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='primary_product_choice').first()
  if feedback_primary_obj != None and feedback_primary_obj != []:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ check if already answered end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ get current activities start ------------------------
  activities_list, activities_list_index = get_team_building_activities_list_function()
  page_dict['activities_list'] = activities_list
  page_dict['activities_list_index'] = activities_list_index
  # ------------------------ get current activities end ------------------------
  page_dict['feedback_step'] = '1'
  page_dict['feedback_request'] = 'primary'
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    ui_answer = request.form.get('ui_selection_radio')
    # ------------------------ invalid start ------------------------
    if ui_answer not in activities_list:
      return redirect(url_for('employees_views_interior.employees_feedback_primary_function'))
    # ------------------------ invalid end ------------------------
    # ------------------------ insert to db start ------------------------
    new_row = UserSignupFeedbackObj(
      id = create_uuid_function('feedback_'),
      created_timestamp = create_timestamp_function(),
      fk_user_id = current_user.id,
      fk_email = current_user.email,
      question = 'primary_product_choice',
      response = ui_answer,
      fk_group_id = current_user.group_id
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ insert to db end ------------------------
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ submission end ------------------------
  localhost_print_function(' ------------------------ employees_feedback_primary_function END ------------------------ ')
  return render_template('employees/interior/feedback/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/feedback/secondary', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/secondary/', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/secondary/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_feedback_secondary_function(url_redirect_code=None, value_to_remove=None):
  localhost_print_function(' ------------------------ employees_feedback_secondary_function START ------------------------ ')
  # ------------------------ check if already answered start ------------------------
  feedback_secondary_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='secondary_product_choice').first()
  if feedback_secondary_obj != None and feedback_secondary_obj != []:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ check if already answered end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ get current activities start ------------------------
  activities_list, activities_list_index = get_team_building_activities_list_function()
  # ------------------------ remove primary from selection start ------------------------
  feedback_primary_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='primary_product_choice').first()
  activities_list.remove(feedback_primary_obj.response)
  activities_list_index.pop()
  # ------------------------ remove primary from selection end ------------------------
  page_dict['activities_list'] = activities_list
  page_dict['activities_list_index'] = activities_list_index
  # ------------------------ get current activities end ------------------------
  page_dict['feedback_step'] = '2'
  page_dict['feedback_request'] = 'secondary'
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    ui_answer = request.form.get('ui_selection_radio')
    # ------------------------ invalid start ------------------------
    if ui_answer not in activities_list:
      return redirect(url_for('employees_views_interior.employees_feedback_secondary_function'))
    # ------------------------ invalid end ------------------------
    # ------------------------ insert to db start ------------------------
    new_row = UserSignupFeedbackObj(
      id = create_uuid_function('feedback_'),
      created_timestamp = create_timestamp_function(),
      fk_user_id = current_user.id,
      fk_email = current_user.email,
      question = 'secondary_product_choice',
      response = ui_answer,
      fk_group_id = current_user.group_id
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ insert to db end ------------------------
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ submission end ------------------------
  localhost_print_function(' ------------------------ employees_feedback_secondary_function END ------------------------ ')
  return render_template('employees/interior/feedback/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/feedback/<url_feedback_code>', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/<url_feedback_code>/', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/<url_feedback_code>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_feedback_year_month_function(url_redirect_code=None, url_feedback_code=None):
  # ------------------------ check if already answered start ------------------------
  feedback_obj = None
  try:
    feedback_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question=url_feedback_code).first()
    if feedback_obj != None and feedback_obj != []:
      return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  except:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ check if already answered end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ variables start ------------------------
  page_dict['url_feedback_code'] = url_feedback_code
  # ------------------------ variables end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['feedback_step'] = None
  page_dict['feedback_request'] = None
  if url_feedback_code == 'birthday':
    page_dict['feedback_step'] = '3'
    page_dict['feedback_request'] = 'birthday'
  if url_feedback_code == 'job_start_date':
    page_dict['feedback_step'] = '4'
    page_dict['feedback_request'] = 'job_start_date'
  # ------------------------ set variables end ------------------------
  # ------------------------ get questions start ------------------------
  favorite_questions_arr, favorite_questions_arr_index = get_favorite_questions_function()
  page_dict['favorite_questions_arr'] = favorite_questions_arr
  page_dict['favorite_questions_arr_index'] = favorite_questions_arr_index
  # ------------------------ get questions end ------------------------
  # ------------------------ get month days dict start ------------------------
  months_arr, days_arr, years_arr, month_day_dict = get_month_days_years_function()
  page_dict['months_arr'] = months_arr
  page_dict['days_arr'] = days_arr
  page_dict['years_arr'] = years_arr
  # ------------------------ get month days dict end ------------------------
  # ------------------------ get current response if exists start ------------------------
  page_dict['existing_complete'] = False
  page_dict['existing_feedback_skipped'] = False
  page_dict['existing_question'] = None
  page_dict['existing_answer'] = None
  page_dict['existing_celebrate_month'] = None
  page_dict['existing_celebrate_day'] = None
  page_dict['existing_celebrate_year'] = None
  try:
    # ------------------------ check if feedback step skipped start ------------------------
    db_feedback_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question=url_feedback_code+'_choice').first()
    if db_feedback_obj != None and db_feedback_obj != []:
      if db_feedback_obj.response == 'feedback skipped':
        page_dict['existing_complete'] = True
        page_dict['existing_feedback_skipped'] = True
    # ------------------------ check if feedback step skipped end ------------------------
    db_celebrate_obj = UserCelebrateObj.query.filter_by(fk_user_id=current_user.id,event=url_feedback_code).first()
    if db_celebrate_obj != None and db_celebrate_obj != []:
      db_celebrate_dict = arr_of_dict_all_columns_single_item_function(db_celebrate_obj)
      page_dict['existing_complete'] = True
      page_dict['existing_question'] = db_celebrate_dict['question']
      page_dict['existing_answer'] = db_celebrate_dict['answer']
      page_dict['existing_celebrate_month'] = db_celebrate_dict['celebrate_month']
      page_dict['existing_celebrate_day'] = db_celebrate_dict['celebrate_day']
      page_dict['existing_celebrate_year'] = db_celebrate_dict['celebrate_year']
  except:
    pass
  # ------------------------ get current response if exists end ------------------------
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    # ------------------------ get user inputs start ------------------------
    ui_year_month_question = request.form.get('ui_year_month_question')
    ui_year_month_answer = request.form.get('ui_year_month_answer')
    ui_month_only = request.form.get('ui_month_only')
    ui_day_only = request.form.get('ui_day_only')
    ui_year_only = request.form.get('ui_year_only')
    # ------------------------ get user inputs end ------------------------
    # ------------------------ sanatize inputs start ------------------------
    # question
    if ui_year_month_question not in favorite_questions_arr:
      return redirect(url_for('employees_views_interior.employees_feedback_year_month_function', url_redirect_code='e17', url_feedback_code=url_feedback_code))
    # answer
    if len(ui_year_month_answer) == 0 or len(ui_year_month_answer) > 100:
      return redirect(url_for('employees_views_interior.employees_feedback_year_month_function', url_redirect_code='e19', url_feedback_code=url_feedback_code))
    special_characters_arr = get_special_characters_function()
    for i in ui_year_month_answer:
      if i in special_characters_arr:
        return redirect(url_for('employees_views_interior.employees_feedback_year_month_function', url_redirect_code='e18', url_feedback_code=url_feedback_code))
    try:
      # birth month
      if int(ui_month_only) not in months_arr:
        return redirect(url_for('employees_views_interior.employees_feedback_year_month_function', url_redirect_code='e20', url_feedback_code=url_feedback_code))
    except:
      pass
    try:
      # birth day
      allowed_days_arr = month_day_dict[str(ui_month_only)]
      if int(ui_day_only) not in allowed_days_arr:
        return redirect(url_for('employees_views_interior.employees_feedback_year_month_function', url_redirect_code='e21', url_feedback_code=url_feedback_code))
    except:
      pass
    try:
      # birth year
      if int(ui_year_only) not in years_arr:
        return redirect(url_for('employees_views_interior.employees_feedback_year_month_function', url_redirect_code='e26', url_feedback_code=url_feedback_code))
    except:
      pass
    # ------------------------ sanatize inputs end ------------------------
    # ------------------------ question double start ------------------------
    try:
      db_celebrate_obj = UserCelebrateObj.query.filter_by(fk_user_id=current_user.id,question=ui_year_month_question).first()
      if db_celebrate_obj != None:
        if db_celebrate_obj.question == ui_year_month_question:
          return redirect(url_for('employees_views_interior.employees_feedback_year_month_function', url_redirect_code='e27', url_feedback_code=url_feedback_code))
    except:
      pass
    # ------------------------ question double end ------------------------
    try:
      # ------------------------ pre set start start ------------------------
      new_month = None
      new_day = None
      new_year = None
      try:
        new_month = int(ui_month_only)
      except:
        pass
      try:
        new_day = int(ui_day_only)
      except:
        pass
      try:
        new_year = int(ui_year_only)
      except:
        pass
      if new_day == None:
        new_day = int(1)
      # ------------------------ pre set start end ------------------------
      new_birthday_row_id = create_uuid_function('celebrate_')
      # ------------------------ insert to db celebration start ------------------------
      new_row = UserCelebrateObj(
        id = new_birthday_row_id,
        created_timestamp = create_timestamp_function(),
        fk_user_id = current_user.id,
        question = ui_year_month_question,
        answer = ui_year_month_answer.lower().capitalize(),
        event = url_feedback_code,
        celebrate_month = new_month,
        celebrate_day = new_day,
        celebrate_year = new_year,
        status = False,
        fk_group_id = current_user.group_id
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ insert to db celebration end ------------------------
      # ------------------------ insert to db feedback start ------------------------
      try:
        new_row = UserSignupFeedbackObj(
          id = create_uuid_function('feedback_'),
          created_timestamp = create_timestamp_function(),
          fk_user_id = current_user.id,
          fk_email = current_user.email,
          question = url_feedback_code + '_choice',
          response = new_birthday_row_id,
          fk_group_id = current_user.group_id
        )
        db.session.add(new_row)
        db.session.commit()
      except:
        pass
      # ------------------------ insert to db feedback end ------------------------
    except:
      pass
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ submission end ------------------------
  localhost_print_function(' ------------- 100-feedback input dates start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-feedback input dates end ------------- ')
  return render_template('employees/interior/feedback/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/feedback/<url_feedback_code>/skip', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/<url_feedback_code>/skip/', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/<url_feedback_code>/skip/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_feedback_year_month_skip_function(url_redirect_code=None, url_feedback_code=None):
  # ------------------------ check if already answered start ------------------------
  feedback_obj = None
  try:
    feedback_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question=url_feedback_code+'_choice').first()
    if feedback_obj != None and feedback_obj != []:
      return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  except:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ check if already answered end ------------------------
  # ------------------------ skip logic start ------------------------
  try:
    # ------------------------ insert to db start ------------------------
    new_row = UserSignupFeedbackObj(
      id = create_uuid_function('feedback_'),
      created_timestamp = create_timestamp_function(),
      fk_user_id = current_user.id,
      fk_email = current_user.email,
      question = url_feedback_code + '_choice',
      response = 'feedback skipped',
      fk_group_id = current_user.group_id
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ insert to db end ------------------------
  except:
    pass
  # ------------------------ skip logic end ------------------------
  return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/feedback/<url_feedback_code>/replace', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/<url_feedback_code>/replace/', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/<url_feedback_code>/replace/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_feedback_year_month_replace_function(url_redirect_code=None, url_feedback_code=None):
  # ------------------------ delete from db start ------------------------
  question_id = None
  test_id = None
  try:
    UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question=url_feedback_code+'_choice').delete()
  except:
    pass
  try:
    db_obj = UserCelebrateObj.query.filter_by(fk_user_id=current_user.id,event=url_feedback_code).first()
    question_id = db_obj.fk_question_id
    test_id = db_obj.fk_test_id
    UserCelebrateObj.query.filter_by(fk_user_id=current_user.id,event=url_feedback_code).delete()
  except:
    pass
  try:
    ActivityACreatedQuestionsObj.query.filter_by(fk_user_id=current_user.id,id=question_id,product=url_feedback_code).delete()
  except:
    pass
  try:
    ActivityAGroupQuestionsUsedObj.query.filter_by(fk_question_id=question_id,fk_test_id=test_id,product=url_feedback_code).delete()
  except:
    pass
  try:
    ActivityATestGradedObj.query.filter_by(fk_test_id=test_id,product=url_feedback_code).delete()
  except:
    pass
  try:
    ActivityATestObj.query.filter_by(id=test_id,product=url_feedback_code).delete()
  except:
    pass
  try:
    db.session.commit()
  except:
    pass
  # ------------------------ delete from db end ------------------------
  return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/feedback/celebrations/delete_skipped', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/celebrations/delete_skipped/', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/celebrations/delete_skipped/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_feedback_delete_skipped_function(url_redirect_code=None):
  UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,response='feedback skipped').delete()
  db.session.commit()
  return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/feedback/marketing', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/marketing/', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/marketing/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_feedback_marketing_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_feedback_marketing_function START ------------------------ ')
  # ------------------------ check if already answered start ------------------------
  feedback_marketing_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='marketing_choice').first()
  if feedback_marketing_obj != None and feedback_marketing_obj != []:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ check if already answered end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ get current activities start ------------------------
  marketing_list, marketing_list_index = get_marketing_list_function()
  page_dict['marketing_list'] = marketing_list
  page_dict['marketing_list_index'] = marketing_list_index
  # ------------------------ get current activities end ------------------------
  page_dict['feedback_step'] = '5'
  page_dict['feedback_request'] = 'marketing'
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    ui_answer = request.form.get('ui_selection_radio')
    # ------------------------ invalid start ------------------------
    if ui_answer not in marketing_list:
      return redirect(url_for('employees_views_interior.employees_feedback_marketing_function'))
    # ------------------------ invalid end ------------------------
    # ------------------------ insert to db start ------------------------
    new_row = UserSignupFeedbackObj(
      id = create_uuid_function('feedback_'),
      created_timestamp = create_timestamp_function(),
      fk_user_id = current_user.id,
      fk_email = current_user.email,
      question = 'marketing_choice',
      response = ui_answer,
      fk_group_id = current_user.group_id
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ insert to db end ------------------------
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ submission end ------------------------
  localhost_print_function(' ------------------------ employees_feedback_marketing_function END ------------------------ ')
  return render_template('employees/interior/feedback/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/feedback/name', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/name/', methods=['GET', 'POST'])
@employees_views_interior.route('/feedback/name/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_feedback_name_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_feedback_name_function START ------------------------ ')
  # ------------------------ check if already answered start ------------------------
  if current_user.name != None and current_user.name != '':
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ check if already answered end ------------------------
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'employees/interior/feedback/index.html'
  # ------------------------ for setting cookie end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  page_dict['feedback_step'] = '0'
  page_dict['feedback_request'] = 'name'
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    # ------------------------ get user inputs start ------------------------
    ui_name = request.form.get('ui_name')
    # ------------------------ get user inputs end ------------------------
    # ------------------------ sanatize inputs start ------------------------
    if len(ui_name) <= 1 or len(ui_name) > 20:
      return redirect(url_for('employees_views_interior.employees_feedback_name_function', url_redirect_code='e19'))
    special_characters_arr = get_special_characters_function()
    for i in ui_name:
      if i in special_characters_arr:
        return redirect(url_for('employees_views_interior.employees_feedback_name_function', url_redirect_code='e18'))
    # ------------------------ sanatize inputs end ------------------------
    # ------------------------ update db start ------------------------
    current_user.name = ui_name.lower().capitalize()
    db.session.commit()
    # ------------------------ update db end ------------------------
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ submission end ------------------------
  localhost_print_function(' ------------------------ employees_feedback_name_function END ------------------------ ')
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, page_dict_to_html=page_dict)
  else:
    browser_response = browser_response_set_cookie_function_v5(current_user, template_location_url, page_dict)
    localhost_print_function(' ------------------------ employees_feedback_name_function END ------------------------ ')
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------
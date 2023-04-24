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
from website.models import EmployeesGroupsObj, EmployeesGroupSettingsObj, EmployeesTestsObj, EmployeesDesiredCategoriesObj, CreatedQuestionsObj, EmployeesTestsGradedObj, UserObj, EmployeesCapacityOptionsObj, EmployeesEmailSentObj, StripeCheckoutSessionObj, EmployeesGroupQuestionsUsedObj, EmployeesFeatureRequestObj, EmployeesFeedbackObj, EmployeesBirthdayInfoObj
from website.backend.candidates.autogeneration import generate_random_length_uuid_function, question_choices_function
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function, categories_tuple_function
from website.backend.candidates.datetime_manipulation import days_times_timezone_arr_function, convert_timestamp_to_month_day_string_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.backend.candidates.string_manipulation import all_employee_question_categories_sorted_function
from website.backend.candidates.user_inputs import sanitize_char_count_1_function, sanitize_create_question_options_function, sanitize_create_question_categories_function, sanitize_create_question_question_function, sanitize_create_question_option_e_function, sanitize_create_question_answer_function, get_special_characters_function
from website.backend.candidates.send_emails import send_email_template_function
import os
from website.backend.candidates.quiz import create_quiz_function, grade_quiz_function, get_next_quiz_open_function
import json
from datetime import datetime
from website.backend.candidates.stripe import check_stripe_subscription_status_function_v2, convert_current_period_end_function
import stripe
from website.backend.candidates.datatype_conversion_manipulation import one_col_dict_to_arr_function
from website.backend.candidates.test_backend import get_test_winner
from website.backend.candidates.test_backend import first_user_first_quiz_check_function
from website.backend.candidates.aws_manipulation import candidates_change_uploaded_image_filename_function, candidates_user_upload_image_checks_aws_s3_function
from website.backend.candidates.string_manipulation import breakup_email_function
from website.backend.candidates.lists import get_team_building_activities_list_function, get_month_days_function, get_favorite_questions_function, get_marketing_list_function
from website.backend.candidates.dropdowns import get_dropdowns_trivia_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
employees_views_interior = Blueprint('employees_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

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
  db_email_obj = EmployeesEmailSentObj.query.filter_by(to_email=current_user.email,subject=output_subject).first()
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
      new_row_email = EmployeesEmailSentObj(
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
        new_row_email = EmployeesEmailSentObj(
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
@employees_views_interior.route('/dashboard')
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
  # ------------------------ check if email verified start ------------------------
  if current_user.verified_email == False:
    return redirect(url_for('employees_views_interior.verify_email_function', url_redirect_code='s8'))
  # ------------------------ check if email verified end ------------------------
  # ------------------------ check if feedback given start ------------------------
  # name
  if current_user.name == None or current_user.name == '':
    return redirect(url_for('employees_views_interior.employees_feedback_name_function'))
  # primary
  feedback_primary_obj = EmployeesFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='primary_product_choice').first()
  if feedback_primary_obj == None or feedback_primary_obj == []:
    return redirect(url_for('employees_views_interior.employees_feedback_primary_function'))
  # secondary
  feedback_secondary_obj = EmployeesFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='secondary_product_choice').first()
  if feedback_secondary_obj == None or feedback_secondary_obj == []:
    return redirect(url_for('employees_views_interior.employees_feedback_secondary_function'))
  # birthday
  feedback_birthday_obj = EmployeesFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='birthday_choice').first()
  if feedback_birthday_obj == None or feedback_birthday_obj == []:
    return redirect(url_for('employees_views_interior.employees_feedback_birthday_function'))
  # how did you hear about triviafy?
  feedback_marketing_obj = EmployeesFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='marketing_choice').first()
  if feedback_marketing_obj == None or feedback_marketing_obj == []:
    return redirect(url_for('employees_views_interior.employees_feedback_marketing_function'))
  # ------------------------ check if feedback given end ------------------------
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'employees/interior/dashboard/index.html'
  # ------------------------ for setting cookie end ------------------------
  # ------------------------ redirect codes start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  # ------------------------ redirect codes end ------------------------
  # ------------------------ page dict start ------------------------
  page_dict = {}
  # ------------------------ page dict end ------------------------
  # ------------------------ pull/create group id start ------------------------
  company_group_id = None
  db_groups_obj = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).first()
  if db_groups_obj == None or db_groups_obj == []:
    company_group_id = generate_random_length_uuid_function(6)
    # ------------------------ while loop if generated group id already exists start ------------------------
    group_id_exists_check = EmployeesGroupsObj.query.filter_by(public_group_id=company_group_id).first()
    while group_id_exists_check != None:
      company_group_id = generate_random_length_uuid_function(6)
      group_id_exists_check = EmployeesGroupsObj.query.filter_by(public_group_id=company_group_id).first()
    # ------------------------ while loop if generated group id already exists end ------------------------
    # ------------------------ insert to db start ------------------------
    try:
      new_row = EmployeesGroupsObj(
        id = create_uuid_function('group_'),
        created_timestamp = create_timestamp_function(),
        fk_company_name = current_user.company_name,
        fk_user_id = current_user.id,
        public_group_id = company_group_id,
        status = 'active',
        trivia = True,
        picture_quiz = False,
        birthday_questions = False,
        icebreakers = False,
        surveys = False,
        personality_test = False,
        this_or_that = False,
        most_likely_to = False,
        giftcard = False
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ insert to db end ------------------------
  else:
    company_group_id = db_groups_obj.public_group_id
  # ------------------------ pull/create group id end ------------------------
  # ------------------------ pull/create group settings start ------------------------
  db_group_settings_obj = EmployeesGroupSettingsObj.query.filter_by(fk_group_id=company_group_id).first()
  if db_group_settings_obj == None or db_group_settings_obj == []:
    # ------------------------ insert to db start ------------------------
    try:
      new_row = EmployeesGroupSettingsObj(
        id = create_uuid_function('gset_'),
        created_timestamp = create_timestamp_function(),
        fk_group_id = company_group_id,
        fk_user_id = current_user.id,
        timezone = 'EST',
        start_day = 'Monday',
        start_time = '12 PM',
        end_day = 'Thursday',
        end_time = '1 PM',
        cadence = 'Weekly',
        total_questions = 10,
        question_type = 'Mixed',
        categories = 'all_categories'
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ insert to db end ------------------------
  else:
    pass
  # ------------------------ pull/create group settings end ------------------------
  # ------------------------ ensure all historical tests are closed start ------------------------
  current_datetime_str = datetime.now().strftime("%m/%d/%Y %H:%M:%S")   # str
  current_datetime_datetime = datetime.strptime(current_datetime_str, "%m/%d/%Y %H:%M:%S")  # datetime
  db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=company_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).all()
  try:
    historical_tests_were_closed = False
    for i in db_tests_obj:
      i_test_dict = arr_of_dict_all_columns_single_item_function(i)
      if i_test_dict['status'] == 'Closed':
        continue
      else:
        i_test_end_timestamp_str = i_test_dict['end_timestamp'].strftime("%m/%d/%Y %H:%M:%S")  # str
        i_test_end_timestamp_datetime = datetime.strptime(i_test_end_timestamp_str, "%m/%d/%Y %H:%M:%S")  # datetime
        if current_datetime_datetime > i_test_end_timestamp_datetime:
          i.status = 'Closed'
          db.session.commit()
          historical_tests_were_closed = True
    if historical_tests_were_closed == True:
      db.session.commit()
      return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  except:
    pass
  # ------------------------ ensure all historical tests are closed end ------------------------
  # ------------------------ delete all historical closed tests with 'No participation' start ------------------------
  db_historical_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=company_group_id, status='Closed').order_by(EmployeesTestsObj.created_timestamp.desc()).all()
  try:
    if db_historical_tests_obj != None and db_historical_tests_obj != []:
      historical_tests_were_deleted = False
      for i_historical_test_obj in db_historical_tests_obj:
        i_historical_test_dict = arr_of_dict_all_columns_single_item_function(i_historical_test_obj)
        # ------------------------ winner start ------------------------
        page_dict['latest_test_winner'], page_dict['latest_test_winner_score'] = get_test_winner(i_historical_test_dict['id'])
        # ------------------------ winner end ------------------------
        # ------------------------ delete histoical no participation start ------------------------
        if page_dict['latest_test_winner'] == 'No participation':
          EmployeesGroupQuestionsUsedObj.query.filter_by(fk_test_id=i_historical_test_dict['id']).delete()
          EmployeesTestsGradedObj.query.filter_by(fk_test_id=i_historical_test_dict['id']).delete()
          EmployeesTestsObj.query.filter_by(id=i_historical_test_dict['id']).delete()
          historical_tests_were_deleted = True
          db.session.commit()
        # ------------------------ delete histoical no participation end ------------------------
      # ------------------------ redirect start ------------------------
      if historical_tests_were_deleted == True:
        db.session.commit()
        return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
      # ------------------------ redirect end ------------------------
  except:
    pass
  # ------------------------ delete all historical closed tests with 'No participation' end ------------------------
  # ------------------------ pull/create latest test start ------------------------
  db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=company_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
  first_test_exists = False
  if db_tests_obj == None or db_tests_obj == []:
    pass
  else:
    first_test_exists = True
    # ------------------------ create latest test start ------------------------
    create_quiz_status = create_quiz_function(db_group_settings_obj.fk_group_id)
    # ------------------------ create latest test end ------------------------
    # ------------------------ latest test info start ------------------------
    db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=company_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
    start_month_day_str = convert_timestamp_to_month_day_string_function(db_tests_obj.start_timestamp)
    end_month_day_str = convert_timestamp_to_month_day_string_function(db_tests_obj.end_timestamp)
    page_dict['full_time_string'] = start_month_day_str + ', ' + db_tests_obj.start_time + ' - ' + end_month_day_str + ', ' + db_tests_obj.end_time + ' ' + db_tests_obj.timezone
    page_dict['ending_time_string'] = end_month_day_str + ', ' + db_tests_obj.end_time + ' ' + db_tests_obj.timezone
    # ------------------------ latest test info end ------------------------
  page_dict['first_test_exists'] = first_test_exists
  # ------------------------ pull/create latest test end ------------------------
  # ------------------------ pull latest graded start ------------------------
  ui_latest_test_completed = False
  try:
    db_test_grading_obj = EmployeesTestsGradedObj.query.filter_by(fk_test_id=db_tests_obj.id, fk_user_id=current_user.id).first()
    # ------------------------ auto route to latest quiz start ------------------------
    # if (db_test_grading_obj == None or db_test_grading_obj == []) and db_tests_obj.status == 'Open':
    #   return redirect(url_for('employees_views_interior.employees_test_id_function'))
    # if db_test_grading_obj.status == 'wip' and db_tests_obj.status == 'Open':
    #   return redirect(url_for('employees_views_interior.employees_test_id_function'))
    # ------------------------ auto route to latest quiz end ------------------------
    if db_test_grading_obj.status == 'complete':
      ui_latest_test_completed = True
  except:
    pass
  page_dict['ui_latest_test_completed'] = ui_latest_test_completed
  # ------------------------ pull latest graded end ------------------------
  # ------------------------ if latest closed then pull winner start ------------------------
  page_dict['latest_test_is_closed'] = False
  page_dict['latest_test_winner'] = ''
  page_dict['latest_test_winner_score'] = float(0)
  db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=company_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
  try:
    db_tests_dict = arr_of_dict_all_columns_single_item_function(db_tests_obj)
    if db_tests_dict['status'] == 'Closed':
      page_dict['latest_test_is_closed'] = True
    # ------------------------ winner start ------------------------
    page_dict['latest_test_winner'], page_dict['latest_test_winner_score'] = get_test_winner(db_tests_dict['id'])
    # ------------------------ winner end ------------------------
    # ------------------------ if latest closed then pull next quiz open datetime start ------------------------
    page_dict['next_quiz_open_string'] = get_next_quiz_open_function(company_group_id)
    # ------------------------ if latest closed then pull next quiz open datetime end ------------------------
  except:
    pass
  # ------------------------ if latest closed then pull winner end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['stripe_subscription_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ total company users check start ------------------------
  db_users_obj = UserObj.query.filter_by(company_name=current_user.company_name).all()
  page_dict['current_total_company_users'] = len(db_users_obj)
  page_dict['desired_min_total_company_users'] = 4
  # ------------------------ total company users check end ------------------------
  # ------------------------ check if share with team email has been sent start ------------------------
  output_subject = f"Successfully Verified Email"
  db_email_obj = EmployeesEmailSentObj.query.filter_by(to_email=current_user.email,subject=output_subject).first()
  if db_email_obj == None or db_email_obj == []:
    # ------------------------ send email start ------------------------
    try:
      guessed_name = breakup_email_function(current_user.email)
      output_to_email = current_user.email
      output_body = f"<p>Hi {guessed_name},</p>\
                      <p>Thank you for creating an account with Triviafy!</p>\
                      <p>Your team members can access the same team building activities <a href='https://triviafy.com/employees/signup'>here</a>, simply forward this email to your team.</p>\
                      <p style='margin:0;'>Best,</p>\
                      <p style='margin:0;'>Triviafy Support Team</p>"
      send_email_template_function(output_to_email, output_subject, output_body)
      # ------------------------ insert email to db start ------------------------
      try:
        new_row = EmployeesEmailSentObj(
          id = create_uuid_function('email_'),
          created_timestamp = create_timestamp_function(),
          from_user_id_fk = current_user.id,
          to_email = output_to_email,
          subject = output_subject,
          body = output_body
        )
        db.session.add(new_row)
        db.session.commit()
      except:
        pass
      # ------------------------ insert email to db end ------------------------
    except:
      pass
    # ------------------------ send email end ------------------------
  # ------------------------ check if share with team email has been sent end ------------------------
  # ------------------------ assign to dict start ------------------------
  db_group_settings_obj = EmployeesGroupSettingsObj.query.filter_by(fk_group_id=company_group_id).first()
  db_group_settings_dict = arr_of_dict_all_columns_single_item_function(db_group_settings_obj)
  # categories fix
  categories_edit = db_group_settings_dict['categories'].replace(',',', ')
  db_group_settings_dict['categories'] = categories_edit
  page_dict['db_group_settings_dict'] = db_group_settings_dict
  # ------------------------ assign to dict end ------------------------
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
@employees_views_interior.route('/employees/request', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/request/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_categories_request_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_categories_request_function START ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ pull/create latest test start ------------------------
  user_group_id = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).order_by(EmployeesGroupsObj.created_timestamp.desc()).first()
  db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=user_group_id.public_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
  first_test_exists = False
  if db_tests_obj == None or db_tests_obj == []:
    pass
  else:
    first_test_exists = True
  page_dict['first_test_exists'] = first_test_exists
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
      insert_new_row = EmployeesDesiredCategoriesObj(
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
@employees_views_interior.route('/employees/schedule', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/schedule/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_schedule_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_schedule_function START ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ assign to dict start ------------------------
  page_dict['activity_type'] = 'trivia'
  # ------------------------ assign to dict end ------------------------
  # ------------------------ get current group settings start ------------------------
  user_group_id = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).order_by(EmployeesGroupsObj.created_timestamp.desc()).first()
  db_group_settings_obj = EmployeesGroupSettingsObj.query.filter_by(fk_group_id=user_group_id.public_group_id).order_by(EmployeesGroupSettingsObj.created_timestamp.desc()).first()
  db_group_settings_dict = arr_of_dict_all_columns_single_item_function(db_group_settings_obj)
  page_dict['db_group_settings_dict'] = db_group_settings_dict
  page_dict['weekdays'], page_dict['times'], page_dict['timezones'] = days_times_timezone_arr_function()
  page_dict['quiz_cadence_arr'], page_dict['question_num_arr'], page_dict['question_type_arr'] = question_choices_function()
  page_dict['dropdowns_dict'] = get_dropdowns_trivia_function()
  # ------------------------ get current group settings end ------------------------
  # ------------------------ pull/create latest test start ------------------------
  db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=user_group_id.public_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
  first_test_exists = False
  if db_tests_obj == None or db_tests_obj == []:
    pass
  else:
    first_test_exists = True
  page_dict['first_test_exists'] = first_test_exists
  # ------------------------ pull/create latest test end ------------------------
  # ------------------------ get all categories start ------------------------
  query_result_arr_of_dicts = select_general_function('select_all_employees_categories_v1')
  page_dict['all_categories_arr'] = all_employee_question_categories_sorted_function(query_result_arr_of_dicts)
  # ------------------------ get all categories end ------------------------
  if request.method == 'POST':
    ui_select_all_categories = request.form.get('flexSwitchCheckDefault_02')
    ui_timezone = request.form.get('radioTimeZone')
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
    # ------------------------ check if ui is invalid start ------------------------
    if ui_start_day == None and ui_start_time == None and ui_end_day == None and ui_end_time == None and ui_cadence == None and ui_total_questions == None and ui_question_type == None:
      # ------------------------ defaults start ------------------------
      ui_start_day = 'Monday'
      ui_start_time = '12 PM'
      ui_end_day = 'Thursday'
      ui_end_time = '1 PM'
      ui_cadence = 'Weekly'
      ui_total_questions = 10
      ui_question_type = 'Mixed'
      # ------------------------ defaults end ------------------------
    if ui_start_day not in page_dict['weekdays'] or ui_end_day not in page_dict['weekdays'] or ui_start_time not in page_dict['times'] or ui_end_time not in page_dict['times'] or ui_timezone not in page_dict['timezones'] or ui_cadence not in page_dict['quiz_cadence_arr'] or int(ui_total_questions) not in page_dict['question_num_arr'] or ui_question_type not in page_dict['question_type_arr']:
      return redirect(url_for('employees_views_interior.employees_schedule_function', url_redirect_code='e6'))
    if ui_selected_categories != [] and ui_selected_categories != None:
      for i in ui_selected_categories:
        if i not in page_dict['all_categories_arr']:
          return redirect(url_for('employees_views_interior.employees_schedule_function', url_redirect_code='e6'))
    # ------------------------ check if ui is invalid start ------------------------
    # ------------------------ if settings changed start ------------------------
    settings_change_occured = False
    # ------------------------ if 'all_categories' selected start ------------------------
    if ui_select_all_categories == 'all_categories':
      if db_group_settings_dict['categories'] == 'all_categories':
        pass
      else:
        settings_change_occured = True
        db_group_settings_obj.categories = 'all_categories'
    # ------------------------ if 'all_categories' selected end ------------------------
    # ------------------------ if 'all_categories' not selected start ------------------------
    if ui_select_all_categories == None:
      if ui_selected_categories == [] or len(ui_selected_categories) == 0:
        return redirect(url_for('employees_views_interior.employees_schedule_function', url_redirect_code='e7'))
      ui_selected_categories_str = ",".join(ui_selected_categories)
      if ui_selected_categories_str == db_group_settings_dict['categories']:
        pass
      else:
        settings_change_occured = True
        db_group_settings_obj.categories = ui_selected_categories_str
        # ------------------------ email self start ------------------------
        try:
          output_to_email = os.environ.get('TRIVIAFY_NOTIFICATIONS_EMAIL')
          output_subject = f'Triviafy - Employees Settings Categories Changed - {current_user.email}'
          output_body = f"<p>Hi there,</p>\
                          <p>{current_user.email} changed their categories to: [{ui_selected_categories_str}]</p>\
                          <p style='margin:0;'>Best,</p>\
                          <p style='margin:0;'>Triviafy Support Team</p>"
          send_email_template_function(output_to_email, output_subject, output_body)
        except:
          pass
        # ------------------------ email self end ------------------------
    # ------------------------ if 'all_categories' not selected end ------------------------
    if ui_start_day != db_group_settings_dict['start_day']:
      settings_change_occured = True
      db_group_settings_obj.start_day = ui_start_day
    if ui_start_time != db_group_settings_dict['start_time']:
      settings_change_occured = True
      db_group_settings_obj.start_time = ui_start_time
    if ui_end_day != db_group_settings_dict['end_day']:
      settings_change_occured = True
      db_group_settings_obj.end_day = ui_end_day
    if ui_end_time != db_group_settings_dict['end_time']:
      settings_change_occured = True
      db_group_settings_obj.end_time = ui_end_time
    if ui_timezone != db_group_settings_dict['timezone']:
      settings_change_occured = True
      db_group_settings_obj.timezone = ui_timezone
    if ui_cadence != db_group_settings_dict['cadence']:
      settings_change_occured = True
      db_group_settings_obj.cadence = ui_cadence
    if int(ui_total_questions) != db_group_settings_dict['total_questions']:
      settings_change_occured = True
      db_group_settings_obj.total_questions = ui_total_questions
    if ui_question_type != db_group_settings_dict['question_type']:
      settings_change_occured = True
      db_group_settings_obj.question_type = ui_question_type
    # ------------------------ if new start/end day/times make sense start ------------------------
    start_day_index = page_dict['weekdays'].index(ui_start_day)
    start_time_index = page_dict['times'].index(ui_start_time)
    end_day_index = page_dict['weekdays'].index(ui_end_day)
    end_time_index = page_dict['times'].index(ui_end_time)
    if start_day_index > end_day_index or (start_day_index == end_day_index and start_time_index >= end_time_index):
      return redirect(url_for('employees_views_interior.employees_schedule_function', url_redirect_code='e8'))
    # ------------------------ if new start/end day/times make sense end ------------------------
    if settings_change_occured == True:
      db.session.commit()
      # ------------------------ if first quiz immediate is checked - after changes start ------------------------
      if first_test_exists == False:
        create_quiz_status = create_quiz_function(page_dict['db_group_settings_dict']['fk_group_id'], True)
        if create_quiz_status == 'false_end_time':
          return redirect(url_for('employees_views_interior.employees_schedule_function', url_redirect_code='e8'))
        if create_quiz_status == True:
          return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s3'))
      # ------------------------ if first quiz immediate is checked - after changes end ------------------------
      return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s2'))
    # ------------------------ if settings changed end ------------------------
    # ------------------------ if first quiz immediate is checked - no changes to existing settings start ------------------------
    if first_test_exists == False:
      create_quiz_status = create_quiz_function(page_dict['db_group_settings_dict']['fk_group_id'], True)
      if create_quiz_status == 'false_end_time':
        return redirect(url_for('employees_views_interior.employees_schedule_function', url_redirect_code='e8'))
      if create_quiz_status == True:
        return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='s3'))
    # ------------------------ if first quiz immediate is checked - no changes to existing settings end ------------------------
    # ------------------------ if no change in settings start ------------------------
    if settings_change_occured == False:
      return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='i1'))
    # ------------------------ if no change in settings end ------------------------
  localhost_print_function(' ------------------------ employees_schedule_function END ------------------------ ')
  return render_template('employees/interior/schedule/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/t', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/<url_test_id>', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/<url_test_id>/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/<url_test_id>/<url_question_number>', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/<url_test_id>/<url_question_number>/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/<url_test_id>/<url_question_number>/<url_initial_page_load>', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/<url_test_id>/<url_question_number>/<url_initial_page_load>/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/t/<url_test_id>/<url_question_number>/<url_initial_page_load>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_test_id_function(url_redirect_code=None, url_test_id=None, url_question_number='1', url_initial_page_load=None):
  localhost_print_function(' ------------------------ employees_test_id_function START ------------------------ ')
  template_location_url = 'employees/interior/test_quiz/index.html'
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ redirect to latest test id start ------------------------
  user_group_id = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).order_by(EmployeesGroupsObj.created_timestamp.desc()).first()
  if url_test_id == None:
    db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=user_group_id.public_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
    if db_tests_obj == None or db_tests_obj == []:
      return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
    else:
      return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=db_tests_obj.id, url_question_number='1', url_initial_page_load='init'))
  # ------------------------ redirect to latest test id end ------------------------
  # ------------------------ first user first quiz delete logic start ------------------------
  page_dict['first_user_first_quiz_can_replace'] = first_user_first_quiz_check_function(current_user.company_name)
  if url_test_id == 'fufq_remove':
    if page_dict['first_user_first_quiz_can_replace'] == True:
      check_latest_test_obj = EmployeesTestsObj.query.filter_by(fk_group_id=user_group_id.public_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
      EmployeesTestsObj.query.filter_by(id=check_latest_test_obj.id).delete()
      EmployeesTestsGradedObj.query.filter_by(fk_test_id=check_latest_test_obj.id).delete()
      EmployeesGroupQuestionsUsedObj.query.filter_by(fk_test_id=check_latest_test_obj.id).delete()
      db.session.commit()
      return redirect(url_for('employees_views_interior.employees_schedule_function'))
  # ------------------------ first user first quiz delete logic end ------------------------
  # ------------------------ on initial page load - redirect to first unanswered question start ------------------------
  # ------------------------ pull latest graded start ------------------------
  if url_initial_page_load == 'init':
    db_test_grading_obj = EmployeesTestsGradedObj.query.filter_by(fk_test_id=url_test_id, fk_user_id=current_user.id, status='wip').first()
    try:
      db_test_grading_dict = arr_of_dict_all_columns_single_item_function(db_test_grading_obj)
      # ------------------------ pull latest graded end ------------------------
      # ------------------------ pull question left off on initial load only start ------------------------
      unanswered_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
      for i in json.loads(db_test_grading_dict['test_obj']):
        already_answered_question_number = str(i['question_number'])
        if already_answered_question_number in unanswered_arr:
          unanswered_arr.remove(already_answered_question_number)
      if str(url_question_number) != unanswered_arr[0]:
        return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=url_test_id, url_question_number=unanswered_arr[0]))
      # ------------------------ pull question left off on initial load only end ------------------------
    except:
      pass
  # ------------------------ on initial page load - redirect to first unanswered question end ------------------------
  # ------------------------ pull test id start ------------------------
  test_id = url_test_id
  db_tests_obj = EmployeesTestsObj.query.filter_by(id=test_id).first()
  if db_tests_obj == None or db_tests_obj == []:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ pull test id end ------------------------
  # ------------------------ validate question number start ------------------------
  total_questions = int(db_tests_obj.total_questions)
  try:
    url_question_number = int(url_question_number)
  except:
    return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=test_id, url_question_number='1'))
  if url_question_number > total_questions or url_question_number < 1:
    return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=test_id, url_question_number='1'))
  # ------------------------ validate question number end ------------------------
  # ------------------------ pull specific question id start ------------------------
  question_ids_str = db_tests_obj.question_ids
  question_ids_arr = question_ids_str.split(',')
  desired_question_id = question_ids_arr[url_question_number-1]
  # ------------------------ pull specific question id end ------------------------
  # ------------------------ pull question from db start ------------------------
  db_question_obj = CreatedQuestionsObj.query.filter_by(id=desired_question_id).first()
  db_question_dict = arr_of_dict_all_columns_single_item_function(db_question_obj, for_json_dumps=True)
  # ------------------------ append question type start ------------------------
  question_type_order_str = db_tests_obj.question_types_order
  question_type_order_arr = question_type_order_str.split(',')
  desired_question_type = question_type_order_arr[url_question_number-1]
  db_question_dict['desired_question_type'] = desired_question_type
  # ------------------------ append question type end ------------------------
  page_dict['db_question_dict'] = db_question_dict
  # ------------------------ pull question from db end ------------------------
  # ------------------------ fix categories presentation start ------------------------
  page_dict['db_question_dict']['categories'] = categories_tuple_function(page_dict['db_question_dict']['categories'])
  # ------------------------ fix categories presentation end ------------------------
  # ------------------------ pull user info start ------------------------
  page_dict['user_company_name'] = current_user.company_name
  # ------------------------ pull user info end ------------------------
  # ------------------------ question order logic start ------------------------
  page_dict['current_question_number'] = str(int(url_question_number))
  page_dict['next_question_number'] = str(int(url_question_number) + 1)
  page_dict['previous_question_number'] = str(int(url_question_number) - 1)
  if int(db_tests_obj.total_questions) == int(url_question_number):
    page_dict['next_question_number'] = 'submit'
  # ------------------------ question order logic end ------------------------
  # ------------------------ test variables start ------------------------
  page_dict['test_total_questions'] = db_tests_obj.total_questions
  test_total_questions_arr = []
  for i in range(int(db_tests_obj.total_questions)):
    test_total_questions_arr.append(str(i+1))
  page_dict['test_total_questions_arr'] = test_total_questions_arr
  page_dict['url_test_id'] = url_test_id
  # ------------------------ test variables end ------------------------
  # ------------------------ contains image check start ------------------------
  contains_img = False
  if 'amazonaws.com' in page_dict['db_question_dict']['aws_image_url']:
    contains_img = True
  page_dict['question_contains_image'] = contains_img
  # ------------------------ contains image check end ------------------------
  # ------------------------ redirect variables start ------------------------
  page_dict['db_question_dict']['redirect_ui_answer'] = ''
  page_dict['latest_test_completed'] = False
  try:
    db_test_grading_obj = EmployeesTestsGradedObj.query.filter_by(fk_test_id=url_test_id, fk_user_id=current_user.id).first()
    db_test_grading_dict = arr_of_dict_all_columns_single_item_function(db_test_grading_obj)
    master_answer_arr_of_dict = json.loads(db_test_grading_dict['test_obj'])
    for i in master_answer_arr_of_dict:
      if int(i['question_number']) == int(url_question_number):
        page_dict['db_question_dict']['redirect_ui_answer'] = i['ui_answer']
    if db_test_grading_dict['status'] == 'complete':
      page_dict['latest_test_completed'] = True
  except:
    pass
  # ------------------------ redirect variables end ------------------------
  # ------------------------ archive logic start ------------------------
  page_dict['view_as_archive'] = False
  try:
    if db_tests_obj.status == 'Closed':
      page_dict['view_as_archive'] = True
      # ------------------------ get teammate answers start ------------------------
      teammate_answers_tuple = []
      db_test_grading_obj = EmployeesTestsGradedObj.query.filter_by(fk_test_id=url_test_id).all()
      for i_obj in db_test_grading_obj:
        db_user_obj = UserObj.query.filter_by(id=i_obj.fk_user_id).first()
        users_master_test_results_arr_of_dict = json.loads(i_obj.test_obj)
        for i_dict in users_master_test_results_arr_of_dict:
          i_question_number = i_dict['question_number']
          if int(i_question_number) == int(url_question_number):
            i_ui_answer = i_dict['ui_answer']
            # ------------------------ capitalize mcq answer start ------------------------
            if len(i_ui_answer) == 1:
              i_ui_answer = i_ui_answer.upper()
            # ------------------------ capitalize mcq answer end ------------------------
            # ------------------------ shorten email start ------------------------
            i_email = db_user_obj.email
            i_email_arr = i_email.split('@')
            i_email = i_email_arr[0]
            if len(i_email) > 15:
              i_email = i_email[0:15]
            # ------------------------ shorten email end ------------------------
            teammate_answers_tuple.append((i_email, i_ui_answer))
            break
      page_dict['teammate_answers_tuple'] = teammate_answers_tuple
      # ------------------------ get teammate answers end ------------------------
  except:
    pass
  # ------------------------ archive logic end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['stripe_subscription_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  if page_dict['view_as_archive'] == False: # no user inputs should be accepted since this test is closed.
    # ------------------------ ui post start ------------------------
    if request.method == 'POST':
      # ------------------------ user input start ------------------------
      ui_answer = ''
      ui_answer_is_correct = False
      # ------------------------ user input - fill in the blank start ------------------------
      if page_dict['db_question_dict']['desired_question_type'] == 'Fill in the blank':
        ui_answer = request.form.get('ui_answer_fitb')
        # ------------------------ validate ui start ------------------------
        if len(ui_answer) < 1 or len(ui_answer) > 280:
          return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=url_test_id, url_question_number=str(url_question_number), url_redirect_code='e6'))
        # ------------------------ validate ui end ------------------------
        # ------------------------ grade ui start ------------------------
        grade_quiz_function(ui_answer, url_test_id, db_tests_obj.total_questions, url_question_number, db_question_dict, current_user.id, user_group_id.public_group_id)
        # ------------------------ grade ui end ------------------------
      # ------------------------ user input - fill in the blank end ------------------------
      # ------------------------ user input - multiple choice start ------------------------
      if page_dict['db_question_dict']['desired_question_type'] == 'Multiple choice':
        ui_answer = request.form.get('ui_answer_mcq')
        # ------------------------ validate ui start ------------------------
        allowed_answers_arr = ['a', 'b', 'c', 'd', 'e']
        if ui_answer.lower() not in allowed_answers_arr:
          return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=url_test_id, url_question_number=str(url_question_number), url_redirect_code='e6'))
        # ------------------------ validate ui start ------------------------
        # ------------------------ grade ui start ------------------------
        grade_quiz_function(ui_answer, url_test_id, db_tests_obj.total_questions, url_question_number, db_question_dict, current_user.id, user_group_id.public_group_id)
        # ------------------------ grade ui end ------------------------
      # ------------------------ user input - multiple choice end ------------------------
      # ------------------------ user input end ------------------------
      if page_dict['next_question_number'] == 'submit':
        # ------------------------ pull latest graded start ------------------------
        db_test_grading_obj = EmployeesTestsGradedObj.query.filter_by(fk_test_id=url_test_id, fk_user_id=current_user.id).first()
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
          return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=url_test_id, url_question_number=unanswered_arr[0]))
      else:
        return redirect(url_for('employees_views_interior.employees_test_id_function', url_test_id=url_test_id, url_question_number=str(int(url_question_number)+1)))
    # ------------------------ ui post end ------------------------
  localhost_print_function(' ------------- 0 ------------- ')
  localhost_print_function(f"page_dict | type: {type(page_dict)}")
  for k, v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
  localhost_print_function(' ------------- 0 ------------- ')
  localhost_print_function(' ------------------------ employees_test_id_function end ------------------------ ')
  return render_template('employees/interior/test_quiz/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/archive')
@employees_views_interior.route('/employees/archive/<url_redirect_code>')
@login_required
def employees_test_archive_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_test_archive_function start ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ get current group start ------------------------
  db_group_obj = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).first()
  # ------------------------ get current group end ------------------------
  # ------------------------ pull all tests for group start ------------------------
  db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=db_group_obj.public_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).all()
  # ------------------------ pull all tests for group end ------------------------
  # ------------------------ turn sql obj into arr of dicts start ------------------------
  tests_arr_of_dicts = []
  for i_obj in db_tests_obj:
    i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
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
  localhost_print_function(' ------------------------ employees_test_archive_function end ------------------------ ')
  return render_template('employees/interior/test_archive/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/leaderboard')
@employees_views_interior.route('/employees/leaderboard/<url_redirect_code>')
@login_required
def employees_leaderboard_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_leaderboard_function start ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ get current users from company start ------------------------
  users_arr_of_dicts = []
  db_users_obj = UserObj.query.filter_by(company_name=current_user.company_name).order_by(UserObj.email.asc()).all()
  for i in db_users_obj:
    i_dict = {}
    user_id = i.id
    user_email = i.email
    # ------------------------ get total correct start ------------------------
    total_correct = int(0)
    db_test_grading_obj = EmployeesTestsGradedObj.query.filter_by(fk_user_id=user_id).all()
    for j in db_test_grading_obj:
      # ------------------------ check if test is closed start ------------------------
      db_tests_obj = EmployeesTestsObj.query.filter_by(id=j.fk_test_id).first()
      if db_tests_obj.status == 'Closed':
        total_correct += int(j.correct_count)
      # ------------------------ check if test is closed end ------------------------
    # ------------------------ get total correct end ------------------------
    i_dict['user_id'] = user_id
    i_dict['user_email'] = user_email
    i_dict['total_correct'] = total_correct
    i_dict['total_wins'] = int(0)
    users_arr_of_dicts.append(i_dict)
  # ------------------------ get current users from company end ------------------------
  # ------------------------ pull all tests for group start ------------------------
  db_group_obj = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).first()
  db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=db_group_obj.public_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).all()
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
  localhost_print_function(' ------------------------ employees_leaderboard_function end ------------------------ ')
  return render_template('employees/interior/leaderboard/index.html', page_dict_to_html=page_dict)
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
  return redirect(url_for('employees_views_interior.employees_account_function', url_redirect_code='s5'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/account', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/account/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/account/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_account_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_account_function START ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['stripe_subscription_status'] = stripe_subscription_obj_status
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
      db_capacity_obj = EmployeesCapacityOptionsObj.query.filter_by(fk_stripe_price_id=stripe_subscription_current_price_id).first()
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
        return redirect(url_for('employees_views_interior.employees_account_function', url_redirect_code='e6'))
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
          new_row_email = EmployeesEmailSentObj(
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
        return redirect(url_for('employees_views_interior.employees_account_function', url_redirect_code='s1'))
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
      db_capacity_obj = EmployeesCapacityOptionsObj.query.filter_by(id=ui_subscription_selected).first()
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
            cancel_url='http://127.0.0.1:80/employees/account',
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
            cancel_url='https://triviafy.com/employees/account',
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
  localhost_print_function(' ------------------------ employees_account_function END ------------------------ ')
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
  page_dict['stripe_subscription_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ non subscribed users should not see this page start ------------------------
  if page_dict['stripe_subscription_status'] != 'active' or url_feature_request_code == None:
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
      db_feature_requested_obj = EmployeesFeatureRequestObj.query.filter_by(fk_user_id=current_user.id, feature_requested=ui_feature_request).first()
      if db_feature_requested_obj == None or db_feature_requested_obj == []:
        # ------------------------ insert email to db start ------------------------
        try:
          db_groups_obj = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).first()
          new_row = EmployeesFeatureRequestObj(
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
@employees_views_interior.route('/employees/questions', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/questions/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/questions/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_questions_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_questions_function START ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['stripe_subscription_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ redirect if not subscribed start ------------------------
  if page_dict['stripe_subscription_status'] != 'active':
    return redirect(url_for('employees_views_interior.employees_account_function', url_redirect_code='e14'))
  # ------------------------ redirect if not subscribed end ------------------------
  db_groups_obj = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).first()
  # ------------------------ delete all in progress questions start ------------------------
  db_drafted_questions_obj = CreatedQuestionsObj.query.filter_by(fk_group_id=db_groups_obj.public_group_id,submission='draft').first()
  if db_drafted_questions_obj != None and db_drafted_questions_obj != []:
    CreatedQuestionsObj.query.filter_by(fk_group_id=db_groups_obj.public_group_id,submission='draft').delete()
    db.session.commit()
    return redirect(url_for('employees_views_interior.employees_questions_function'))
  # ------------------------ delete all in progress questions end ------------------------
  # ------------------------ pull all created questions by group start ------------------------
  db_created_questions_obj = CreatedQuestionsObj.query.filter_by(fk_group_id=db_groups_obj.public_group_id).all()
  group_created_questions_arr_of_dicts = []
  for i_obj in db_created_questions_obj:
    i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
    # ------------------------ append creator email start ------------------------
    db_user_obj = UserObj.query.filter_by(id=i_dict['fk_user_id']).first()
    i_dict['created_by_email'] = db_user_obj.email
    # ------------------------ append creator email end ------------------------
    # ------------------------ append asked status start ------------------------
    i_dict['question_used_status'] = 'Include in future quiz'
    db_used_obj = EmployeesGroupQuestionsUsedObj.query.filter_by(fk_question_id=i_dict['id'], fk_group_id=db_groups_obj.public_group_id).first()
    if db_used_obj != None and db_used_obj != []:
      i_dict['question_used_status'] = 'Included in past quiz'
    # ------------------------ append asked status end ------------------------
    group_created_questions_arr_of_dicts.append(i_dict)
  page_dict['group_created_questions_arr_of_dicts'] = group_created_questions_arr_of_dicts
  page_dict['total_group_created_questions_arr_of_dicts'] = len(group_created_questions_arr_of_dicts)
  # ------------------------ pull all created questions by group end ------------------------
  localhost_print_function(' ------------------------ employees_questions_function END ------------------------ ')
  return render_template('employees/interior/create_question/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/questions/v3', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/questions/v3/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/questions/v3/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_create_question_v3_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_create_question_v3_function START ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function_v2(current_user, 'employees', current_user.email)
  page_dict['stripe_subscription_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ redirect if not subscribed start ------------------------
  if page_dict['stripe_subscription_status'] != 'active':
    return redirect(url_for('employees_views_interior.employees_account_function', url_redirect_code='e14'))
  # ------------------------ redirect if not subscribed end ------------------------
  page_dict['user_company_name'] = current_user.company_name
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
      db_groups_obj = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).first()
      # ------------------------ append answers start ------------------------
      concat_ui_answer = ui_answer.upper() + ', ' + ui_answer_fitb.lower()
      # ------------------------ append answers end ------------------------
      new_row = CreatedQuestionsObj(
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
        product = 'employees',
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
  localhost_print_function(' ------------------------ employees_create_question_v3_function END ------------------------ ')
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
  page_dict['stripe_subscription_status'] = stripe_subscription_obj_status
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ redirect if not subscribed start ------------------------
  if page_dict['stripe_subscription_status'] != 'active':
    return redirect(url_for('employees_views_interior.employees_account_function', url_redirect_code='e14'))
  # ------------------------ redirect if not subscribed end ------------------------
  # ------------------------ redirect if question id none start ------------------------
  if url_question_id == None:
    return redirect(url_for('employees_views_interior.employees_questions_function', url_redirect_code='e16'))
  # ------------------------ redirect if question id none end ------------------------
  page_dict['user_company_name'] = current_user.company_name
  page_dict['user_company_name'] = page_dict['user_company_name'].title()
  # ------------------------ get latest custom question start ------------------------
  db_question_obj = CreatedQuestionsObj.query.filter_by(id=url_question_id).first()
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
    return redirect(url_for('employees_views_interior.employees_questions_function'))
  localhost_print_function(' ------------------------ employees_preview_question_function END ------------------------ ')
  return render_template('employees/interior/create_question/preview/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/feedback/primary', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feedback/primary/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feedback/primary/<url_redirect_code>', methods=['GET', 'POST'])

@login_required
def employees_feedback_primary_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_feedback_primary_function START ------------------------ ')
  # ------------------------ check if already answered start ------------------------
  feedback_primary_obj = EmployeesFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='primary_product_choice').first()
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
    new_row = EmployeesFeedbackObj(
      id = create_uuid_function('feedback_'),
      created_timestamp = create_timestamp_function(),
      fk_user_id = current_user.id,
      fk_email = current_user.email,
      question = 'primary_product_choice',
      response = ui_answer
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
@employees_views_interior.route('/employees/feedback/secondary', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feedback/secondary/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feedback/secondary/<url_redirect_code>', methods=['GET', 'POST'])

@login_required
def employees_feedback_secondary_function(url_redirect_code=None, value_to_remove=None):
  localhost_print_function(' ------------------------ employees_feedback_secondary_function START ------------------------ ')
  # ------------------------ check if already answered start ------------------------
  feedback_secondary_obj = EmployeesFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='secondary_product_choice').first()
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
  feedback_primary_obj = EmployeesFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='primary_product_choice').first()
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
    new_row = EmployeesFeedbackObj(
      id = create_uuid_function('feedback_'),
      created_timestamp = create_timestamp_function(),
      fk_user_id = current_user.id,
      fk_email = current_user.email,
      question = 'secondary_product_choice',
      response = ui_answer
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
@employees_views_interior.route('/employees/feedback/birthday', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feedback/birthday/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feedback/birthday/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_feedback_birthday_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_feedback_birthday_function START ------------------------ ')
  # ------------------------ check if already answered start ------------------------
  feedback_birthday_obj = EmployeesFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='birthday_choice').first()
  if feedback_birthday_obj != None and feedback_birthday_obj != []:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ check if already answered end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['feedback_step'] = '3'
  page_dict['feedback_request'] = 'birthday'
  # ------------------------ set variables end ------------------------
  # ------------------------ get questions start ------------------------
  favorite_questions_arr, favorite_questions_arr_index = get_favorite_questions_function()
  page_dict['favorite_questions_arr'] = favorite_questions_arr
  page_dict['favorite_questions_arr_index'] = favorite_questions_arr_index
  # ------------------------ get questions end ------------------------
  # ------------------------ get month days dict start ------------------------
  months_arr, days_arr, month_day_dict = get_month_days_function()
  page_dict['months_arr'] = months_arr
  page_dict['days_arr'] = days_arr
  # ------------------------ get month days dict end ------------------------
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    # ------------------------ get user inputs start ------------------------
    ui_birthday_question = request.form.get('ui_birthday_question')
    ui_birthday_answer = request.form.get('ui_birthday_answer')
    ui_birthday_month = request.form.get('ui_birthday_month')
    ui_birthday_day = request.form.get('ui_birthday_day')
    # ------------------------ get user inputs end ------------------------
    # ------------------------ sanatize inputs start ------------------------
    # question
    if ui_birthday_question not in favorite_questions_arr:
      return redirect(url_for('employees_views_interior.employees_feedback_birthday_function', url_redirect_code='e17'))
    # answer
    if len(ui_birthday_answer) == 0 or len(ui_birthday_answer) > 100:
      return redirect(url_for('employees_views_interior.employees_feedback_birthday_function', url_redirect_code='e19'))
    special_characters_arr = get_special_characters_function()
    for i in ui_birthday_answer:
      if i in special_characters_arr:
        return redirect(url_for('employees_views_interior.employees_feedback_birthday_function', url_redirect_code='e18'))
    # birth month
    if int(ui_birthday_month) not in months_arr:
      return redirect(url_for('employees_views_interior.employees_feedback_birthday_function', url_redirect_code='e20'))
    # birth day
    allowed_days_arr = month_day_dict[str(ui_birthday_month)]
    if int(ui_birthday_day) not in allowed_days_arr:
      return redirect(url_for('employees_views_interior.employees_feedback_birthday_function', url_redirect_code='e21'))
    # ------------------------ sanatize inputs end ------------------------
    try:
      new_birthday_row_id = create_uuid_function('birthday_')
      # ------------------------ insert to db start ------------------------
      new_row = EmployeesBirthdayInfoObj(
        id = new_birthday_row_id,
        created_timestamp = create_timestamp_function(),
        fk_user_id = current_user.id,
        question = ui_birthday_question,
        answer = ui_birthday_answer,
        birth_month = int(ui_birthday_month),
        birth_day = int(ui_birthday_day)
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ insert to db end ------------------------
      try:
        # ------------------------ insert to db start ------------------------
        new_row = EmployeesFeedbackObj(
          id = create_uuid_function('feedback_'),
          created_timestamp = create_timestamp_function(),
          fk_user_id = current_user.id,
          fk_email = current_user.email,
          question = 'birthday_choice',
          response = new_birthday_row_id
        )
        db.session.add(new_row)
        db.session.commit()
        # ------------------------ insert to db end ------------------------
      except:
        pass
    except:
      pass
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ submission end ------------------------
  localhost_print_function(' ------------------------ employees_feedback_birthday_function END ------------------------ ')
  return render_template('employees/interior/feedback/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/feedback/birthday/skip', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feedback/birthday/skip/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feedback/birthday/skip/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_feedback_birthday_skip_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_feedback_birthday_skip_function START ------------------------ ')
  # ------------------------ check if already answered start ------------------------
  feedback_birthday_obj = EmployeesFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='birthday_choice').first()
  if feedback_birthday_obj != None and feedback_birthday_obj != []:
    return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
  # ------------------------ check if already answered end ------------------------
  # ------------------------ skip logic start ------------------------
  try:
    # ------------------------ insert to db start ------------------------
    new_row = EmployeesFeedbackObj(
      id = create_uuid_function('feedback_'),
      created_timestamp = create_timestamp_function(),
      fk_user_id = current_user.id,
      fk_email = current_user.email,
      question = 'birthday_choice',
      response = 'feedback skipped'
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ insert to db end ------------------------
  except:
    pass
  # ------------------------ skip logic end ------------------------
  localhost_print_function(' ------------------------ employees_feedback_birthday_skip_function END ------------------------ ')
  return redirect(url_for('employees_views_interior.login_dashboard_page_function'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_interior.route('/employees/feedback/marketing', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feedback/marketing/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feedback/marketing/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def employees_feedback_marketing_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ employees_feedback_marketing_function START ------------------------ ')
  # ------------------------ check if already answered start ------------------------
  feedback_marketing_obj = EmployeesFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='marketing_choice').first()
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
  page_dict['feedback_step'] = '4'
  page_dict['feedback_request'] = 'marketing'
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    ui_answer = request.form.get('ui_selection_radio')
    # ------------------------ invalid start ------------------------
    if ui_answer not in marketing_list:
      return redirect(url_for('employees_views_interior.employees_feedback_marketing_function'))
    # ------------------------ invalid end ------------------------
    # ------------------------ insert to db start ------------------------
    new_row = EmployeesFeedbackObj(
      id = create_uuid_function('feedback_'),
      created_timestamp = create_timestamp_function(),
      fk_user_id = current_user.id,
      fk_email = current_user.email,
      question = 'marketing_choice',
      response = ui_answer
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
@employees_views_interior.route('/employees/feedback/name', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feedback/name/', methods=['GET', 'POST'])
@employees_views_interior.route('/employees/feedback/name/<url_redirect_code>', methods=['GET', 'POST'])
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
    current_user.name = ui_name
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
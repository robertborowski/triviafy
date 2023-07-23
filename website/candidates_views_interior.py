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
from website.models import UserObj, StripeCheckoutSessionObj, ActivityACreatedQuestionsObj
from website.backend.candidates.browser import browser_response_set_cookie_function, browser_response_set_cookie_function_v2
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.backend.candidates.datatype_conversion_manipulation import one_col_dict_to_arr_function
from website import db
from website.backend.candidates.user_inputs import validate_upload_candidate_function, sanitize_loop_check_if_exists_within_arr_function, sanitize_check_if_str_exists_within_arr_function, sanitize_create_question_categories_function, sanitize_create_question_question_function, sanitize_create_question_options_function, sanitize_create_question_answer_function, sanitize_create_question_option_e_function, sanitize_letters_numbers_spaces_only_function, alert_message_default_function, sanitize_char_count_1_function
from website.backend.candidates.send_emails import send_email_template_function
import pandas as pd
from website.backend.candidates.string_manipulation import all_question_candidate_categories_sorted_function, create_assessment_name_function
from website.backend.candidates.sqlalchemy_manipulation import pull_desired_languages_arr_function
from website.backend.candidates.dict_manipulation import create_assessment_info_dict_function_v2, create_question_info_dict_function, arr_of_dict_necessary_columns_function, categories_tuple_function, arr_of_dict_all_columns_single_item_function
from website.backend.candidates.datetime_manipulation import next_x_days_function, times_arr_function, expired_assessment_check_function
import datetime
import json
import stripe
import os
from website.backend.candidates.aws_manipulation import candidates_change_uploaded_image_filename_function, candidates_user_upload_image_checks_aws_s3_function
from website.backend.candidates.sql_statements.sql_prep import prepare_where_clause_function, prepare_question_ids_where_clause_function
from website.backend.candidates.stripe import check_stripe_subscription_status_function, convert_current_period_end_function
from website.backend.candidates.user_inputs import alert_message_default_function_v2
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
candidates_views_interior = Blueprint('candidates_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ before page variables start ------------------------
cache_busting_output = create_uuid_function('css_')
# ------------------------ before page variables end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/')
@candidates_views_interior.route('/candidates/dashboard')
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
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'candidates/interior/dashboard/index.html'
  # ------------------------ for setting cookie end ------------------------
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 'e':
      alert_message_page = 'Error.'
      alert_message_type = 'danger'
  # ------------------------ redirect codes end ------------------------
  # ------------------------ delete test drafts start ------------------------
  # db.session.commit()
  # ------------------------ delete test drafts end ------------------------
  # ------------------------ get users total assessments created start ------------------------
  # len_test_created_obj = len(test_created_obj)
  # ------------------------ redirect new users to create assessment start ------------------------
  # if len_test_created_obj == 0:
  #   localhost_print_function(' ------------------------ login_dashboard_page_function END ------------------------ ')
  #   return redirect(url_for('candidates_views_interior.candidates_assessment_create_new_function', step_status='1'))
  # ------------------------ redirect new users to create assessment end ------------------------
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type)
  else:
    browser_response = browser_response_set_cookie_function(current_user, template_location_url)
    localhost_print_function(' ------------------------ login_dashboard_page_function END ------------------------ ')
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/subscription/success')
@login_required
def candidates_subscription_success_function():
  localhost_print_function(' ------------------------ candidates_subscription_success_function START ------------------------ ')
  # ------------------------ get from db start ------------------------
  db_checkout_session_obj = StripeCheckoutSessionObj.query.filter_by(fk_user_id=current_user.id,status='draft').order_by(StripeCheckoutSessionObj.created_timestamp.desc()).first()
  # ------------------------ get from db end ------------------------
  # ------------------------ if not found start ------------------------
  if db_checkout_session_obj == None or db_checkout_session_obj == '' or db_checkout_session_obj == False:
    localhost_print_function(' ------------------------ candidates_subscription_success_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.login_dashboard_page_function'))
  # ------------------------ if not found end ------------------------
  # ------------------------ get desired start ------------------------
  fk_checkout_session_id = db_checkout_session_obj.fk_checkout_session_id
  # ------------------------ get desired end ------------------------
  # ------------------------ stripe lookup start ------------------------
  stripe_checkout_session_obj = stripe.checkout.Session.retrieve(fk_checkout_session_id)
  # ------------------------ if not found start ------------------------
  if stripe_checkout_session_obj == None:
    localhost_print_function(' ------------------------ candidates_subscription_success_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.login_dashboard_page_function'))
  # ------------------------ if not found end ------------------------
  # ------------------------ if not finalized start ------------------------
  stripe_checkout_session_payment_status = stripe_checkout_session_obj.payment_status
  if stripe_checkout_session_payment_status != 'paid':
    localhost_print_function(' ------------------------ candidates_subscription_success_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.login_dashboard_page_function'))
  # ------------------------ if not finalized end ------------------------
  stripe_customer_id = stripe_checkout_session_obj.customer
  stripe_subscription_id = stripe_checkout_session_obj.subscription
  # ------------------------ stripe lookup end ------------------------
  # ------------------------ update db start ------------------------
  user_obj = UserObj.query.filter_by(id=current_user.id).first()
  user_obj.fk_stripe_customer_id = stripe_customer_id
  user_obj.fk_stripe_subscription_id = stripe_subscription_id
  db_checkout_session_obj.status = 'final'
  db.session.commit()
  # ------------------------ update db end ------------------------
  # ------------------------ email self start ------------------------
  try:
    output_to_email = os.environ.get('TRIVIAFY_SUPPORT_EMAIL')
    output_subject = f'Triviafy - Subscription - {user_obj.email}'
    output_body = f"Hi there,\n\nNew user subscribed: {user_obj.email} \n\nBest,\nTriviafy"
    send_email_template_function(output_to_email, output_subject, output_body)
  except:
    pass
  # ------------------------ email self end ------------------------
  localhost_print_function(' ------------------------ candidates_subscription_success_function END ------------------------ ')
  return redirect(url_for('candidates_views_interior.candidates_account_settings_function_v2', url_redirect_code='s'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/account', methods=['GET', 'POST'])
@login_required
def candidates_account_settings_function_v2(url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_account_settings_function_v2 START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 's':
      alert_message_page = 'Successfully updated subscription.'
      alert_message_type = 'success'
    if redirect_var == 's2':
      alert_message_page = 'Successfully submitted message.'
      alert_message_type = 'success'
    if redirect_var == 'e':
      alert_message_page = 'Contact message must be only 1-280 characters long.'
      alert_message_type = 'danger'
  # ------------------------ redirect codes end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function(current_user)
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ get current plan from stripe start ------------------------
  current_plan_type = 'Free'
  stripe_current_period_end = ''
  if stripe_subscription_obj_status == 'not active':
    pass
  if stripe_subscription_obj_status == 'active':
    try:
      stripe_subscription_obj = stripe.Subscription.retrieve(current_user.fk_stripe_subscription_id)
      stripe_current_period_end = convert_current_period_end_function(stripe_subscription_obj)
      stripe_subscription_current_price_id = stripe_subscription_obj.plan.id
      db_capacity_obj = CandidatesCapacityOptionsObj.query.filter_by(fk_stripe_price_id=stripe_subscription_current_price_id).first()
      current_plan_type = db_capacity_obj.name
    except:
      current_plan_type = 'Free'
  # ------------------------ get current plan from stripe end ------------------------
  # ------------------------ get current user info start ------------------------
  user_obj = {
    'email': current_user.email,
    'name': current_user.name,
    'company_name': current_user.company_name
  }
  # ------------------------ get current user info end ------------------------
  # ------------------------ if post data start ------------------------
  if request.method == 'POST':
    # ------------------------ post uiMessage start ------------------------
    ui_message = request.form.get('uiMessage')
    if ui_message != None and ui_message != '' and ui_message != []:
      ui_message = sanitize_create_question_options_function(ui_message)
      if ui_message == False:
        localhost_print_function(' ------------------------ candidates_account_settings_function_v2 END ------------------------ ')
        return redirect(url_for('candidates_views_interior.candidates_account_settings_function_v2', url_redirect_code='e'))
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
          new_row_email = CandidatesEmailSentObj(
            id = create_uuid_function('email_test_'),
            created_timestamp = create_timestamp_function(),
            from_user_id_fk = current_user.id,
            to_email = output_to_email,
            assessment_expiring_url_fk = 'confirrm_email_sent',
            subject = output_subject,
            body = output_body
          )
          db.session.add(new_row_email)
          db.session.commit()
        except:
          pass
        # ------------------------ insert email to db end ------------------------
        localhost_print_function(' ------------------------ candidates_account_settings_function_v2 END ------------------------ ')
        return redirect(url_for('candidates_views_interior.candidates_account_settings_function_v2', url_redirect_code='s2'))
    # ------------------------ post uiMessage end ------------------------
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
    query_result_arr_of_dicts = select_general_function('select_all_capacity_options')
    capacity_options_arr = one_col_dict_to_arr_function(query_result_arr_of_dicts)
    if ui_subscription_selected not in capacity_options_arr:
      ui_subscription_selected = None
    # ------------------------ valid input check end ------------------------
    if ui_subscription_selected != None and ui_subscription_selected != '1m':
      # ------------------------ db get price id start ------------------------
      db_capacity_obj = CandidatesCapacityOptionsObj.query.filter_by(id=ui_subscription_selected).first()
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
        new_checkout_session_obj = StripeCheckoutSessionObj(
          id = create_uuid_function('ccheck_'),
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
      # ------------------------ stripe checkout end ------------------------
  # ------------------------ if post data end ------------------------
  localhost_print_function(' ------------------------ candidates_account_settings_function_v2 END ------------------------ ')
  return render_template('candidates/interior/account/index.html', user=current_user, users_company_name_to_html=current_user.company_name, user_email_to_html=current_user.email, current_plan_type_to_html=current_plan_type, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type, stripe_current_period_end_to_html=stripe_current_period_end, user_obj_to_html=user_obj)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/upload', methods=['GET', 'POST'])
@login_required
def candidates_upload_emails_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_upload_emails_function START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 'e1':
      alert_message_page = 'Invalid email'
      alert_message_type = 'danger'
    if redirect_var == 'e2':
      alert_message_page = 'Email already exists'
      alert_message_type = 'danger'
    if redirect_var == 'e3':
      alert_message_page = 'Upload was invalid file type (.csv only)'
      alert_message_type = 'danger'
  # ------------------------ redirect codes end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function(current_user)
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ candidate analytics start ------------------------
  db_candidates_obj = CandidatesUploadedCandidatesObj.query.filter_by(user_id_fk=current_user.id).order_by(CandidatesUploadedCandidatesObj.email).all()
  db_candidates_obj_exists = False
  if db_candidates_obj == None:
    pass
  else:
    db_candidates_obj_exists = True
    # ------------------------ pull necessary columns start ------------------------
    db_candidates_obj = arr_of_dict_necessary_columns_function(db_candidates_obj, ['email'])
    # ------------------------ pull necessary columns end ------------------------
    db_candidates_obj.append({'email': current_user.email})
    for i_dict in db_candidates_obj:
      # ------------------------ get schedule start ------------------------
      i_total_pending = 0
      db_schedule_pending_obj = CandidatesScheduleObj.query.filter_by(user_id_fk=current_user.id, candidates=i_dict['email'], candidate_status='Pending').all()
      try:
        i_total_pending = len(db_schedule_pending_obj)
      except:
        pass
      i_total_completed = 0
      db_schedule_completed_obj = CandidatesScheduleObj.query.filter_by(user_id_fk=current_user.id, candidates=i_dict['email'], candidate_status='Completed').all()
      try:
        i_total_completed = len(db_schedule_completed_obj)
      except:
        pass
      # ------------------------ get schedule end ------------------------
      i_dict['total_pending'] = i_total_pending
      i_dict['total_completed'] = i_total_completed
      # ------------------------ get grade start ------------------------
      i_dict['average_grade'] = '-'
      try:
        db_grade_obj = CandidatesAssessmentGradedObj.query.filter_by(created_assessment_user_id_fk=current_user.id, candidate_email=i_dict['email'], status='submitted').all()
        db_grade_obj = arr_of_dict_necessary_columns_function(db_grade_obj, ['total_questions', 'correct_count'])
        current_total_questions = 0
        current_total_correct_count = 0
        for j in db_grade_obj:
          current_total_questions += j['total_questions']
          current_total_correct_count += j['correct_count']
        i_dict['average_grade'] = str(int(float(float(current_total_correct_count) / float(current_total_questions)) * float(100))) + '%'
      except:
        pass
      # ------------------------ get grade end ------------------------
  # ------------------------ candidate analytics end ------------------------
  post_result = ''
  if request.method == 'POST':
    # ------------------------ user inputs start ------------------------
    ui_email = request.form.get('uiCandidateEmail')
    # ------------------------ user inputs end ------------------------
    # ------------------------ ui_email individual start ------------------------
    if ui_email != None and ui_email != '':
      post_result = validate_upload_candidate_function(db, current_user, ui_email, 'individual')
    # ------------------------ ui_email individual end ------------------------
    if stripe_subscription_obj_status == 'active':
      # ------------------------ form results start ------------------------
      ui_csv_file_uploaded = None
      try:
        ui_csv_file_uploaded = request.files['file']
      except:
        pass
      # ------------------------ form results end ------------------------
      # ------------------------ ui_email bulk start ------------------------
      if ui_csv_file_uploaded != None:
        try:
          filename = ui_csv_file_uploaded.filename
          if filename[-4:] != '.csv':
            post_result = 'e3'
          else:
            df_csv_data = pd.read_csv(ui_csv_file_uploaded)
            for i, r in df_csv_data.iterrows():
              ui_email = r[0]
              post_result = validate_upload_candidate_function(db, current_user, ui_email, 'bulk')
        except:
          post_result = 'e3'
      # ------------------------ ui_email bulk end ------------------------
    if post_result == 'success':
      # ------------------------ email self start ------------------------
      try:
        output_to_email = os.environ.get('TRIVIAFY_SUPPORT_EMAIL')
        output_subject = f'Triviafy - Candidate Uploaded - {current_user.email}'
        output_body = f"Hi there,\n\n{current_user.email} uploaded candidate(s).\n\nBest,\nTriviafy"
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self end ------------------------
      return redirect(url_for('candidates_views_interior.candidates_schedule_dashboard_function', url_redirect_code='s'))
    # ------------------------ if post error start ------------------------
    if post_result != 'success' and post_result != None and post_result != '':
      return redirect(url_for('candidates_views_interior.candidates_upload_emails_function', url_redirect_code=post_result))
    # ------------------------ if post error end ------------------------
  localhost_print_function(' ------------------------ candidates_upload_emails_function END ------------------------ ')
  return render_template('candidates/interior/candidates_page_templates/candidates_upload/index.html', user=current_user, stripe_subscription_obj_status_to_html=stripe_subscription_obj_status, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type, db_candidates_obj_exists_to_html=db_candidates_obj_exists, db_candidates_obj_to_html=db_candidates_obj)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/<url_email>', methods=['GET', 'POST'])
@login_required
def candidates_email_specific_function(url_email=None, url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_email_specific_function START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 'e1':
      alert_message_page = 'Invalid email'
      alert_message_type = 'danger'
    if redirect_var == 'e2':
      alert_message_page = 'Email already exists'
      alert_message_type = 'danger'
    if redirect_var == 'e3':
      alert_message_page = 'Upload was invalid file type (.csv only)'
      alert_message_type = 'danger'
  # ------------------------ redirect codes end ------------------------
  # ------------------------ assessments analytics start ------------------------
  # this has to be ascending
  db_schedule_obj = CandidatesScheduleObj.query.filter_by(user_id_fk=current_user.id, candidates=url_email).order_by(CandidatesScheduleObj.assessment_name, CandidatesScheduleObj.created_timestamp).all()
  if db_schedule_obj == None or db_schedule_obj == []:
    localhost_print_function(' ------------------------ candidates_email_specific_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.login_dashboard_page_function'))
  db_schedule_obj = arr_of_dict_necessary_columns_function(db_schedule_obj, ['assessment_name', 'assessment_id_fk', 'send_date', 'send_time', 'send_timezone', 'expiring_url'])
  previous_test_name = ''
  for i in db_schedule_obj:
    # ------------------------ attempt tracking start ------------------------
    if i['assessment_name'] == previous_test_name:
      current_attempt += 1
    if i['assessment_name'] != previous_test_name:
      previous_test_name = i['assessment_name']
      current_attempt = 1
    i['current_attempt'] = current_attempt
    # ------------------------ attempt tracking end ------------------------
    # ------------------------ email sent start ------------------------
    if i['send_date'] == 'Immediate':
      i['send_date'] = 'Sent'
    else:
      db_email_obj = CandidatesEmailSentObj.query.filter_by(assessment_expiring_url_fk=i['expiring_url']).order_by(CandidatesEmailSentObj.created_timestamp.desc()).first()
      if db_email_obj == None:
        i['send_date'] = f"{i['send_date']} {i['send_time']} {i['send_timezone']}"
      else:
        i['send_date'] = 'Sent'
    # ------------------------ email sent end ------------------------
    # ------------------------ test status grade start ------------------------
    try:
      db_graded_obj = CandidatesAssessmentGradedObj.query.filter_by(assessment_expiring_url_fk=i['expiring_url']).first()
      i['candidate_test_status'] = db_graded_obj.status.capitalize()
      if db_graded_obj.status != 'wip':
        i['final_score'] = str(int(float(db_graded_obj.final_score) * float(100))) + '%'
      else:
        i['candidate_test_status'] = 'Work in progress'
        i['final_score'] = '-'
    except:
      i['candidate_test_status'] = 'Not started'
      i['final_score'] = '-'
    # ------------------------ test status grade end ------------------------
  # ------------------------ assessments analytics end ------------------------
  localhost_print_function(' ------------------------ candidates_email_specific_function END ------------------------ ')
  return render_template('candidates/interior/candidates_page_templates/specific/index.html', user=current_user, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type, db_schedule_obj_to_html=db_schedule_obj, url_email_to_html = url_email)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/tests/', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/tests/dashboard', methods=['GET', 'POST'])
@login_required
def candidates_assessments_dashboard_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_assessments_dashboard_function START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 'r':
      alert_message_page = 'Previous question successfully removed.'
      alert_message_type = 'success'
    if redirect_var == 'a':
      alert_message_page = 'Successfully added question to test.'
      alert_message_type = 'success'
  # ------------------------ valid redirect start ------------------------
  # ------------------------ delete test drafts start ------------------------
  # db.session.commit()
  # ------------------------ delete test drafts end ------------------------
  # ------------------------ get assessments start ------------------------
  # if db_tests_obj == None:
  #   localhost_print_function(' ------------------------ candidates_assessments_dashboard_function END ------------------------ ')
  #   return redirect(url_for('candidates_views_interior.candidates_assessment_create_new_function', step_status='1'))
  # ------------------------ get assessments end ------------------------
  # ------------------------ pull necessary columns start ------------------------
  db_tests_obj = arr_of_dict_necessary_columns_function(db_tests_obj, ['id', 'assessment_name', 'total_questions'])
  # ------------------------ pull necessary columns end ------------------------
  # ------------------------ loop through each test add scheduled details start ------------------------
  for i_dict in db_tests_obj:
    # ------------------------ get schedule start ------------------------
    i_total_pending = 0
    db_schedule_pending_obj = CandidatesScheduleObj.query.filter_by(user_id_fk=current_user.id, assessment_name=i_dict['assessment_name'], candidate_status='Pending').all()
    try:
      i_total_pending = len(db_schedule_pending_obj)
    except:
      pass
    i_total_completed = 0
    db_schedule_completed_obj = CandidatesScheduleObj.query.filter_by(user_id_fk=current_user.id, assessment_name=i_dict['assessment_name'], candidate_status='Completed').all()
    try:
      i_total_completed = len(db_schedule_completed_obj)
    except:
      pass
    # ------------------------ get schedule end ------------------------
    i_dict['total_pending'] = i_total_pending
    i_dict['total_completed'] = i_total_completed
  # ------------------------ loop through each test add scheduled details end ------------------------
  localhost_print_function(' ------------------------ candidates_assessments_dashboard_function END ------------------------ ')
  return render_template('candidates/interior/assessments/assessments_dashboard/index.html', user=current_user, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type, db_tests_obj_to_html=db_tests_obj)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/tests/preview/', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/tests/preview/<url_test_id>', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/tests/preview/<url_test_id>/<url_question_number>', methods=['GET', 'POST'])
@login_required
def candidates_test_preview_function(url_test_id=None, url_question_number='1', url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_test_preview_function START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 'r':
      alert_message_page = 'Previous question successfully removed.'
      alert_message_type = 'success'
  # ------------------------ valid redirect start ------------------------
  # ------------------------ valid test start ------------------------
  db_test_obj = ZDontDeleteTableObj.query.filter_by(user_id_fk=current_user.id, id=url_test_id).first()
  if db_test_obj == None or url_test_id == []:
    return redirect(url_for('candidates_views_interior.candidates_assessments_dashboard_function'))
  # ------------------------ valid test end ------------------------
  # ------------------------ valid number start ------------------------
  try:
    max_num = int(db_test_obj.total_questions)
    if int(url_question_number) < 1 or int(url_question_number) > max_num:
      return redirect(url_for('candidates_views_interior.candidates_test_preview_function', url_test_id=url_test_id, url_question_number='1'))
  except:
    return redirect(url_for('candidates_views_interior.candidates_assessments_dashboard_function'))
  current_question_number = str(int(url_question_number))
  next_question_number = str(int(url_question_number)+1)
  if int(current_question_number) == int(max_num):
    next_question_number = 'submit'
  previous_question_number = str(int(url_question_number)-1)
  # ------------------------ valid number end ------------------------
  # ------------------------ company name start ------------------------
  user_company_name = current_user.company_name
  if len(user_company_name) > 15:
    user_company_name = user_company_name[:14] + '...'
  # ------------------------ company name end ------------------------
  # ------------------------ pull desired test obj start ------------------------
  desired_question_arr = db_test_obj.question_ids_arr.split(',')
  desired_question_str = desired_question_arr[(int(url_question_number)-1)]
  # ------------------------ pull desired test obj end ------------------------
  # ------------------------ pull desired question obj start ------------------------
  db_question_obj = ActivityACreatedQuestionsObj.query.filter_by(id=desired_question_str).first()
  if db_question_obj == None or db_question_obj == []:
    return redirect(url_for('candidates_views_interior.candidates_assessments_dashboard_function'))
  db_question_obj = arr_of_dict_all_columns_single_item_function(db_question_obj)
  db_question_obj['categories'] = categories_tuple_function(db_question_obj['categories'])
  # ------------------------ check if contains img start ------------------------
  contains_img = False
  if 'amazonaws.com' in db_question_obj['aws_image_url']:
    contains_img = True
  # ------------------------ check if contains img end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function(current_user)
  # ------------------------ stripe subscription status check end ------------------------
  if stripe_subscription_obj_status != 'active':
    db_question_obj['answer'] = ''
  # ------------------------ pull desired question obj end ------------------------
  localhost_print_function(' ------------------------ candidates_test_preview_function END ------------------------ ')
  return render_template('candidates/interior/assessments/post_preview/index.html', user=current_user, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type, users_company_name_to_html=user_company_name, current_question_number_to_html=current_question_number, next_question_number_to_html=next_question_number, previous_question_number_to_html=previous_question_number, url_test_id_to_html=url_test_id, db_question_obj_to_html=db_question_obj, contains_img_to_html=contains_img)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/tests/results/', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/tests/results/<url_test_id>', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/tests/results/<url_test_id>/', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/tests/results/<url_test_id>/<url_email>', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/tests/results/<url_test_id>/<url_email>/', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/tests/results/<url_test_id>/<url_email>/<url_current_attempt>', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/tests/results/<url_test_id>/<url_email>/<url_current_attempt>/', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/tests/results/<url_test_id>/<url_email>/<url_current_attempt>/<url_question_number>', methods=['GET', 'POST'])
@login_required
def candidates_test_answered_preview_function(url_test_id=None, url_email=None, url_current_attempt=None, url_question_number='1', url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_test_answered_preview_function START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 'r':
      alert_message_page = 'Previous question successfully removed.'
      alert_message_type = 'success'
  # ------------------------ valid redirect start ------------------------
  # ------------------------ redirect start ------------------------
  if url_test_id == None or url_email == None or url_current_attempt == None or url_question_number == None:
    return redirect(url_for('candidates_views_interior.candidates_assessments_dashboard_function'))
  # ------------------------ redirect end ------------------------
  # ------------------------ valid test start ------------------------
  db_test_obj = ZDontDeleteTableObj.query.filter_by(user_id_fk=current_user.id, id=url_test_id).first()
  if db_test_obj == None or url_test_id == []:
    return redirect(url_for('candidates_views_interior.candidates_assessments_dashboard_function'))
  # ------------------------ valid test end ------------------------
  # ------------------------ valid number start ------------------------
  try:
    max_num = int(db_test_obj.total_questions)
    if int(url_question_number) < 1 or int(url_question_number) > max_num:
      return redirect(url_for('candidates_views_interior.candidates_test_answered_preview_function', url_test_id=url_test_id, url_email=url_email, url_current_attempt=url_current_attempt, url_question_number='1'))
  except:
    return redirect(url_for('candidates_views_interior.candidates_assessments_dashboard_function'))
  current_question_number = str(int(url_question_number))
  next_question_number = str(int(url_question_number)+1)
  if int(current_question_number) == int(max_num):
    next_question_number = 'submit'
  previous_question_number = str(int(url_question_number)-1)
  # ------------------------ valid number end ------------------------
  # ------------------------ company name start ------------------------
  user_company_name = current_user.company_name
  if len(user_company_name) > 15:
    user_company_name = user_company_name[:14] + '...'
  # ------------------------ company name end ------------------------
  # ------------------------ pull desired test obj start ------------------------
  desired_question_arr = db_test_obj.question_ids_arr.split(',')
  desired_question_str = desired_question_arr[(int(url_question_number)-1)]
  # ------------------------ pull desired test obj end ------------------------
  # ------------------------ pull desired question obj start ------------------------
  db_question_obj = ActivityACreatedQuestionsObj.query.filter_by(id=desired_question_str).first()
  if db_question_obj == None or db_question_obj == []:
    return redirect(url_for('candidates_views_interior.candidates_assessments_dashboard_function'))
  db_question_obj = arr_of_dict_all_columns_single_item_function(db_question_obj)
  db_question_obj['categories'] = categories_tuple_function(db_question_obj['categories'])
  # ------------------------ check if contains img start ------------------------
  contains_img = False
  if 'amazonaws.com' in db_question_obj['aws_image_url']:
    contains_img = True
  # ------------------------ check if contains img end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function(current_user)
  # ------------------------ stripe subscription status check end ------------------------
  if stripe_subscription_obj_status != 'active':
    db_question_obj['answer'] = ''
  # ------------------------ pull desired question obj end ------------------------
  # ------------------------ add/get candidate answers start ------------------------
  # this has to be ascending
  db_schedule_obj = CandidatesScheduleObj.query.filter_by(assessment_id_fk=url_test_id, candidates=url_email).order_by(CandidatesScheduleObj.created_timestamp).all()
  db_schedule_obj = arr_of_dict_necessary_columns_function(db_schedule_obj, ['expiring_url'])
  desired_expiring_url = ''
  try:
    desired_expiring_url = db_schedule_obj[(int(url_current_attempt)-1)]['expiring_url']
  except:
    return redirect(url_for('candidates_views_interior.candidates_assessments_dashboard_function'))
  db_graded_obj = CandidatesAssessmentGradedObj.query.filter_by(assessment_expiring_url_fk=desired_expiring_url).first()
  candidate_email = db_graded_obj.candidate_email
  db_graded_arr = json.loads(db_graded_obj.assessment_obj)
  db_user_anser = ''
  try:
    db_user_anser = db_graded_arr[(int(url_question_number)-1)]['user_answer'].upper()
  except:
    return redirect(url_for('candidates_views_interior.candidates_assessments_dashboard_function'))
  # ------------------------ add/get candidate answers end ------------------------
  localhost_print_function(' ------------------------ candidates_test_answered_preview_function END ------------------------ ')
  return render_template('candidates/interior/assessments/post_preview/post_preview_answers/index.html', user=current_user, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type, users_company_name_to_html=user_company_name, current_question_number_to_html=current_question_number, next_question_number_to_html=next_question_number, previous_question_number_to_html=previous_question_number, url_test_id_to_html=url_test_id, db_question_obj_to_html=db_question_obj, contains_img_to_html=contains_img, db_user_anser_to_html=db_user_anser, url_current_attempt_to_html=url_current_attempt, candidate_email_to_html=candidate_email)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/tests/<url_test_id>', methods=['GET', 'POST'])
@login_required
def candidates_test_summary_function(url_test_id=None, url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_test_summary_function START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 'r':
      alert_message_page = 'Previous question successfully removed.'
      alert_message_type = 'success'
    if redirect_var == 'a':
      alert_message_page = 'Successfully added question to test.'
      alert_message_type = 'success'
  # ------------------------ valid redirect start ------------------------
  # ------------------------ assessment start ------------------------
  db_test_obj = ZDontDeleteTableObj.query.filter_by(user_id_fk=current_user.id, id=url_test_id).first()
  if db_test_obj == None or db_test_obj == []:
    localhost_print_function(' ------------------------ candidates_test_summary_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_test_summary_function', url_test_id='dashboard'))
  test_name = db_test_obj.assessment_name
  # ------------------------ assessment end ------------------------
  # ------------------------ schedule start ------------------------
  # this has to be ascending
  db_schedule_obj = CandidatesScheduleObj.query.filter_by(user_id_fk=current_user.id, assessment_id_fk=url_test_id).order_by(CandidatesScheduleObj.candidates, CandidatesScheduleObj.created_timestamp).all()
  db_schedule_obj = arr_of_dict_necessary_columns_function(db_schedule_obj, ['candidates', 'send_date', 'send_time', 'send_timezone', 'candidate_status', 'expiring_url'])
  previous_email = ''
  current_attempt = 0
  for i in db_schedule_obj:
    # ------------------------ attempt tracking start ------------------------
    current_email = i['candidates']
    if current_email == previous_email:
      current_attempt += 1
    if current_email != previous_email:
      previous_email = current_email
      current_attempt = 1
    i['current_attempt'] = current_attempt
    # ------------------------ attempt tracking end ------------------------
    if i['send_date'] == 'Immediate':
      i['send_date'] = 'Sent'
    else:
      # ------------------------ email sent start ------------------------
      db_email_obj = CandidatesEmailSentObj.query.filter_by(assessment_expiring_url_fk=i['expiring_url']).order_by(CandidatesEmailSentObj.created_timestamp.desc()).first()
      if db_email_obj == None:
        i['send_date'] = f"{i['send_date']} {i['send_time']} {i['send_timezone']}"
      else:
        i['send_date'] = 'Sent'
      # ------------------------ email sent end ------------------------
    # ------------------------ graded start ------------------------
    try:
      db_graded_obj = CandidatesAssessmentGradedObj.query.filter_by(assessment_expiring_url_fk=i['expiring_url']).first()
      i['candidate_test_status'] = db_graded_obj.status.capitalize()
      if db_graded_obj.status != 'wip':
        i['final_score'] = str(int(float(db_graded_obj.final_score) * float(100))) + '%'
      else:
        i['candidate_test_status'] = 'Work in progress'
        i['final_score'] = '-'  
    except:
      i['candidate_test_status'] = 'Not started'
      i['final_score'] = '-'
    # ------------------------ graded end ------------------------
  # ------------------------ schedule end ------------------------
  # ------------------------ loop through each test add scheduled details end ------------------------
  localhost_print_function(' ------------------------ candidates_test_summary_function END ------------------------ ')
  return render_template('candidates/interior/assessments/assessments_dashboard/specific/index.html', user=current_user, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type, db_schedule_obj_to_html=db_schedule_obj, test_name_to_html=test_name, url_test_id_to_html=url_test_id)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/assessment/new/<step_status>', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/assessment/new/<step_status>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def candidates_assessment_create_new_function(step_status, url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_assessment_create_new_function START ------------------------ ')
  template_location_url = 'candidates/interior/assessments/assessments_create_new/index.html'
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ delete test drafts start ------------------------
  if step_status == '1b':
    ZDontDeleteTableObj.query.filter_by(user_id_fk=current_user.id,status='draft').delete()
    db.session.commit()
  # ------------------------ delete test drafts end ------------------------
  # ------------------------ pull all categories associated with candidates start ------------------------
  query_result_arr_of_dicts = select_general_function('select_all_candidate_categories_chosen_v2')
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
  create_assessment_error_statement = ''
  # ------------------------ post method hit start ------------------------
  if request.method == 'POST':
    # ------------------------ get form user inputs start ------------------------
    ui_desired_languages_checkboxes_arr = request.form.getlist('testLabelAdded')
    # ------------------------ get form user inputs end ------------------------
    # ------------------------ redirect start ------------------------
    if ui_desired_languages_checkboxes_arr == None or ui_desired_languages_checkboxes_arr == []:
      return redirect(url_for('candidates_views_interior.candidates_assessment_create_new_function', step_status='1', url_redirect_code='e12'))
    # ------------------------ redirect end ------------------------
    # ------------------------ sanitize/check user inputs start ------------------------
    # ------------------------ sanitize/check desired languages start ------------------------
    ui_desired_languages_checkboxes_arr = sanitize_loop_check_if_exists_within_arr_function(ui_desired_languages_checkboxes_arr, candidate_categories_arr)
    if ui_desired_languages_checkboxes_arr == [] or ui_desired_languages_checkboxes_arr == False:
      ui_desired_languages_checkboxes_arr = False
      create_assessment_error_statement = 'Please fill out all required fields.'
    ui_desired_languages_checkboxes_str = ''
    if ui_desired_languages_checkboxes_arr != False:
      ui_desired_languages_checkboxes_str = ','.join(ui_desired_languages_checkboxes_arr)
    if len(ui_desired_languages_checkboxes_str) > 1000:
      create_assessment_error_statement = 'Please select fewer categories.'
      ui_desired_languages_checkboxes_arr == False
    # ------------------------ sanitize/check desired languages end ------------------------
    # ------------------------ create name based on langs start ------------------------
    auto_generated_assessment_name = ''
    if ui_desired_languages_checkboxes_arr != False:
      auto_generated_assessment_name = create_assessment_name_function(ui_desired_languages_checkboxes_str)
    # ------------------------ create name based on langs end ------------------------
    # ------------------------ check if assessment name already exists for user start ------------------------
    user_assessment_name_already_exists = ZDontDeleteTableObj.query.filter_by(assessment_name=auto_generated_assessment_name,user_id_fk=current_user.id).first()
    if user_assessment_name_already_exists != None:
      auto_generated_assessment_name = False
      create_assessment_error_statement = f'Assessment name "{auto_generated_assessment_name}" already exists.'
    # ------------------------ check if assessment name already exists for user end ------------------------
    # ------------------------ sanitize/check user inputs end ------------------------
    # ------------------------ pull random assessment questions start ------------------------
    # ------------------------ prepare where statement start ------------------------
    where_clause_arr = prepare_where_clause_function(ui_desired_languages_checkboxes_str)
    # ------------------------ prepare where statement end ------------------------
    # ------------------------ pull question obj from db start ------------------------
    query_result_arr_of_dicts = select_general_function('select_all_questions_for_x_categories_v3', where_clause_arr[0])
    auto_generated_question_ids_arr = []
    for i_dict in query_result_arr_of_dicts:
      i_id = i_dict['id']
      auto_generated_question_ids_arr.append(i_id)
    # ------------------------ pull question obj from db end ------------------------
    auto_generated_question_ids_str = ','.join(auto_generated_question_ids_arr)
    # ------------------------ pull random assessment questions end ------------------------
    # ------------------------ create new assessment in db start ------------------------
    if auto_generated_assessment_name != False and ui_desired_languages_checkboxes_arr != False and ui_desired_languages_checkboxes_arr != []:
      new_row = ZDontDeleteTableObj(
        id=create_uuid_function('assessment_'),
        created_timestamp=create_timestamp_function(),
        user_id_fk=current_user.id,
        assessment_name=auto_generated_assessment_name,
        desired_languages_arr = ui_desired_languages_checkboxes_str,
        total_questions = len(auto_generated_question_ids_arr),
        question_ids_arr=auto_generated_question_ids_str,
        status='draft'
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ create new assessment in db end ------------------------
      localhost_print_function(' ------------------------ candidates_assessment_create_new_function END ------------------------ ')
      return redirect(url_for('candidates_views_interior.candidates_assessment_create_review_function', url_assessment_name=auto_generated_assessment_name))
  # ------------------------ post method hit end ------------------------
  """
  # ------------------------ normal page load start ------------------------
  localhost_print_function(' ------------------------ candidates_assessment_create_new_function END ------------------------ ')
  return render_template('candidates/interior/assessments/assessments_create_new/index.html', user=current_user, users_company_name_to_html = current_user.company_name, error_message_to_html=create_assessment_error_statement, candidate_categories_arr_1_to_html=candidate_categories_arr_1, candidate_categories_arr_2_to_html=candidate_categories_arr_2, candidate_categories_arr_3_to_html=candidate_categories_arr_3, trial_name_attempt_to_html=trial_name_attempt)
  # ------------------------ normal page load end ------------------------
  """
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, users_company_name_to_html=current_user.company_name, error_message_to_html=create_assessment_error_statement, candidate_categories_arr_to_html=candidate_categories_arr, page_dict_to_html=page_dict)
  else:
    browser_response = browser_response_set_cookie_function_v2(template_location_url, current_user, current_user.company_name, create_assessment_error_statement, candidate_categories_arr, page_dict)
    localhost_print_function(' ------------------------ candidates_assessment_create_new_function END ------------------------ ')
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/assessment/review/<url_assessment_name>', methods=['GET', 'POST'])
@login_required
def candidates_assessment_create_review_function(url_assessment_name):
  localhost_print_function(' ------------------------ candidates_assessment_create_review_function START ------------------------ ')
  review_assessment_error_statement = ''
  # ------------------------ pull assessment obj start ------------------------
  db_assessment_obj = ZDontDeleteTableObj.query.filter_by(assessment_name=url_assessment_name,user_id_fk=current_user.id).first()
  if db_assessment_obj == None or db_assessment_obj == []:
    return redirect(url_for('candidates_views_interior.login_dashboard_page_function'))
  assessment_name = db_assessment_obj.assessment_name
  assessment_total_questions = db_assessment_obj.total_questions
  # ------------------------ pull assessment obj end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function(current_user)
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ post submit start ------------------------
  if request.method == 'POST':
    # ------------------------ get user inputs start ------------------------
    ui_name = request.form.get('uiName')
    # ------------------------ get user inputs end ------------------------
    # ------------------------ sanitize user inputs start ------------------------
    if ui_name != db_assessment_obj.assessment_name:
      ui_name = sanitize_letters_numbers_spaces_only_function(ui_name)
      if ui_name == False:
        review_assessment_error_statement = 'Test name should be 1-100 characters in length and contain only: letters/numbers/spaces.'
      if ui_name != False:
        ui_name = ui_name.strip()
        db_assessment_obj.assessment_name = ui_name
    # ------------------------ sanitize user inputs end ------------------------
    if review_assessment_error_statement == '':
      db_assessment_obj.status = 'final'
      db.session.commit()
      # ------------------------ email self start ------------------------
      try:
        output_to_email = os.environ.get('TRIVIAFY_SUPPORT_EMAIL')
        output_subject = f'Triviafy - Test Created - {current_user.email}'
        output_body = f"Hi there,\n\nNew test created: {current_user.email} \n\nBest,\nTriviafy"
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self end ------------------------
      return redirect(url_for('candidates_views_interior.candidates_schedule_dashboard_function'))
  # ------------------------ post submit end ------------------------
  localhost_print_function(' ------------------------ candidates_assessment_create_review_function END ------------------------ ')
  return render_template('candidates/interior/assessments/assessments_create_review/index.html', user=current_user, users_company_name_to_html=current_user.company_name, error_message_to_html=review_assessment_error_statement, assessment_name_to_html=assessment_name, stripe_subscription_obj_status_to_html=stripe_subscription_obj_status, assessment_total_questions_to_html=assessment_total_questions)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/assessment/preview/<url_assessment_name>/', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/assessment/preview/<url_assessment_name>/<url_question_number>', methods=['GET', 'POST'])
@login_required
def candidates_assessment_preview_function(url_assessment_name, url_question_number='1', url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_assessment_preview_function START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 'r':
      alert_message_page = 'Previous question successfully removed.'
      alert_message_type = 'success'
    if redirect_var == 'a':
      alert_message_page = 'Successfully added question to test.'
      alert_message_type = 'success'
  # ------------------------ valid redirect start ------------------------
  valid_url_question_number = False
  try:
    valid_url_question_number = int(url_question_number)
  except:
    pass
  if valid_url_question_number == False:
    localhost_print_function(' ------------------------ candidates_assessment_preview_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_assessment_preview_function',url_assessment_name=url_assessment_name, url_question_number='1'))
  # ------------------------ valid redirect end ------------------------
  # ------------------------ redirect codes end ------------------------
  next_question_number = int(url_question_number) + 1
  previous_question_number = int(url_question_number) - 1
  # ------------------------ variables start ------------------------
  user_company_name = current_user.company_name
  if len(user_company_name) > 15:
    user_company_name = user_company_name[:14] + '...'
  # ------------------------ variables end ------------------------
  # ------------------------ pull assessment obj start ------------------------
  db_assessment_obj = ZDontDeleteTableObj.query.filter_by(assessment_name=url_assessment_name,user_id_fk=current_user.id).first()
  if db_assessment_obj == None:
    localhost_print_function(' ------------------------ candidates_assessment_preview_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_assessment_invalid_function'))
  assessment_total_questions = db_assessment_obj.total_questions
  if str(url_question_number) == str(assessment_total_questions):
    next_question_number = 'submit'
  # ------------------------ pull assessment obj end ------------------------
  # ------------------------ redirect to latest if url number is not found start ------------------------
  if int(url_question_number) > int(assessment_total_questions):
    return redirect(url_for('candidates_views_interior.candidates_assessment_preview_function',url_assessment_name=url_assessment_name, url_question_number=assessment_total_questions))
  # ------------------------ redirect to latest if url number is not found end ------------------------
  # ------------------------ assign assessment info to dict start ------------------------
  try:
    assessment_info_dict = create_assessment_info_dict_function_v2(db_assessment_obj, url_question_number)
  except:
    # ------------------------ once all questions answered start ------------------------
    # This code needs to be replaced down the line once you get the individual answer captured for questions 1-n.
    url_question_number = assessment_total_questions
    assessment_info_dict = create_assessment_info_dict_function_v2(db_assessment_obj, url_question_number)
    next_question_number = 'submit'
    # ------------------------ once all questions answered end ------------------------
  # ------------------------ assign assessment info to dict end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function(current_user)
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ if subscription not paid start ------------------------
  if stripe_subscription_obj_status != 'active':
    assessment_info_dict['question_details_dict']['answer'] = ''
  # ------------------------ if subscription not paid end ------------------------
  # ------------------------ check if contains img start ------------------------
  contains_img = False
  if 'amazonaws.com' in assessment_info_dict['question_details_dict']['aws_image_url']:
    contains_img = True
  # ------------------------ check if contains img end ------------------------
  # ------------------------ option e fix start ------------------------
  current_option_e = assessment_info_dict['question_details_dict']['option_e']
  if current_option_e == None or len(current_option_e) == 0:
    assessment_info_dict['question_details_dict']['option_e'] = None
  # ------------------------ option e fix end ------------------------
  # ------------------------ post hit admin control start ------------------------
  if request.method == 'POST':
    # ------------------------ get user inputs start ------------------------
    ui_desired_actions_checkboxes_arr = request.form.getlist('uiAdminEditSelection')
    # ------------------------ remove question id start ------------------------
    if 'remove' in ui_desired_actions_checkboxes_arr:
      if assessment_info_dict['total_questions'] == 1:
        alert_message_page = 'Test must contain at least 1 question.'
        alert_message_type = 'danger'
      if assessment_info_dict['total_questions'] != 1:
        current_question_id = assessment_info_dict['question_details_dict']['id']
        all_current_question_ids_from_obj_str = db_assessment_obj.question_ids_arr
        # remove the question id from str
        all_current_question_ids_from_obj_str = all_current_question_ids_from_obj_str.replace(current_question_id, '')
        # remove any leading, in between double, and trailing commas
        if all_current_question_ids_from_obj_str[0] == ',':
          all_current_question_ids_from_obj_str = all_current_question_ids_from_obj_str[1:]
        if all_current_question_ids_from_obj_str[-1] == ',':
          all_current_question_ids_from_obj_str = all_current_question_ids_from_obj_str[:-1]
        all_current_question_ids_from_obj_str = all_current_question_ids_from_obj_str.replace(',,', ',')
        # update total questions
        current_question_count = int(assessment_info_dict['total_questions'])
        corrected_current_question_count = str(current_question_count - 1)
        # commit changes
        db_assessment_obj.question_ids_arr = all_current_question_ids_from_obj_str
        db_assessment_obj.total_questions = corrected_current_question_count
        db.session.commit()
        # redirect back to same page post changes
        if url_question_number == '1':
          pass
        else:
          url_question_number = str(int(url_question_number) - 1)
        return redirect(url_for('candidates_views_interior.candidates_assessment_preview_function',url_assessment_name=url_assessment_name, url_question_number=url_question_number, url_redirect_code='r'))
    # ------------------------ remove question id end ------------------------
    # ------------------------ add new question id start ------------------------
    if 'add' in ui_desired_actions_checkboxes_arr:
      if assessment_info_dict['total_questions'] == 50:
        alert_message_page = 'Test cannot be more than 50 questions.'
        alert_message_type = 'danger'
      if assessment_info_dict['total_questions'] != 50:
        desired_languages_str = db_assessment_obj.desired_languages_arr
        # ------------------------ prepare where statement start ------------------------
        current_question_ids_str = prepare_question_ids_where_clause_function(db_assessment_obj)
        where_clause_arr = prepare_where_clause_function(desired_languages_str)
        # ------------------------ prepare where statement end ------------------------
        # ------------------------ sql query start ------------------------
        query_result_arr_of_dicts = select_general_function('select_one_question_for_x_categories_v1', where_clause_arr[0], current_question_ids_str)
        try:
          add_question_id = query_result_arr_of_dicts[0]['id']
        except:
          add_question_id = None
        # ------------------------ sql query end ------------------------
        # ------------------------ action based on sql query result start ------------------------
        if add_question_id == None:
          alert_message_page = 'All available questions for this category are already selected. Triviafy team will be making more questions for this category, thank you.'
          alert_message_type = 'danger'
          # ------------------------ add row to requested categories start ------------------------
          current_user_desired_langs_arr = CandidatesDesiredLanguagesObj.query.filter_by(user_id_fk=current_user.id).all()
          # ------------------------ check if already requested start ------------------------
          already_requested_flag = False
          for i_obj in current_user_desired_langs_arr:
            if i_obj.desired_languages == desired_languages_str:
              already_requested_flag = True
          # ------------------------ check if already requested end ------------------------
          if already_requested_flag == False:
            # ------------------------ new row db start ------------------------
            new_row = CandidatesDesiredLanguagesObj(
              id=create_uuid_function('langs_'),
              created_timestamp=create_timestamp_function(),
              user_id_fk=current_user.id,
              desired_languages=desired_languages_str
            )
            db.session.add(new_row)
            db.session.commit()
            # ------------------------ new row db end ------------------------
          # ------------------------ add row to requested categories end ------------------------
        else:
          # str of question ids
          new_question_ids_str = db_assessment_obj.question_ids_arr + f',{add_question_id}'
          # total questions
          new_total_question_count = str(int(db_assessment_obj.total_questions) + 1)
          # update db
          db_assessment_obj.question_ids_arr = new_question_ids_str
          db_assessment_obj.total_questions = new_total_question_count
          db.session.commit()
          # redirect back to same page post changes
          return redirect(url_for('candidates_views_interior.candidates_assessment_preview_function',url_assessment_name=url_assessment_name, url_question_number=new_total_question_count, url_redirect_code='a'))
        # ------------------------ action based on sql query result end ------------------------
    # ------------------------ add new question id end ------------------------
    # ------------------------ get user inputs end ------------------------
  # ------------------------ post hit admin control end ------------------------
  localhost_print_function(' ------------------------ candidates_assessment_preview_function END ------------------------ ')
  return render_template('candidates/interior/assessments/assessments_preview/index.html', user=current_user, users_company_name_to_html=user_company_name, alert_message_page_to_html=alert_message_page, alert_message_type_to_html = alert_message_type, stripe_subscription_obj_status_to_html=stripe_subscription_obj_status, current_question_number_to_html=url_question_number, next_question_number_to_html=next_question_number, previous_question_number_to_html=previous_question_number, url_assessment_name_to_html=url_assessment_name, assessment_info_dict_to_html=assessment_info_dict, contains_img_to_html=contains_img, assessment_total_questions_to_html=assessment_total_questions)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/schedule', methods=['GET', 'POST'])
@login_required
def candidates_schedule_dashboard_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_schedule_dashboard_function START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 's':
      alert_message_page = 'Candidate successfully added.'
      alert_message_type = 'success'
    if redirect_var == 'e':
      alert_message_page = 'Invalid selection.'
      alert_message_type = 'danger'
  # ------------------------ redirect codes end ------------------------
  # ------------------------ total assessments made start ------------------------  
  total_test_made = 0
  test_obj = ZDontDeleteTableObj.query.filter_by(user_id_fk=current_user.id, status='final').order_by(ZDontDeleteTableObj.created_timestamp).all()
  if test_obj == [] or test_obj == None:
    total_test_made = 0
  else:
    for i in test_obj:
      total_test_made += 1
  # ------------------------ total assessments made end ------------------------
  # ------------------------ schedule analytics start ------------------------
  db_schedule_obj = CandidatesScheduleObj.query.filter_by(user_id_fk=current_user.id).order_by(CandidatesScheduleObj.created_timestamp.desc()).all()
  db_schedule_obj_exists = False
  if db_schedule_obj == None:
    pass
  else:
    db_schedule_obj_exists = True
    db_schedule_obj = arr_of_dict_necessary_columns_function(db_schedule_obj, ['assessment_name', 'created_timestamp', 'candidates', 'send_date', 'send_time', 'send_timezone', 'candidate_status', 'expiring_url'])
    for i in db_schedule_obj:
      if i['send_date'] != 'Immediate':
        i['send_date'] = f"{i['send_date']} {i['send_time']} {i['send_timezone']}"
      i['created_timestamp'] = i['created_timestamp'].strftime('%Y-%m-%d %H:%M')
  # ------------------------ schedule analytics end ------------------------
  if request.method == 'POST':
    # ------------------------ user input start ------------------------
    ui_choice = request.form.get('listGroupRadios')
    allowed_arr = ['immediate', 'scheduled']
    if ui_choice not in allowed_arr:
      return redirect(url_for('candidates_views_interior.candidates_schedule_dashboard_function', url_redirect_code='e'))
    else:
      if ui_choice == 'immediate':
        localhost_print_function(' ------------------------ candidates_schedule_dashboard_function END ------------------------ ')
        return redirect(url_for('candidates_views_interior.candidates_schedule_create_now_function_v2'))
      if ui_choice == 'scheduled':
        localhost_print_function(' ------------------------ candidates_schedule_dashboard_function END ------------------------ ')
        return redirect(url_for('candidates_views_interior.candidates_schedule_create_new_function'))
    # ------------------------ user input end ------------------------
  localhost_print_function(' ------------------------ candidates_schedule_dashboard_function END ------------------------ ')
  return render_template('candidates/interior/schedule/schedule_dashboard/index.html', user=current_user, total_test_made_to_html=total_test_made, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type, db_schedule_obj_exists_to_html=db_schedule_obj_exists, db_schedule_obj_to_html=db_schedule_obj)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/schedule/new', methods=['GET', 'POST'])
@login_required
def candidates_schedule_create_new_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_schedule_create_new_function START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 'e':
      alert_message_page = 'Please fill out all fields.'
      alert_message_type = 'danger'
    if redirect_var == 'e2':
      alert_message_page = 'Invalid test name.'
      alert_message_type = 'danger'
    if redirect_var == 's':
      alert_message_page = 'Test scheduled successfully.'
      alert_message_type = 'success'
  # ------------------------ redirect codes end ------------------------
  # ------------------------ pull all available dates, times, timezones start ------------------------
  next_x_days_arr = next_x_days_function()
  times_arr, timezone_arr = times_arr_function()
  # ------------------------ pull all available dates, times, timezones end ------------------------
  # ------------------------ pull tests arr of dict start ------------------------
  db_tests_obj = ZDontDeleteTableObj.query.filter_by(user_id_fk=current_user.id).order_by(ZDontDeleteTableObj.assessment_name).all()
  all_test_names_arr = []
  for i in db_tests_obj:
    all_test_names_arr.append(i.assessment_name)
  db_tests_obj = arr_of_dict_necessary_columns_function(db_tests_obj, ['assessment_name', 'desired_languages_arr', 'total_questions'])
  if len(db_tests_obj[0]['desired_languages_arr']) > 15:
    categories_short = db_tests_obj[0]['desired_languages_arr'][0:19]
    db_tests_obj[0]['desired_languages_arr'] = categories_short
  # ------------------------ pull tests arr of dict end ------------------------
  # ------------------------ pull candidates arr of dict start ------------------------
  db_candidates_obj = CandidatesUploadedCandidatesObj.query.filter_by(user_id_fk=current_user.id).order_by(CandidatesUploadedCandidatesObj.email).all()
  all_candidate_emails_arr = []
  all_candidate_emails_arr.append(current_user.email)
  for i in db_candidates_obj:
    all_candidate_emails_arr.append(i.email)
  db_candidates_obj = arr_of_dict_necessary_columns_function(db_candidates_obj, ['email'])
  # ------------------------ pull candidates arr of dict end ------------------------
  # ------------------------ self email start ------------------------
  current_user_email = current_user.email
  # ------------------------ self email end ------------------------
  if request.method == 'POST':
    # ------------------------ get user inputs start ------------------------
    ui_test_selected = request.form.get('uiTestSelected')                  # str
    ui_candidates_selected = request.form.getlist('uiCandidateSelected')   # list of str
    ui_date_selected = request.form.get('uiDateSelected')
    ui_time_selected = request.form.get('uiTimeSelected')
    ui_timezone_selected = request.form.get('uiTimeZoneSelected')
    # ------------------------ get user inputs end ------------------------
    # ------------------------ validate ui start ------------------------
    ui_test_selected_check = sanitize_check_if_str_exists_within_arr_function(ui_test_selected, all_test_names_arr)
    ui_candidates_selected_check = sanitize_loop_check_if_exists_within_arr_function(ui_candidates_selected, all_candidate_emails_arr)
    ui_date_selected_check = sanitize_check_if_str_exists_within_arr_function(ui_date_selected, next_x_days_arr)
    ui_time_selected_check = sanitize_check_if_str_exists_within_arr_function(ui_time_selected, times_arr)
    ui_timezone_selected_check = sanitize_check_if_str_exists_within_arr_function(ui_timezone_selected, timezone_arr)
    if ui_test_selected_check == False or ui_candidates_selected_check == False or ui_date_selected_check == False or ui_time_selected_check == False or ui_timezone_selected_check == False:
      localhost_print_function(' ------------------------ candidates_schedule_create_new_function END ------------------------ ')
      return redirect(url_for('candidates_views_interior.candidates_schedule_create_new_function', url_redirect_code='e'))
    # ------------------------ validate ui end ------------------------
    else:
      # ------------------------ get assessment id based on name and user id fk start ------------------------
      db_assessment_obj = ZDontDeleteTableObj.query.filter_by(user_id_fk=current_user.id, assessment_name=ui_test_selected).first()
      if db_assessment_obj == None:
        localhost_print_function(' ------------------------ candidates_schedule_create_new_function END ------------------------ ')
        return redirect(url_for('candidates_views_interior.candidates_schedule_create_new_function', url_redirect_code='e2'))
      # ------------------------ get assessment id based on name and user id fk end ------------------------
      for i in ui_candidates_selected:
        new_row = CandidatesScheduleObj(
          id = create_uuid_function('schedule_'),
          created_timestamp = create_timestamp_function(),
          user_id_fk = current_user.id,
          assessment_id_fk = db_assessment_obj.id,
          assessment_name = ui_test_selected,
          candidates = i,
          send_date = ui_date_selected,
          send_time = ui_time_selected,
          send_timezone = ui_timezone_selected,
          candidate_status = 'Pending',
          expiring_url = create_uuid_function('expire_')
        )
        db.session.add(new_row)
        db.session.commit()
      # ------------------------ email self start ------------------------
      try:
        output_to_email = os.environ.get('TRIVIAFY_SUPPORT_EMAIL')
        output_subject = f'Triviafy - Future Schedule Created - {current_user.email}'
        output_body = f"Hi there,\n\n{current_user.email} created schedule.\n\nBest,\nTriviafy"
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self end ------------------------
      localhost_print_function(' ------------------------ candidates_schedule_create_new_function END ------------------------ ')
      return redirect(url_for('candidates_views_interior.candidates_schedule_create_new_function', url_redirect_code='s'))
      # ------------------------ insert to db end ------------------------
  # ------------------------ post triggered end ------------------------
  localhost_print_function(' ------------------------ candidates_schedule_create_new_function END ------------------------ ')
  return render_template('candidates/interior/schedule/schedule_create_new/index.html', user=current_user, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type, db_tests_obj_to_html=db_tests_obj, db_candidates_obj_to_html=db_candidates_obj, current_user_email_to_html=current_user_email, next_x_days_arr_to_html=next_x_days_arr, times_arr_to_html=times_arr, timezone_arr_to_html=timezone_arr)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/schedule/now', methods=['GET', 'POST'])
@login_required
def candidates_schedule_create_now_function_v2(url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_schedule_create_now_function_v2 START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 's':
      alert_message_page = 'Emailed test sent successfully.'
      alert_message_type = 'success'
    if redirect_var == 'e':
      alert_message_page = 'Please select at least 1 test and 1 candidate.'
      alert_message_type = 'danger'
  # ------------------------ redirect codes end ------------------------
  current_user_email = current_user.email
  # ------------------------ pull tests arr of dict start ------------------------
  db_tests_obj = ZDontDeleteTableObj.query.filter_by(user_id_fk=current_user.id).order_by(ZDontDeleteTableObj.assessment_name).all()
  all_test_names_arr = []
  for i in db_tests_obj:
    all_test_names_arr.append(i.assessment_name)
  db_tests_obj = arr_of_dict_necessary_columns_function(db_tests_obj, ['assessment_name', 'desired_languages_arr', 'total_questions'])
  if len(db_tests_obj[0]['desired_languages_arr']) > 15:
    categories_short = db_tests_obj[0]['desired_languages_arr'][0:19]
    db_tests_obj[0]['desired_languages_arr'] = categories_short
  # ------------------------ pull tests arr of dict end ------------------------
  # ------------------------ pull candidates arr of dict start ------------------------
  db_candidates_obj = CandidatesUploadedCandidatesObj.query.filter_by(user_id_fk=current_user.id).order_by(CandidatesUploadedCandidatesObj.email).all()
  all_candidate_emails_arr = []
  all_candidate_emails_arr.append(current_user.email)
  for i in db_candidates_obj:
    all_candidate_emails_arr.append(i.email)
  db_candidates_obj = arr_of_dict_necessary_columns_function(db_candidates_obj, ['email'])
  # ------------------------ pull candidates arr of dict end ------------------------
  if request.method == 'POST':
    # ------------------------ get user inputs start ------------------------
    ui_test_selected = request.form.get('uiTestSelected')                  # str
    ui_candidates_selected = request.form.getlist('uiCandidateSelected')   # list of str
    # ------------------------ get user inputs end ------------------------
    # ------------------------ validate ui start ------------------------
    ui_test_selected_check = sanitize_check_if_str_exists_within_arr_function(ui_test_selected, all_test_names_arr)
    ui_candidates_selected_check = sanitize_loop_check_if_exists_within_arr_function(ui_candidates_selected, all_candidate_emails_arr)
    # ------------------------ validate ui end ------------------------
    if ui_test_selected_check != False and ui_candidates_selected_check != False:
      # ------------------------ get assessment id based on name and user id fk start ------------------------
      db_test_obj = ZDontDeleteTableObj.query.filter_by(user_id_fk=current_user.id, assessment_name=ui_test_selected).first()
      db_test_obj_assessment_id = db_test_obj.id
      # ------------------------ get assessment id based on name and user id fk end ------------------------
      # ------------------------ for each email selected start ------------------------
      for i_email in ui_candidates_selected:
        expiring_url_i_created = create_uuid_function('expire_')
        new_row = CandidatesScheduleObj(
          id = create_uuid_function('schedule_'),
          created_timestamp = create_timestamp_function(),
          user_id_fk = current_user.id,
          assessment_id_fk = db_test_obj_assessment_id,
          assessment_name = ui_test_selected,
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
        output_subject = f'Triviafy Test: {ui_test_selected}'
        output_body = f"Hi there,\n\nYour Triviafy test is ready! The following link will expire 1 hour from the time you receive this email.\nPlease visit the following link to complete your test: https://triviafy.com/candidates/assessment/{expiring_url_i_created}/1 \n\nBest,\nTriviafy"
        # output_body = f"Hi there,\n\nYour Triviafy test is ready! The following link will expire 1 hour from the time you receive this email.\nPlease visit the following link to complete your test: http://127.0.0.1/candidates/assessment/{expiring_url_i_created}/1 \n\nBest,\nTriviafy"
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
      # ------------------------ for each email selected end ------------------------
      # ------------------------ email self start ------------------------
      try:
        output_to_email = os.environ.get('TRIVIAFY_SUPPORT_EMAIL')
        output_subject = f'Triviafy - Immediate Schedule Created - {current_user.email}'
        output_body = f"Hi there,\n\n{current_user.email} created schedule.\n\nBest,\nTriviafy"
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self end ------------------------
      return redirect(url_for('candidates_views_interior.candidates_schedule_create_now_function_v2', url_redirect_code='s'))
    else:
      return redirect(url_for('candidates_views_interior.candidates_schedule_create_now_function_v2', url_redirect_code='e'))
  localhost_print_function(' ------------------------ candidates_schedule_create_now_function_v2 END ------------------------ ')
  return render_template('candidates/interior/schedule/schedule_create_now/index.html', user=current_user, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type, current_user_email_to_html=current_user_email, db_tests_obj_to_html=db_tests_obj, db_candidates_obj_to_html=db_candidates_obj)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/assessment/invalid')
def candidates_assessment_invalid_function():
  localhost_print_function(' ------------------------ candidates_assessment_invalid_function START ------------------------ ')
  localhost_print_function(' ------------------------ candidates_assessment_invalid_function END ------------------------ ')
  return render_template('candidates/exterior/assessments/assessment_not_found/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/assessment/early')
def candidates_assessment_early_function():
  localhost_print_function(' ------------------------ candidates_assessment_early_function START ------------------------ ')
  localhost_print_function(' ------------------------ candidates_assessment_early_function END ------------------------ ')
  return render_template('candidates/exterior/assessments/assessment_early/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/assessment/completed/success')
def candidates_assessment_completed_success_function():
  localhost_print_function(' ------------------------ candidates_assessment_completed_success_function START ------------------------ ')
  localhost_print_function(' ------------------------ candidates_assessment_completed_success_function END ------------------------ ')
  return render_template('candidates/exterior/assessments/assessment_completed_success/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/assessment/closed')
def candidates_assessment_closed_function():
  localhost_print_function(' ------------------------ candidates_assessment_closed_function START ------------------------ ')
  localhost_print_function(' ------------------------ candidates_assessment_closed_function END ------------------------ ')
  return render_template('candidates/exterior/assessments/assessment_closed/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/assessment/<url_assessment_expiring>/', methods=['GET', 'POST'])
@candidates_views_interior.route('/candidates/assessment/<url_assessment_expiring>/<url_question_number>', methods=['GET', 'POST'])
def candidates_assessment_expiring_function(url_assessment_expiring, url_question_number='1', url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_assessment_expiring_function START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 'e1':
      alert_message_page = 'Invalid answer choice'
      alert_message_type = 'danger'
  # ------------------------ redirect codes end ------------------------
  # ------------------------ submit after submit start ------------------------
  if url_question_number == 'submit':
    db_grading_in_progress_obj = CandidatesAssessmentGradedObj.query.filter_by(assessment_expiring_url_fk=url_assessment_expiring, status='wip').first()
    if db_grading_in_progress_obj == None:
      localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
      return redirect(url_for('candidates_views_interior.candidates_assessment_closed_function'))
    else:
      if int(db_grading_in_progress_obj.graded_count) == int(db_grading_in_progress_obj.total_questions):
        db_grading_in_progress_obj.status = 'submitted'
        db_schedule_obj = CandidatesScheduleObj.query.filter_by(expiring_url=url_assessment_expiring).first()
        db_schedule_obj.candidate_status = 'Completed'
        db.session.commit()
        # ------------------------ email self start ------------------------
        try:
          output_to_email = os.environ.get('TRIVIAFY_SUPPORT_EMAIL')
          output_subject = f'Triviafy - Graded Assessment - {db_grading_in_progress_obj.assessment_name}'
          output_body = f"Hi there,\n\nCandidate submitted assessment answers for {db_grading_in_progress_obj.assessment_name} \n\nBest,\nTriviafy"
          send_email_template_function(output_to_email, output_subject, output_body)
        except:
          pass
        # ------------------------ email self end ------------------------
        localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
        return redirect(url_for('candidates_views_interior.candidates_assessment_completed_success_function'))
  # ------------------------ submit after submit end ------------------------
  # ------------------------ confirm int start ------------------------
  is_int = False
  try:
    is_int = isinstance(int(url_question_number), int)
  except:
    pass
  if is_int == False:
    localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_assessment_expiring_function', url_assessment_expiring=url_assessment_expiring, url_question_number='1'))
  # ------------------------ confirm int end ------------------------
  # ------------------------ invalid url_assessment_name start ------------------------
  if url_assessment_expiring == False or url_assessment_expiring == None or url_assessment_expiring == '':
    localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_assessment_invalid_function'))
  # ------------------------ invalid url_assessment_name end ------------------------
  # ------------------------ check if answers already submitted start ------------------------
  db_already_graded_obj = CandidatesAssessmentGradedObj.query.filter_by(assessment_expiring_url_fk=url_assessment_expiring, status='submitted').first()
  if db_already_graded_obj != None:
    localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_assessment_closed_function'))
  # ------------------------ check if answers already submitted end ------------------------
  # ------------------------ check if question number already submitted start ------------------------
  db_grading_in_progress_obj = CandidatesAssessmentGradedObj.query.filter_by(assessment_expiring_url_fk=url_assessment_expiring, status='wip').first()
  if db_grading_in_progress_obj == None:
    if int(url_question_number) > 1 or int(url_question_number) < 1:
      localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
      return redirect(url_for('candidates_views_interior.candidates_assessment_expiring_function', url_assessment_expiring=url_assessment_expiring, url_question_number='1'))
  if db_grading_in_progress_obj != None:
    if int(url_question_number) != (int(db_grading_in_progress_obj.graded_count) + 1):
      localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
      return redirect(url_for('candidates_views_interior.candidates_assessment_expiring_function', url_assessment_expiring=url_assessment_expiring, url_question_number=str(int(db_grading_in_progress_obj.graded_count) + 1)))
  # ------------------------ check if question number already submitted start ------------------------
  # ------------------------ expire check based on email send datetime start ------------------------
  db_email_obj = CandidatesEmailSentObj.query.filter_by(assessment_expiring_url_fk=url_assessment_expiring).order_by(CandidatesEmailSentObj.created_timestamp.desc()).first()
  if db_email_obj == None:
    localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_assessment_invalid_function'))
  email_sent_timestamp = db_email_obj.created_timestamp      # type: datetime.datetime
  expired_assessment_check, assessment_not_open_yet_check = expired_assessment_check_function(email_sent_timestamp)
  if assessment_not_open_yet_check == True:
    localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_assessment_early_function'))
  if expired_assessment_check == True:
    localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_assessment_invalid_function'))
  # ------------------------ expire check based on email send datetime end ------------------------
  # ------------------------ pull schedule info start ------------------------
  db_schedule_obj = CandidatesScheduleObj.query.filter_by(expiring_url=url_assessment_expiring).first()
  if db_schedule_obj == None:
    localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_assessment_invalid_function'))
  # ------------------------ pull schedule info end ------------------------
  # ------------------------ pull schedule vars start ------------------------
  db_schedule_obj_user_id_fk = db_schedule_obj.user_id_fk
  db_schedule_obj_assessment_id_fk = db_schedule_obj.assessment_id_fk
  # ------------------------ pull schedule vars end ------------------------
  # ------------------------ pull assessment info start ------------------------
  db_assessment_obj = ZDontDeleteTableObj.query.filter_by(id=db_schedule_obj_assessment_id_fk).first()
  if db_assessment_obj == None:
    localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_assessment_invalid_function'))
  # ------------------------ pull assessment info end ------------------------
  # ------------------------ next question start ------------------------
  next_question_number = int(url_question_number) + 1
  # ------------------------ next question end ------------------------
  # ------------------------ get desired question id start ------------------------
  question_ids_str = db_assessment_obj.question_ids_arr
  question_ids_arr = question_ids_str.split(',')
  if int(url_question_number) == int(len(question_ids_arr)):
    next_question_number = 'submit'
  current_page_question_id = question_ids_arr[int(url_question_number)-1]
  # ------------------------ get desired question id end ------------------------
  # ------------------------ pull question info start ------------------------
  db_question_obj = ActivityACreatedQuestionsObj.query.filter_by(id=current_page_question_id).first()
  if db_question_obj == None:
    localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_assessment_invalid_function'))
  # ------------------------ pull question info start ------------------------
  # ------------------------ contains img start ------------------------
  contains_img = False
  if 'amazonaws.com' in db_question_obj.aws_image_url:
    contains_img = True
  # ------------------------ contains img end ------------------------
  # ------------------------ create categories tuple start ------------------------
  categories_tuple = categories_tuple_function(db_question_obj.categories)
  # ------------------------ create categories tuple end ------------------------
  # ------------------------ company name start ------------------------
  db_user_obj = UserObj.query.filter_by(id=db_schedule_obj_user_id_fk).first()
  if db_user_obj == None:
    localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.candidates_assessment_invalid_function'))
  user_company_name = db_user_obj.company_name
  if len(user_company_name) > 15:
    user_company_name = user_company_name[:14] + '...'
  # ------------------------ company name start ------------------------
  # ------------------------ post triggered start ------------------------
  if request.method == 'POST':
    # ------------------------ user input start ------------------------
    ui_answer_choice = request.form.get('ui_answer_choice_selected')
    # ------------------------ user input end ------------------------
    # ------------------------ validate ui start ------------------------
    allowed_answers_arr = ['a', 'b', 'c', 'd', 'e']
    if ui_answer_choice.lower() not in allowed_answers_arr:
      localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
      return redirect(url_for('candidates_views_interior.candidates_assessment_expiring_function', url_assessment_expiring=url_assessment_expiring, url_question_number=url_question_number, url_redirect_code='e1'))
    # ------------------------ validate ui start ------------------------
    # ------------------------ answer graded start ------------------------
    answer_result = False
    if ui_answer_choice.lower() == db_question_obj.answer.lower():
      answer_result = True
    current_db_question_obj = arr_of_dict_all_columns_single_item_function(db_question_obj, for_json_dumps=True)
    current_db_question_obj['user_answer'] = ui_answer_choice.lower()
    current_db_question_obj['user_answer_result'] = answer_result
    # ------------------------ answer graded end ------------------------
    # ------------------------ grading wip obj start ------------------------
    db_grading_in_progress_obj = CandidatesAssessmentGradedObj.query.filter_by(assessment_expiring_url_fk=url_assessment_expiring, status='wip').first()
    # ------------------------ grading wip obj end ------------------------
    # ------------------------ first answer start ------------------------
    if db_grading_in_progress_obj == None:
      # ------------------------ initialize variables start ------------------------
      current_correct_count = 0
      current_final_score = 0
      # ------------------------ initialize variables end ------------------------
      # ------------------------ updates before input start ------------------------
      if answer_result == True:
        current_correct_count += 1
        current_final_score = float(current_correct_count) / float(db_assessment_obj.total_questions)
      # ------------------------ updates before input end ------------------------
      # ------------------------ insert db start ------------------------
      try:
        new_row = CandidatesAssessmentGradedObj(
          id = create_uuid_function('graded_'),
          created_timestamp = create_timestamp_function(),
          candidate_email = db_schedule_obj.candidates, # str
          assessment_name = db_schedule_obj.assessment_name,  # str
          assessment_id_fk = db_schedule_obj.assessment_id_fk,  # str
          created_assessment_user_id_fk = db_schedule_obj.user_id_fk, # str
          assessment_expiring_url_fk = url_assessment_expiring, # str
          total_questions = db_assessment_obj.total_questions,  # int
          correct_count = int(current_correct_count), # int
          final_score = float(current_final_score), # float
          status = 'wip', # str
          graded_count = int('1'),
          assessment_obj = json.dumps(current_db_question_obj)
        )
        db.session.add(new_row)
        db.session.commit()
      except:
        pass
      # ------------------------ insert db end ------------------------
      # ------------------------ redirect next question start ------------------------
      localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
      return redirect(url_for('candidates_views_interior.candidates_assessment_expiring_function', url_assessment_expiring=url_assessment_expiring, url_question_number=next_question_number))
      # ------------------------ redirect next question end ------------------------
    # ------------------------ first answer end ------------------------
    # ------------------------ subsequent answers start ------------------------
    else:
      # ------------------------ build on existing variables start ------------------------
      current_correct_count = int(db_grading_in_progress_obj.correct_count)
      current_final_score = float(db_grading_in_progress_obj.final_score)
      if answer_result == True:
        current_correct_count += 1
        current_final_score = float(current_correct_count) / float(db_assessment_obj.total_questions)
      current_graded_count = int(db_grading_in_progress_obj.graded_count) + 1
      current_master_arr_of_dict = []
      previous_answers = json.loads(db_grading_in_progress_obj.assessment_obj)
      if isinstance(previous_answers, dict):
        current_master_arr_of_dict.append(previous_answers)
      if isinstance(previous_answers, list):
        for i in previous_answers:
          current_master_arr_of_dict.append(i)
      current_master_arr_of_dict.append(current_db_question_obj)
      # ------------------------ update db obj start ------------------------
      try:
        db_grading_in_progress_obj.correct_count = int(current_correct_count), # int
        db_grading_in_progress_obj.final_score = float(current_final_score), # float
        db_grading_in_progress_obj.graded_count = int(current_graded_count),  # int
        db_grading_in_progress_obj.assessment_obj = json.dumps(current_master_arr_of_dict)
        db.session.commit()
        localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
        return redirect(url_for('candidates_views_interior.candidates_assessment_expiring_function', url_assessment_expiring=url_assessment_expiring, url_question_number=next_question_number))
      except:
        pass
      # ------------------------ update db obj end ------------------------
      pass
    # ------------------------ subsequent answers end ------------------------
  # ------------------------ post triggered end ------------------------
  localhost_print_function(' ------------------------ candidates_assessment_expiring_function END ------------------------ ')
  return render_template('candidates/exterior/assessments/assessment_candidate_test/index.html', users_company_name_to_html=user_company_name, db_question_obj_to_html=db_question_obj, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type, next_question_number_to_html=next_question_number, current_question_number_to_html=url_question_number, url_assessment_expiring_to_html=url_assessment_expiring, contains_img_to_html=contains_img, categories_tuple_to_html=categories_tuple)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/request', methods=['GET', 'POST'])
@login_required
def candidates_categories_request_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ candidates_categories_request_function START ------------------------ ')
  alert_message_page, alert_message_type = alert_message_default_function()
  # ------------------------ redirect codes start ------------------------
  redirect_var = request.args.get('url_redirect_code')
  if redirect_var != None:
    if redirect_var == 's':
      alert_message_page = 'Request sent.'
      alert_message_type = 'success'
  # ------------------------ redirect codes end ------------------------
  # ------------------------ if post method hit start ------------------------
  ui_requested = ''
  if request.method == 'POST':
    ui_requested = request.form.get('ui_requested')
    ui_requested = sanitize_char_count_1_function(ui_requested)
    if ui_requested == False:
      alert_message_page = 'Requested categories should be 1-100 characters long.'
      alert_message_type = 'danger'
    else:
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
      # ------------------------ email self start ------------------------
      try:
        output_to_email = os.environ.get('TRIVIAFY_SUPPORT_EMAIL')
        output_subject = f'Triviafy - Requested Language - {current_user.email}'
        output_body = f"Hi there,\n\nRequester: {current_user.email}\nRequested: '{ui_requested}'\n\nBest,\nTriviafy"
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self end ------------------------
      return redirect(url_for('candidates_views_interior.candidates_categories_request_function', url_redirect_code='s'))
  # ------------------------ if post method hit end ------------------------
  localhost_print_function(' ------------------------ candidates_categories_request_function END ------------------------ ')
  return render_template('candidates/interior/request_categories/index.html', user=current_user, users_company_name_to_html=current_user.company_name, alert_message_page_to_html=alert_message_page, alert_message_type_to_html=alert_message_type)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/question/create/dashboard', methods=['GET', 'POST'])
@login_required
def candidates_create_question_dashboard_function():
  localhost_print_function(' ------------------------ candidates_create_question_dashboard_function START ------------------------ ')
  page_error_statement = ''
  # ------------------------ delete questions still draft start ------------------------
  db_questions_obj_arr = ActivityACreatedQuestionsObj.query.filter_by(fk_user_id=current_user.id,submission='draft',product='candidates').delete()
  db.session.commit()
  # ------------------------ delete questions still draft end ------------------------
  # ------------------------ pull from db start ------------------------
  db_questions_obj_arr = ActivityACreatedQuestionsObj.query.filter_by(fk_user_id=current_user.id,product='candidates').order_by(ActivityACreatedQuestionsObj.created_timestamp.desc()).all()
  total_questions_created = 0
  if db_questions_obj_arr == []:
    pass
  else:    
    total_questions_created = len(db_questions_obj_arr)
    db_questions_obj_arr = arr_of_dict_necessary_columns_function(db_questions_obj_arr, ['id', 'title', 'categories', 'question'])
    if len(db_questions_obj_arr[0]['categories']) > 15:
      shortened = db_questions_obj_arr[0]['categories'][0:19]
      db_questions_obj_arr[0]['categories'] = shortened
    if len(db_questions_obj_arr[0]['question']) > 15:
      shortened = db_questions_obj_arr[0]['question'][0:19]
      db_questions_obj_arr[0]['question'] = shortened
  # ------------------------ pull from db end ------------------------
  # ------------------------ pull from db start ------------------------
  db_test_drafts_obj_arr = ZDontDeleteTableObj.query.filter_by(user_id_fk=current_user.id,status='draft').all()
  db_test_drafts_obj_arr = arr_of_dict_necessary_columns_function(db_test_drafts_obj_arr, ['assessment_name', 'desired_languages_arr'])
  # ------------------------ pull from db end ------------------------
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function(current_user)
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ post submit start ------------------------
  if request.method == 'POST':
    # ------------------------ get form user inputs start ------------------------
    ui_questions_to_add_arr = request.form.getlist('uiQuestionSelected')
    ui_test_add_to = request.form.get('uiTestSelected')
    # ------------------------ get form user inputs end ------------------------
    # ------------------------ check valid inputs start ------------------------
    if len(ui_questions_to_add_arr) == 0 or ui_questions_to_add_arr == []:
      page_error_statement = 'Please select at least one custom question.'
    else:
      # ------------------------ check valid inputs question start ------------------------
      for i in ui_questions_to_add_arr:
        db_question_obj_exists_check = ActivityACreatedQuestionsObj.query.get(i)
        if db_question_obj_exists_check == None:
          break
      if db_question_obj_exists_check == None:
        page_error_statement = 'Invalid question ID submitted.'
      # ------------------------ check valid inputs question end ------------------------
      else:
        # ------------------------ check valid inputs test start ------------------------
        db_test_obj = ZDontDeleteTableObj.query.filter_by(user_id_fk=current_user.id,assessment_name=ui_test_add_to).first()
        if db_test_obj == None:
          page_error_statement = 'Invalid test name submitted.'
        # ------------------------ check valid inputs test end ------------------------
        else:
          # ------------------------ update latest draft test start ------------------------
          question_ids_str = db_test_obj.question_ids_arr
          current_total_questions = int(db_test_obj.total_questions)
          change_check = False
          for i in ui_questions_to_add_arr:
            if i not in question_ids_str:
              change_check = True
              question_ids_str += f',{i}'
              current_total_questions += 1
          if change_check == True:
            db_test_obj.question_ids_arr = question_ids_str
            db_test_obj.total_questions = current_total_questions
            db.session.commit()
          # ------------------------ update latest draft test end ------------------------
          # ------------------------ redirect start ------------------------
          localhost_print_function(' ------------------------ candidates_create_question_dashboard_function END ------------------------ ')
          return redirect(url_for('candidates_views_interior.candidates_assessment_create_review_function', url_assessment_name=ui_test_add_to))
          # ------------------------ redirect end ------------------------
    # ------------------------ check valid inputs end ------------------------
  # ------------------------ post submit end ------------------------
  localhost_print_function(' ------------------------ candidates_create_question_dashboard_function END ------------------------ ')
  return render_template('candidates/interior/create_question_dashboard/index.html', user=current_user, users_company_name_to_html=current_user.company_name, error_message_to_html=page_error_statement, stripe_subscription_obj_status_to_html=stripe_subscription_obj_status, total_questions_created_to_html=total_questions_created, db_questions_obj_arr_to_html=db_questions_obj_arr, db_test_drafts_obj_arr_to_html=db_test_drafts_obj_arr)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/question/create/v2', methods=['GET', 'POST'])
@login_required
def candidates_create_question_function_v2():
  localhost_print_function(' ------------------------ candidates_create_question_function_v2 START ------------------------ ')
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function(current_user)
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ redirect if not subscribed start ------------------------
  if stripe_subscription_obj_status != 'active':
    localhost_print_function(' ------------------------ candidates_create_question_function_v2 END ------------------------ ')
    return redirect(url_for('candidates_views_interior.login_dashboard_page_function'))
  # ------------------------ redirect if not subscribed end ------------------------
  # ------------------------ variables start ------------------------
  user_company_name = current_user.company_name
  if len(user_company_name) > 15:
    user_company_name = user_company_name[:14] + '...'
  # ------------------------ variables end ------------------------
  page_error_statement = ''
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
    # ------------------------ sanitize user inputs end ------------------------
    # ------------------------ error catch check start ------------------------
    if ui_option_e == None and ui_answer_checked.lower() == 'e':
      page_error_statement = 'Invalid answer choice'
    # ------------------------ error catch check end ------------------------
    else:
      # ------------------------ error catch check start ------------------------
      if ui_title_checked == False or ui_categories_checked == False or ui_question_checked == False or ui_option_a_checked == False or ui_option_b_checked == False or ui_option_c_checked == False or ui_option_d_checked == False or ui_option_e_checked == False or ui_answer_checked == False:
        page_error_statement = 'Invalid input(s)'
        localhost_print_function('Invalid input(s)!!!')
        localhost_print_function(' ------------------------ candidates_create_question_function_v2 END ------------------------ ')
      # ------------------------ error catch check end ------------------------
      else:
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
          insert_new_row = ActivityACreatedQuestionsObj(
            id=final_id,
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
            answer = ui_answer.upper(),
            aws_image_uuid = create_question_uploaded_image_uuid,
            aws_image_url = create_question_uploaded_image_aws_url,
            submission='draft',
            product = 'candidates',
            fk_group_id='candidates'
          )
          db.session.add(insert_new_row)
          db.session.commit()
        except:
          localhost_print_function('did not create question in db')
          pass
        # ------------------------ add to db end ------------------------
        # ------------------------ redirect start ------------------------
        return redirect(url_for('candidates_views_interior.candidates_preview_created_question_function'))
        # ------------------------ redirect end ------------------------
  localhost_print_function(' ------------------------ candidates_create_question_function_v2 END ------------------------ ')
  return render_template('candidates/interior/create_question_v2/index.html', user=current_user, users_company_name_to_html=user_company_name, error_message_to_html=page_error_statement)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@candidates_views_interior.route('/candidates/question/create/v2/preview', methods=['GET', 'POST'])
@login_required
def candidates_preview_created_question_function():
  localhost_print_function(' ------------------------ candidates_preview_created_question_function START ------------------------ ')
  # ------------------------ stripe subscription status check start ------------------------
  stripe_subscription_obj_status = check_stripe_subscription_status_function(current_user)
  # ------------------------ stripe subscription status check end ------------------------
  # ------------------------ redirect if not subscribed start ------------------------
  if stripe_subscription_obj_status != 'active':
    localhost_print_function(' ------------------------ candidates_preview_created_question_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.login_dashboard_page_function'))
  # ------------------------ redirect if not subscribed end ------------------------
  # ------------------------ variables start ------------------------
  user_company_name = current_user.company_name
  if len(user_company_name) > 15:
    user_company_name = user_company_name[:14] + '...'
  # ------------------------ variables end ------------------------
  # ------------------------ get latest custom question start ------------------------
  db_question_obj = ActivityACreatedQuestionsObj.query.filter_by(fk_user_id=current_user.id,submission='draft',product='candidates').order_by(ActivityACreatedQuestionsObj.created_timestamp.desc()).first()
  if db_question_obj == None:
    localhost_print_function(' ------------------------ candidates_preview_created_question_function END ------------------------ ')
    return redirect(url_for('candidates_views_interior.login_dashboard_page_function'))
  # ------------------------ get latest custom question end ------------------------
  # ------------------------ build latest dict start ------------------------
  question_info_dict = create_question_info_dict_function(db_question_obj)
  # ------------------------ build latest dict end ------------------------
  page_error_statement = ''
  if request.method == 'POST':
    db_question_obj.submission = 'submitted'
    db.session.commit()
    # ------------------------ email self start ------------------------
    try:
      output_to_email = os.environ.get('TRIVIAFY_SUPPORT_EMAIL')
      output_subject = f'Triviafy - Custom Question - {current_user.email}'
      output_body = f"Hi there,\n\nNew custom question created: {current_user.email} \n\nBest,\nTriviafy"
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
    # ------------------------ email self end ------------------------
    return redirect(url_for('candidates_views_interior.candidates_create_question_dashboard_function'))
  localhost_print_function(' ------------------------ candidates_preview_created_question_function END ------------------------ ')
  return render_template('candidates/interior/create_question_v2/submission/index.html', user=current_user, users_company_name_to_html=user_company_name, error_message_to_html=page_error_statement, question_info_dict_to_html=question_info_dict)
# ------------------------ individual route end ------------------------
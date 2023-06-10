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
from flask_login import login_required, current_user, logout_user
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from website import db
from website.backend.candidates.user_inputs import alert_message_default_function_v2
from website.backend.candidates.browser import browser_response_set_cookie_function_v6
from website.models import UserObj, EmailSentObj, UserSignupFeedbackObj
from website.backend.onboarding import onboarding_checks_v2_function
from website.backend.login_checks import product_login_checks_function
from website.backend.candidates.string_manipulation import breakup_email_function
import os
from website.backend.candidates.send_emails import send_email_template_function
from website.backend.candidates.user_inputs import get_special_characters_function
from website.backend.candidates.lists import get_month_days_years_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
polling_views_interior = Blueprint('polling_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/polling/dashboard', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/dashboard/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def polling_dashboard_function(url_redirect_code=None):
  # ------------------------ product login check start ------------------------
  is_match = product_login_checks_function(current_user,'polling')
  if is_match == False:
    logout_user()
    localhost_print_function('user logged out and redirecting to login product - polling')
    return redirect(url_for('polling_auth.polling_login_function'))
  # ------------------------ product login check end ------------------------
  # ------------------------ onboarding checks start ------------------------
  onbaording_status = onboarding_checks_v2_function(current_user)
  if onbaording_status == 'verify':
    return redirect(url_for('polling_views_interior.verify_email_function'))
  if onbaording_status == 'polling_terms_of_service':
    return redirect(url_for('polling_views_interior.polling_feedback_function', url_feedback_code=onbaording_status))
  if onbaording_status == 'attribute_birthday':
    return redirect(url_for('polling_views_interior.polling_feedback_function', url_feedback_code=onbaording_status))
  # ------------------------ onboarding checks end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'polling/interior/dashboard/index.html'
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
    return render_template(template_location_url, user=current_user, page_dict_to_html=page_dict)
  else:
    browser_response = browser_response_set_cookie_function_v6(current_user, template_location_url, page_dict)
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/polling/verify/success/<url_verification_code>')
@polling_views_interior.route('/polling/verify/success/<url_verification_code>/<url_redirect_code>')
@polling_views_interior.route('/polling/verify/success/<url_verification_code>/<url_redirect_code>/')
@login_required
def verification_code_clicked_function(url_redirect_code=None, url_verification_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ verification start ------------------------
  if url_verification_code == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function'))
  redis_uuid_value = ''
  try:
    redis_uuid_value = redis_connection.get(url_verification_code).decode('utf-8')
  except:
    return redirect(url_for('polling_views_interior.verify_email_function', url_redirect_code='e28'))
  db_user_obj = UserObj.query.filter_by(id=redis_uuid_value).first()
  db_user_obj.verified_email = True
  db.session.commit()
  redis_connection.delete(url_verification_code)
  # ------------------------ verification end ------------------------
  return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='s9'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/polling/verify', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/verify/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/verify/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def verify_email_function(url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ redirect check start ------------------------
  if current_user.verified_email == True:
    return redirect(url_for('polling_views_interior.polling_dashboard_function'))
  # ------------------------ redirect check end ------------------------
  page_dict['user_email'] = current_user.email
  page_dict['feedback_step'] = '0'
  output_subject = f'Verify Polling Email: {current_user.email}'
  # ------------------------ check if verify email already sent start ------------------------
  db_email_obj = EmailSentObj.query.filter_by(to_email=current_user.email,subject=output_subject).first()
  # ------------------------ check if verify email already sent end ------------------------
  if db_email_obj == None or db_email_obj == []:
    # ------------------------ verification code store in redis start ------------------------
    verification_code = create_uuid_function('verify_')
    redis_connection.set(verification_code, current_user.id.encode('utf-8'))
    # ------------------------ verification code store in redis end ------------------------
    # ------------------------ auto send first email to user start ------------------------
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
                        <p>Verify email link: http://127.0.0.1:80/polling/verify/success/{verification_code}</p>\
                        <p style='margin:0;'>Best,</p>\
                        <p style='margin:0;'>Triviafy Support Team</p>"
      # ------------------------ localhost end ------------------------
      # ------------------------ production start ------------------------
      else:
        output_body = f"<p>Hi {guessed_name},</p>\
                        <p>Please click the link below to verify your email address.</p>\
                        <p>Verify email link: https://triviafy.com/polling/verify/success/{verification_code}</p>\
                        <p style='margin:0;'>Best,</p>\
                        <p style='margin:0;'>Triviafy Support Team</p>"
      # ------------------------ production end ------------------------
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
    # ------------------------ auto send first email to user end ------------------------
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
                      <p>Verify email link: http://127.0.0.1:80/polling/verify/success/{new_verification_code}</p>\
                      <p style='margin:0;'>Best,</p>\
                      <p style='margin:0;'>Triviafy Support Team</p>"
      # ------------------------ localhost end ------------------------
      # ------------------------ production start ------------------------
      else:
        output_body = f"<p>Hi {guessed_name},</p>\
                        <p>Please click the link below to verify your email address.</p>\
                        <p>Verify email link: https://triviafy.com/polling/verify/success/{new_verification_code}</p>\
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
    return redirect(url_for('polling_views_interior.verify_email_function', url_redirect_code='s8'))
  # ------------------------ resend email end ------------------------
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'polling/interior/verify_email/index.html'
  # ------------------------ for setting cookie end ------------------------
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, page_dict_to_html=page_dict)
  else:
    browser_response = browser_response_set_cookie_function_v6(current_user, template_location_url, page_dict)
    return browser_response
  # ------------------------ auto set cookie end ------------------------
  # return render_template('polling/interior/verify_email/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/polling/feedback/<url_feedback_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/feedback/<url_feedback_code>/', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/feedback/<url_feedback_code>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def polling_feedback_function(url_redirect_code=None, url_feedback_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ set loading bar variables start ------------------------
  # if url_feedback_code == 'name':
  #   page_dict['feedback_step'] = '0'
  #   page_dict['feedback_request'] = url_feedback_code
  if url_feedback_code == 'polling_terms_of_service':
    page_dict['feedback_step'] = '1'
    page_dict['feedback_request'] = url_feedback_code
  if url_feedback_code == 'attribute_birthday':
    page_dict['feedback_step'] = '2'
    page_dict['feedback_request'] = url_feedback_code  
  # ------------------------ set loading bar variables end ------------------------
  # ------------------------ more specific variables start ------------------------
  months_arr = []
  days_arr = []
  years_arr = []
  month_day_dict = {}
  if url_feedback_code == 'attribute_birthday':
    # ------------------------ get month days dict start ------------------------
    months_arr, days_arr, years_arr, month_day_dict = get_month_days_years_function()
    page_dict['months_arr'] = months_arr
    page_dict['days_arr'] = days_arr
    page_dict['years_arr'] = years_arr
    # ------------------------ get month days dict end ------------------------
  # ------------------------ more specific variables end ------------------------
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    # # ------------------------ post feedback name start ------------------------
    # if url_feedback_code == 'name':
    #   # ------------------------ check if already answered start ------------------------
    #   if current_user.name != None and current_user.name != '':
    #     return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    #   # ------------------------ check if already answered end ------------------------
    #   # ------------------------ get user inputs start ------------------------
    #   ui_name = request.form.get('ui_name')
    #   ui_last_name = request.form.get('ui_last_name')
    #   # ------------------------ get user inputs end ------------------------
    #   # ------------------------ sanatize inputs start ------------------------
    #   if len(ui_name) <= 1 or len(ui_name) > 20 or len(ui_last_name) <= 1 or len(ui_last_name) > 20:
    #     return redirect(url_for('polling_views_interior.feedback_name_function', url_redirect_code='e19'))
    #   special_characters_arr = get_special_characters_function()
    #   for i in ui_name:
    #     if i in special_characters_arr:
    #       return redirect(url_for('polling_views_interior.feedback_name_function', url_redirect_code='e18'))
    #   for i in ui_last_name:
    #     if i in special_characters_arr:
    #       return redirect(url_for('polling_views_interior.feedback_name_function', url_redirect_code='e18'))
    #   # ------------------------ sanatize inputs end ------------------------
    #   # ------------------------ update db start ------------------------
    #   current_user.name = ui_name.lower().capitalize()
    #   current_user.last_name = ui_last_name.lower().capitalize()
    #   db.session.commit()
    #   # ------------------------ update db end ------------------------
    #   return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # # ------------------------ post feedback name end ------------------------
    # ------------------------ post feedback tos start ------------------------
    if url_feedback_code == 'polling_terms_of_service':
      # ------------------------ insert to db start ------------------------
      new_row = UserSignupFeedbackObj(
        id = create_uuid_function('feedback_'),
        created_timestamp = create_timestamp_function(),
        fk_user_id = current_user.id,
        fk_email = current_user.email,
        question = url_feedback_code,
        response = 'Complete'
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ insert to db end ------------------------
      return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ post feedback tos end ------------------------
    # ------------------------ post feedback birthday start ------------------------
    if url_feedback_code == 'attribute_birthday':
      # ------------------------ get user inputs start ------------------------
      ui_month_only = request.form.get('ui_month_only')
      ui_day_only = request.form.get('ui_day_only')
      ui_year_only = request.form.get('ui_year_only')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ insert to db start ------------------------
      # ------------------------ insert to db end ------------------------
      return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ post feedback birthday end ------------------------
  # ------------------------ submission end ------------------------
  # ------------------------ set cookie on first feedback step start ------------------------
  if url_feedback_code == 'polling_terms_of_service':
    # ------------------------ for setting cookie start ------------------------
    template_location_url = 'polling/interior/feedback/index.html'
    # ------------------------ for setting cookie end ------------------------
    # ------------------------ auto set cookie start ------------------------
    get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
    if get_cookie_value_from_browser != None:
      redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
      return render_template(template_location_url, user=current_user, page_dict_to_html=page_dict)
    else:
      browser_response = browser_response_set_cookie_function_v6(current_user, template_location_url, page_dict)
      return browser_response
    # ------------------------ auto set cookie end ------------------------
  # ------------------------ set cookie on first feedback step end ------------------------
  else:
    return render_template('polling/interior/feedback/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------
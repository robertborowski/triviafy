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
from website.models import UserObj, EmailSentObj, UserAttributesObj, ShowsFollowingObj, ShowsObj, PollsObj, PollsAnsweredObj, ShowsQueueObj
from website.backend.onboarding import onboarding_checks_v2_function
from website.backend.login_checks import product_login_checks_function
from website.backend.candidates.string_manipulation import breakup_email_function
import os
import json
from website.backend.candidates.send_emails import send_email_template_function
from website.backend.candidates.lists import get_month_days_years_function, get_marketing_list_v2_function
from website.backend.dates import get_years_from_date_function, return_ints_from_str_function
from website.backend.get_create_obj import get_all_shows_following_function, get_all_platforms_function, get_platform_based_on_name_function, get_all_shows_for_platform_function, get_show_based_on_name_function, get_show_based_on_id_and_platform_id_function, check_if_currently_following_show_function, get_show_based_on_id_function, get_poll_based_on_id_function, get_show_percent_of_all_polls_answered_function
from website.backend.spotify import spotify_search_show_function
from website.backend.user_inputs import sanitize_letters_numbers_spaces_specials_only_function, sanitize_text_v1_function
from website.backend.dict_manipulation import arr_of_dict_all_columns_single_item_function, prep_poll_dict_function
from website.backend.openai import create_openai_starter_poll_questions_function
from website.backend.show_utils import shows_following_arr_of_dict_function
from website.backend.sql_statements.select import select_general_function
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
  if onbaording_status == 'attribute_tos':
    return redirect(url_for('polling_views_interior.polling_feedback_function', url_feedback_code=onbaording_status))
  if onbaording_status == 'attribute_birthday':
    return redirect(url_for('polling_views_interior.polling_feedback_function', url_feedback_code=onbaording_status))
  if onbaording_status == 'attribute_marketing':
    return redirect(url_for('polling_views_interior.polling_feedback_function', url_feedback_code=onbaording_status))
  # ------------------------ onboarding checks end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ get all shows following sorted start ------------------------
  page_dict['shows_following_arr_of_dict'] = get_all_shows_following_function(current_user)
  page_dict = shows_following_arr_of_dict_function(page_dict)
  # ------------------------ get all shows following sorted end ------------------------
  # ------------------------ pull + calculate status bar percent complete start ------------------------
  try:
    show_counter = 0
    for i_dict in page_dict['shows_following_arr_of_dict']:
      i_dict['percent_total_polls_complete'], i_dict['user_completed_all_polls'] = get_show_percent_of_all_polls_answered_function(current_user.id, i_dict['id'])
      show_counter += 1
      i_dict['show_count'] = show_counter
  except:
    pass
  # ------------------------ pull + calculate status bar percent complete end ------------------------
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
    # ------------------------ redirect check start ------------------------
    if current_user.verified_email == True:
      return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ redirect check end ------------------------
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
  # ------------------------ double check redirect start ------------------------
  onbaording_status = onboarding_checks_v2_function(current_user)
  if onbaording_status != url_feedback_code:
    return redirect(url_for('polling_views_interior.polling_dashboard_function'))
  # ------------------------ double check redirect end ------------------------
  # ------------------------ set loading bar variables start ------------------------
  if url_feedback_code == 'attribute_tos':
    page_dict['feedback_step'] = '1'
    page_dict['feedback_request'] = url_feedback_code
  if url_feedback_code == 'attribute_birthday':
    page_dict['feedback_step'] = '2'
    page_dict['feedback_request'] = url_feedback_code
  if url_feedback_code == 'attribute_marketing':
    page_dict['feedback_step'] = '3'
    page_dict['feedback_request'] = url_feedback_code
  # ------------------------ set loading bar variables end ------------------------
  # ------------------------ more specific variables init start ------------------------
  months_arr = []
  days_arr = []
  years_arr = []
  month_day_dict = {}
  marketing_list = None
  marketing_list_index = None
  # ------------------------ more specific variables init end ------------------------
  # ------------------------ more specific variables for birthday start ------------------------
  if url_feedback_code == 'attribute_birthday':
    # ------------------------ get month days dict start ------------------------
    months_arr, days_arr, years_arr, month_day_dict = get_month_days_years_function()
    page_dict['months_arr'] = months_arr
    page_dict['days_arr'] = days_arr
    page_dict['years_arr'] = years_arr
    # ------------------------ get month days dict end ------------------------
  # ------------------------ more specific variables for birthday end ------------------------
  # ------------------------ more specific variables for marketing start ------------------------
  if url_feedback_code == 'attribute_marketing':
    # ------------------------ get current activities start ------------------------
    marketing_list, marketing_list_index = get_marketing_list_v2_function()
    page_dict['marketing_list'] = marketing_list
    page_dict['marketing_list_index'] = marketing_list_index
    # ------------------------ get current activities end ------------------------
  # ------------------------ more specific variables for marketing end ------------------------
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    # ------------------------ double check redirect start ------------------------
    if url_feedback_code == 'attribute_tos':
      onbaording_status = onboarding_checks_v2_function(current_user)
      if onbaording_status != url_feedback_code:
        return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    if url_feedback_code == 'attribute_birthday':
      onbaording_status = onboarding_checks_v2_function(current_user)
      if onbaording_status != url_feedback_code:
        return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ double check redirect end ------------------------
    # ------------------------ post feedback tos start ------------------------
    if url_feedback_code == 'attribute_tos':
      # ------------------------ insert to db start ------------------------
      new_row = UserAttributesObj(
        id=create_uuid_function('attribute_'),
        created_timestamp=create_timestamp_function(),
        fk_user_id=current_user.id,
        product='polling',
        attribute_code=url_feedback_code,
        attribute_response = 'Complete'
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ insert to db end ------------------------
      return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ post feedback tos end ------------------------
    # ------------------------ post feedback birthday start ------------------------
    if url_feedback_code == 'attribute_birthday':
      # ------------------------ get user inputs start ------------------------
      ui_birthday = request.form.get('ui_birthday')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ sanatize inputs start ------------------------
      ui_year, ui_month, ui_day = return_ints_from_str_function(ui_birthday)
      if ui_year == False or ui_month == False or ui_day == False:
        return redirect(url_for('polling_views_interior.polling_feedback_function', url_redirect_code='e6'))
      # ------------------------ sanatize inputs end ------------------------
      # ------------------------ sanatize inputs start ------------------------
      try:
        # birth month
        if int(ui_month) not in months_arr:
          return redirect(url_for('polling_views_interior.polling_feedback_function', url_redirect_code='e20', url_feedback_code=url_feedback_code))
      except:
        pass
      try:
        # birth day
        allowed_days_arr = month_day_dict[str(ui_month)]
        if int(ui_day) not in allowed_days_arr:
          return redirect(url_for('polling_views_interior.polling_feedback_function', url_redirect_code='e21', url_feedback_code=url_feedback_code))
      except:
        pass
      try:
        # birth year
        if int(ui_year) not in years_arr:
          return redirect(url_for('polling_views_interior.polling_feedback_function', url_redirect_code='e26', url_feedback_code=url_feedback_code))
      except:
        pass
      # ------------------------ sanatize inputs end ------------------------
      # ------------------------ age check start ------------------------
      current_age = get_years_from_date_function(ui_year, ui_month, ui_day)
      if float(current_age) < float(18.0):
        return redirect(url_for('polling_views_interior.polling_feedback_function', url_redirect_code='e30', url_feedback_code=url_feedback_code))
      # ------------------------ age check end ------------------------
      # ------------------------ insert to db start ------------------------
      new_row = UserAttributesObj(
        id=create_uuid_function('attribute_'),
        created_timestamp=create_timestamp_function(),
        fk_user_id=current_user.id,
        product='polling',
        attribute_code=url_feedback_code,
        attribute_year=ui_year,
        attribute_month=ui_month,
        attribute_day=ui_day
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ insert to db end ------------------------
      return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ post feedback birthday end ------------------------
    # ------------------------ post feedback marketing start ------------------------
    if url_feedback_code == 'attribute_marketing':
      ui_answer = request.form.get('ui_general_selection_radio')
      # ------------------------ invalid start ------------------------
      if ui_answer not in marketing_list:
        return redirect(url_for('polling_views_interior.polling_feedback_function', url_feedback_code=url_feedback_code, url_redirect_code='e6'))
      # ------------------------ invalid end ------------------------
      # ------------------------ insert to db start ------------------------
      new_row = UserAttributesObj(
        id=create_uuid_function('attribute_'),
        created_timestamp=create_timestamp_function(),
        fk_user_id=current_user.id,
        product='polling',
        attribute_code=url_feedback_code,
        attribute_response=ui_answer
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ insert to db end ------------------------
      return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ post feedback marketing end ------------------------
  # ------------------------ submission end ------------------------
  # ------------------------ set cookie on first feedback step start ------------------------
  if url_feedback_code == 'attribute_tos':
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

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/polling/loading/<url_platform_reference_id>')
@login_required
def polling_loading_function(url_platform_reference_id=None):
  # ------------------------ check url start ------------------------
  if url_platform_reference_id == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
  # ------------------------ check url end ------------------------
  # ------------------------ check if exists start ------------------------
  db_show_check_obj = ShowsObj.query.filter_by(platform_reference_id=url_platform_reference_id).first()
  if db_show_check_obj != None:
    db_show_following_obj = ShowsFollowingObj.query.filter_by(fk_show_id=db_show_check_obj.id,fk_user_id=current_user.id).first()
    if db_show_following_obj != None:
      return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=db_show_following_obj.fk_show_id, url_redirect_code='s16'))
  # ------------------------ check if exists end ------------------------
  return render_template('polling/interior/loading_screen/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/polling/show/add', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/add/', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/add/<url_step_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/add/<url_step_code>/', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/add/<url_step_code>/<url_platform_id>', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/add/<url_step_code>/<url_platform_id>/', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/add/<url_step_code>/<url_platform_id>/<url_redis_key>', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/add/<url_step_code>/<url_platform_id>/<url_redis_key>/', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/add/<url_step_code>/<url_platform_id>/<url_redis_key>/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/add/<url_step_code>/<url_platform_id>/<url_redis_key>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def polling_add_show_function(url_redirect_code=None, url_step_code='1', url_platform_id=None, url_redis_key=None):
  # ------------------------ page dict start ------------------------
  if url_redirect_code == None:
    try:
      url_redirect_code = request.args.get('url_redirect_code')
    except:
      pass
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ remove from redis check start ------------------------
  try:
    wip_key = request.args.get('wip_key')
    if wip_key != None and wip_key != '':
      redis_connection.delete(wip_key)
  except:
    pass
  # ------------------------ remove from redis check end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['url_step_code'] = url_step_code
  page_dict['url_platform_id'] = url_platform_id
  page_dict['url_redis_key'] = url_redis_key
  page_dict['url_next_step_code'] = str(int(url_step_code) + 1)
  page_dict['url_previous_step_code'] = str(int(url_step_code) - 1)
  page_dict['platforms_arr'] = []
  page_dict['shows_arr_of_dict'] = []
  page_dict['url_step_title'] = ''
  page_dict['url_back_str'] = ''
  page_dict['spotify_pulled_dict'] = None
  spotify_pulled_dict = {}
  # ------------------------ set variables end ------------------------
  # ------------------------ redirect steps check start ------------------------
  if url_step_code == '1' and url_platform_id != None:
    return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code))
  if url_step_code == '2' and (url_platform_id == None or url_redis_key != None):
    return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=page_dict['url_previous_step_code'], url_redirect_code='e6'))
  if url_step_code == '3' and (url_platform_id == None or url_redis_key == None):
    return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=page_dict['url_previous_step_code'], url_platform_id=url_platform_id, url_redirect_code='e6'))
  # ------------------------ redirect steps check end ------------------------
  # ------------------------ set back button string start ------------------------
  if url_step_code == '2':
    page_dict['url_back_str'] = f"{page_dict['url_previous_step_code']}"
  elif url_step_code == '3':
    page_dict['url_back_str'] = f"{page_dict['url_previous_step_code']}/{url_platform_id}?wip_key={url_redis_key}"
  # ------------------------ set back button string end ------------------------
  # ------------------------ get all sources following start ------------------------
  page_dict['shows_following_arr_of_dict'] = get_all_shows_following_function(current_user)
  # ------------------------ get all sources following end ------------------------
  # ------------------------ set title start ------------------------
  page_dict['url_step_subtitle'] = "Audience Polling Platform"
  if page_dict['url_step_code'] == '1':
    page_dict['url_step_title'] = 'Platform selection'
  if page_dict['url_step_code'] == '2':
    page_dict['url_step_title'] = 'Show selection'
  if page_dict['url_step_code'] == '3':
    page_dict['url_step_title'] = 'Confirm show'
  # ------------------------ set title end ------------------------
  # ------------------------ get platforms start ------------------------
  if page_dict['url_step_code'] == '1':
    all_platforms_obj = get_all_platforms_function()
    for i_obj in all_platforms_obj:
      page_dict['platforms_arr'].append(i_obj.name)
  # ------------------------ get platforms end ------------------------
  # ------------------------ get shows start ------------------------
  if page_dict['url_step_code'] == '2':
    all_shows_obj = get_all_shows_for_platform_function(page_dict['url_platform_id'])
    try:
      for i_obj in all_shows_obj:
        i_dict = {}
        i_dict['id'] = i_obj.id
        i_dict['fk_platform_id'] = i_obj.fk_platform_id
        i_dict['name'] = i_obj.name
        i_dict['platform_image_small'] = i_obj.platform_image_small
        i_dict['description'] = i_obj.description[0:100] + '...'
        page_dict['shows_arr_of_dict'].append(i_dict)
    except:
      pass
  # ------------------------ get shows end ------------------------
  # ------------------------ pull from redis if exists start ------------------------
  if page_dict['url_step_code'] == '3':
    try:
      redis_pulled_value = redis_connection.get(url_redis_key).decode('utf-8')
      spotify_pulled_dict = json.loads(redis_pulled_value)
      page_dict['spotify_pulled_dict'] = spotify_pulled_dict
    except:
      pass
  # ------------------------ pull from redis if exists end ------------------------
  if request.method == 'POST':
    if page_dict['url_step_code'] == '1':
      # ------------------------ get user inputs start ------------------------
      ui_platform_selection = request.form.get('ui_general_selection_radio')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ sanitize ui start ------------------------
      if ui_platform_selection not in page_dict['platforms_arr']:
        return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code, url_redirect_code='e6'))
      if ui_platform_selection != 'Podcast':
        return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code, url_redirect_code='e33'))
      # ------------------------ sanitize ui end ------------------------
      # ------------------------ get id based on user inputs start ------------------------
      db_obj = get_platform_based_on_name_function(ui_platform_selection)
      return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=page_dict['url_next_step_code'], url_platform_id=db_obj.id))
      # ------------------------ get id based on user inputs end ------------------------
    if page_dict['url_step_code'] == '2':
      # ------------------------ get user inputs start ------------------------
      ui_search_show_name = request.form.get('ui_search_show_name')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ sanitize ui start ------------------------
      ui_search_show_name_check = sanitize_letters_numbers_spaces_specials_only_function(ui_search_show_name)
      if ui_search_show_name_check == False:
        return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code, url_platform_id=url_platform_id, url_redirect_code='e6'))
      # ------------------------ sanitize ui end ------------------------
      # ------------------------ search spotify start ------------------------
      spotify_pulled_dict = spotify_search_show_function(ui_search_show_name)
      if spotify_pulled_dict == None:
        return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code, url_platform_id=url_platform_id, url_redirect_code='e32'))
      # ------------------------ search spotify end ------------------------
      # ------------------------ check if show already in db start ------------------------
      show_already_exists_check = get_show_based_on_name_function(url_platform_id, spotify_pulled_dict['name'])
      if show_already_exists_check != None:
        return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code, url_platform_id=url_platform_id, url_redirect_code='e31'))
      # ------------------------ check if show already in db end ------------------------
      # ------------------------ add spotify result to redis start ------------------------
      url_redis_key = create_uuid_function('spotify_temp_')
      redis_connection.set(url_redis_key, json.dumps(spotify_pulled_dict).encode('utf-8'))
      # ------------------------ add spotify result to redis end ------------------------
      return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=page_dict['url_next_step_code'], url_platform_id=url_platform_id, url_redis_key=url_redis_key))
    if page_dict['url_step_code'] == '3':
      # ------------------------ remove from redis start ------------------------
      try:
        redis_connection.delete(url_redis_key)
      except:
        pass
      # ------------------------ remove from redis end ------------------------
      # ------------------------ check if already in queue start ------------------------
      db_queue_obj = ShowsQueueObj.query.filter_by(name=spotify_pulled_dict['name']).first()
      # ------------------------ check if already in queue end ------------------------
      if db_queue_obj == None:
        # ------------------------ add to live job queue start ------------------------
        new_row = ShowsQueueObj(
          id=create_uuid_function('queue_'),
          created_timestamp=create_timestamp_function(),
          name=spotify_pulled_dict['name'],
          fk_platform_id = url_platform_id,
          platform_reference_id = spotify_pulled_dict['id']
        )
        db.session.add(new_row)
        db.session.commit()
        # ------------------------ add to live job queue end ------------------------
        return redirect(url_for('polling_views_interior.polling_loading_function', url_platform_reference_id=spotify_pulled_dict['id']))
      """
      new_show_id=create_uuid_function('show_')
      try:
        # ------------------------ openai get starter polls start ------------------------
        chatgpt_response_arr_of_dicts = create_openai_starter_poll_questions_function(spotify_pulled_dict['name'])
        if chatgpt_response_arr_of_dicts != None and chatgpt_response_arr_of_dicts != []:
          # ------------------------ if refresh/issue make sure does not already exist start ------------------------
          show_already_exists_check = get_show_based_on_name_function(url_platform_id, spotify_pulled_dict['name'])
          if show_already_exists_check != None:
            return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code, url_platform_id=url_platform_id, url_redirect_code='e31'))
          # ------------------------ if refresh/issue make sure does not already exist end ------------------------
          # ------------------------ add to db start ------------------------
          for i_dict in chatgpt_response_arr_of_dicts:
            answers_str = "~".join(i_dict['answer_choices'])
            new_row = PollsObj(
              id=create_uuid_function('poll_'),
              created_timestamp=create_timestamp_function(),
              type='show',
              fk_show_id=new_show_id,
              question=i_dict['question'],
              answer_choices=answers_str,
              status_approved=True,
              status_removed=False
            )
            db.session.add(new_row)
          db.session.commit()
          # ------------------------ add to db end ------------------------
          # ------------------------ openai get starter polls end ------------------------
          # ------------------------ insert to db start ------------------------
          new_row = ShowsObj(
            id=new_show_id,
            created_timestamp=create_timestamp_function(),
            name = spotify_pulled_dict['name'],
            description = spotify_pulled_dict['description'],
            fk_platform_id = url_platform_id,
            status = True,
            platform_reference_id = spotify_pulled_dict['id'],
            platform_image_large = spotify_pulled_dict['img_large'],
            platform_image_medium = spotify_pulled_dict['img_medium'],
            platform_image_small = spotify_pulled_dict['img_small'],
            platform_url = spotify_pulled_dict['show_url']
          )
          db.session.add(new_row)
          db.session.commit()
          # ------------------------ insert to db end ------------------------
          # ------------------------ insert to db start ------------------------
          new_row = ShowsFollowingObj(
            id=create_uuid_function('following_'),
            created_timestamp=create_timestamp_function(),
            fk_platform_id = url_platform_id,
            fk_show_id = new_show_id,
            fk_user_id = current_user.id
          )
          db.session.add(new_row)
          db.session.commit()
          # ------------------------ insert to db end ------------------------
      except:
        # ------------------------ delete in progress failed rows start ------------------------
        try:
          PollsObj.query.filter_by(fk_show_id=new_show_id).delete()
        except:
          pass
        try:
          ShowsObj.query.filter_by(id=new_show_id).delete()
        except:
          pass
        try:
          ShowsFollowingObj.query.filter_by(fk_show_id=new_show_id).delete()
        except:
          pass
        # ------------------------ delete in progress failed rows end ------------------------
        # ------------------------ remove from redis start ------------------------
        try:
          redis_connection.delete(url_redis_key)
        except:
          pass
        # ------------------------ remove from redis end ------------------------
        return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code='1', url_redirect_code='e34'))
      # ------------------------ remove from redis start ------------------------
      try:
        redis_connection.delete(url_redis_key)
      except:
        pass
      # ------------------------ remove from redis end ------------------------
      return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=new_show_id, url_redirect_code='s16'))
      """
  localhost_print_function(' ------------- 100-show selection start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-show selection end ------------- ')
  return render_template('polling/interior/show_select/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/polling/show/follow/<url_platform_id>/<url_show_id>', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/follow/<url_platform_id>/<url_show_id>/', methods=['GET', 'POST'])
@login_required
def polling_follow_show_function(url_platform_id=None, url_show_id=None):
  # ------------------------ check inputs start ------------------------
  if url_platform_id == None or url_show_id == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
  # ------------------------ check inputs end ------------------------
  # ------------------------ sanitize inputs start ------------------------
  db_obj = get_show_based_on_id_and_platform_id_function(url_show_id, url_platform_id)
  if db_obj == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
  # ------------------------ sanitize inputs end ------------------------
  # ------------------------ check if already following start ------------------------
  db_obj = check_if_currently_following_show_function(current_user, url_show_id, url_platform_id)
  if db_obj != None:
    return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_redirect_code='s16'))
  # ------------------------ check if already following end ------------------------
  # ------------------------ add to db start ------------------------
  new_row = ShowsFollowingObj(
    id=create_uuid_function('following_'),
    created_timestamp=create_timestamp_function(),
    fk_platform_id = url_platform_id,
    fk_show_id = url_show_id,
    fk_user_id = current_user.id
  )
  db.session.add(new_row)
  db.session.commit()
  # ------------------------ add to db end ------------------------
  # ------------------------ redirect to dashboard start ------------------------
  return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_redirect_code='s16'))
  # ------------------------ redirect to dashboard end ------------------------
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/polling/show/<url_show_id>', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/<url_show_id>/', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/<url_show_id>/<url_poll_id>', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/<url_show_id>/<url_poll_id>/', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/<url_show_id>/<url_poll_id>/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/show/<url_show_id>/<url_poll_id>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def polling_show_function(url_redirect_code=None, url_show_id=None, url_poll_id=None):
  # ------------------------ page dict start ------------------------
  if url_redirect_code == None:
    try:
      url_redirect_code = request.args.get('url_redirect_code')
    except:
      pass
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ pull show info start ------------------------
  db_show_obj = get_show_based_on_id_function(url_show_id)
  # ------------------------ check if show exists in db start ------------------------
  if db_show_obj == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
  # ------------------------ check if show exists in db end ------------------------
  page_dict['db_show_dict'] = arr_of_dict_all_columns_single_item_function(db_show_obj)
  title_limit = 15
  if len(page_dict['db_show_dict']['name']) > title_limit:
    page_dict['db_show_dict']['name_title'] = page_dict['db_show_dict']['name'][0:title_limit] + '...'
  else:
    page_dict['db_show_dict']['name_title'] = page_dict['db_show_dict']['name']
  # ------------------------ pull show info end ------------------------
  # ------------------------ variables start ------------------------
  page_dict['url_show_id'] = url_show_id
  page_dict['url_poll_id'] = url_poll_id
  page_dict['current_user_email'] = current_user.email
  page_dict['poll_answered'] = False
  page_dict['poll_answered_dict'] = None
  # ------------------------ variables end ------------------------
  # ------------------------ pull show + poll combination start ------------------------
  poll_arr_of_dict = []
  if url_poll_id != None:
    # ------------------------ check if poll exists in db start ------------------------
    db_poll_obj = get_poll_based_on_id_function(url_poll_id)
    if db_poll_obj == None:
      return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
    # ------------------------ check if poll exists in db end ------------------------
    # pull specific, unanswered or answered
    poll_arr_of_dict = select_general_function('select_query_general_2', url_show_id, url_poll_id)
  else:
    # pull random, unanswered
    poll_arr_of_dict = select_general_function('select_query_general_1', url_show_id, current_user.id)
    if poll_arr_of_dict == None or poll_arr_of_dict == []:
      return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='s17'))
  page_dict['poll_dict'] = prep_poll_dict_function(poll_arr_of_dict[0])
  if url_poll_id == None or url_poll_id != page_dict['poll_dict']['id']:
    return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code=url_redirect_code))
  # ------------------------ pull show + poll combination end ------------------------
  # ------------------------ pull + calculate status bar percent complete start ------------------------
  page_dict['percent_total_polls_complete'], page_dict['user_completed_all_polls'] = get_show_percent_of_all_polls_answered_function(current_user.id, url_show_id)
  # ------------------------ pull + calculate status bar percent complete end ------------------------
  # ------------------------ pull latest answer if exists start ------------------------
  try:
    db_latest_poll_obj = PollsAnsweredObj.query.filter_by(fk_show_id=url_show_id,fk_poll_id=url_poll_id,fk_user_id=current_user.id).order_by(PollsAnsweredObj.created_timestamp.desc()).first()
    page_dict['poll_answered_dict'] = arr_of_dict_all_columns_single_item_function(db_latest_poll_obj)
    page_dict['poll_answered'] = True
  except:
    pass
  # ------------------------ pull latest answer if exists end ------------------------
  if request.method == 'POST':
    # ------------------------ get ui start ------------------------
    ui_answer_selected = request.form.get('ui_selection_radio')
    ui_anonymous_check = request.form.get('ui_anonymous_check')
    ui_vote_question = request.form.get('ui_vote_question')
    ui_vote_feedback = request.form.get('ui_vote_feedback')
    ui_written_feedback = request.form.get('ui_written_feedback')
    # ------------------------ get ui end ------------------------
    # ------------------------ sanatize ui start ------------------------
    if ui_answer_selected not in page_dict['poll_dict']['answer_choices']:
      return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code='e6'))
    if ui_anonymous_check != None and ui_anonymous_check != 'ui_checked':
      return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code='e6'))
    if ui_vote_question != None and ui_vote_question != 'up' and ui_vote_question != 'down':
      return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code='e6'))
    if ui_vote_feedback != None and ui_vote_feedback != 'up' and ui_vote_feedback != 'down':
      return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code='e6'))
    ui_written_feedback = sanitize_text_v1_function(ui_written_feedback, 150, False)
    if ui_written_feedback == False:
      return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code='e6'))
    # ------------------------ sanatize ui end ------------------------
    # ------------------------ variables before insert start ------------------------
    if ui_vote_question == 'up':
      ui_vote_question = True
    if ui_vote_question == 'down':
      ui_vote_question = False
    if ui_vote_feedback == 'up':
      ui_vote_feedback = True
    if ui_vote_feedback == 'down':
      ui_vote_feedback = False
    if ui_anonymous_check == 'ui_checked':
      ui_anonymous_check = True
    # ------------------------ variables before insert end ------------------------
    # ------------------------ insert to db start ------------------------
    new_row = PollsAnsweredObj(
      id=create_uuid_function('vote_'),
      created_timestamp=create_timestamp_function(),
      fk_show_id=url_show_id,
      fk_poll_id=url_poll_id,
      fk_user_id=current_user.id,
      poll_answer_submitted=ui_answer_selected,
      written_answer_submitted=ui_written_feedback,
      status_answer_anonymous=ui_anonymous_check,
      poll_vote_updown_question=ui_vote_question,
      poll_vote_updown_feedback=ui_vote_feedback
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ insert to db end ------------------------
    return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id']))
  localhost_print_function(' ------------- 100-show poll start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-show poll end ------------- ')
  return render_template('polling/interior/poll/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------
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
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from website import db
from website.backend.candidates.user_inputs import alert_message_default_function_v2
from website.models import ActivityAGroupQuestionsUsedObj, ActivityASettingsObj, GroupObj, ActivityATestGradedObj, ActivityATestObj, UserObj, StripeCheckoutSessionObj, EmailDeletedObj, EmailSentObj, EmailCollectObj, UserFeatureRequestObj, EmailScrapedObj, UserSignupFeedbackObj, UserCelebrateObj, UserDesiredCategoriesObj, ActivityBGroupQuestionsUsedObj, ActivityBSettingsObj, ActivityBTestGradedObj, ActivityBTestObj, ActivityACreatedQuestionsObj
import os
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
from website.backend.candidates.sql_statements.sql_statements_select_general_v1_jobs import select_general_v1_jobs_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from datetime import datetime
from website.backend.candidates.string_manipulation import breakup_email_function
from website.backend.candidates.send_emails import send_email_template_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.backend.candidates.user_inputs import sanitize_email_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
admin_views_interior = Blueprint('admin_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@admin_views_interior.route('/admin', methods=['GET', 'POST'])
@admin_views_interior.route('/admin/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def admin_dashboard_page_function(url_redirect_code=None):
  # ------------------------ ensure correct email start ------------------------
  if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
    return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e9'))
  # ------------------------ ensure correct email end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ add scraped email start ------------------------
  if request.method == 'POST':
    ui_email = request.form.get('NewScrapedEmail').lower()
    # ------------------------ sanitize start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email)
    if ui_email_cleaned == False:
      return redirect(url_for('admin_views_interior.admin_dashboard_page_function', url_redirect_code='e1'))
    # ------------------------ sanitize end ------------------------
    # ------------------------ check if user alread exists start ------------------------
    db_users_obj = UserObj.query.filter_by(email=ui_email,signup_product='employees').first()
    if db_users_obj != None and db_users_obj != []:
      return redirect(url_for('admin_views_interior.admin_dashboard_page_function', url_redirect_code='e3'))
    # ------------------------ check if user alread exists end ------------------------
    # ------------------------ check if collected email alread exists start ------------------------
    db_collected_obj = EmailCollectObj.query.filter_by(email=ui_email).first()
    if db_collected_obj != None and db_collected_obj != []:
      return redirect(url_for('admin_views_interior.admin_dashboard_page_function', url_redirect_code='e3'))
    # ------------------------ check if collected email alread exists end ------------------------
    # ------------------------ check if scraped email alread exists start ------------------------
    db_scraped_obj = EmailScrapedObj.query.filter_by(email=ui_email).first()
    if db_scraped_obj != None and db_scraped_obj != []:
      return redirect(url_for('admin_views_interior.admin_dashboard_page_function', url_redirect_code='e3'))
    # ------------------------ check if scraped email alread exists end ------------------------
    # ------------------------ insert email to db start ------------------------
    new_row = EmailScrapedObj(
      id = create_uuid_function('scraped_'),
      created_timestamp = create_timestamp_function(),
      email = ui_email
    )
    db.session.add(new_row)
    db.session.commit()
    return redirect(url_for('admin_views_interior.admin_dashboard_page_function', url_redirect_code='s10'))
    # ------------------------ insert email to db end ------------------------
  # ------------------------ add scraped email end ------------------------
  return render_template('admin_page/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@admin_views_interior.route('/admin/d', methods=['GET', 'POST'])
@admin_views_interior.route('/admin/d/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def admin_delete_page_function(url_redirect_code=None):
  # ------------------------ ensure correct email start ------------------------
  if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
    return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e9'))
  # ------------------------ ensure correct email end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  if request.method == 'POST':
    # ------------------------ ensure correct email on post to be safe start ------------------------
    try:
      if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
        return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e9'))
    except:
      return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e9'))
    # ------------------------ ensure correct email on post to be safe end ------------------------
    # ------------------------ DeleteOneGroupAllEmployeesTables start ------------------------
    group_to_delete = request.form.get('DeleteOneGroupAllEmployeesTables')
    if group_to_delete != None:
      try:
        ActivityACreatedQuestionsObj.query.filter_by(fk_group_id=group_to_delete,product='birthday').delete()
      except:
        pass
      try:
        ActivityACreatedQuestionsObj.query.filter_by(fk_group_id=group_to_delete,product='job_start_date').delete()
      except:
        pass
      try:
        ActivityAGroupQuestionsUsedObj.query.filter_by(fk_group_id=group_to_delete).delete()
      except:
        pass
      try:
        ActivityASettingsObj.query.filter_by(fk_group_id=group_to_delete).delete()
      except:
        pass
      try:
        ActivityATestGradedObj.query.filter_by(fk_group_id=group_to_delete).delete()
      except:
        pass
      try:
        ActivityATestObj.query.filter_by(fk_group_id=group_to_delete).delete()
      except:
        pass
      try:
        ActivityBGroupQuestionsUsedObj.query.filter_by(fk_group_id=group_to_delete).delete()
      except:
        pass
      try:
        ActivityBSettingsObj.query.filter_by(fk_group_id=group_to_delete).delete()
      except:
        pass
      try:
        ActivityBTestGradedObj.query.filter_by(fk_group_id=group_to_delete).delete()
      except:
        pass
      try:
        ActivityBTestObj.query.filter_by(fk_group_id=group_to_delete).delete()
      except:
        pass
      try:
        GroupObj.query.filter_by(public_group_id=group_to_delete).delete()
      except:
        pass
      try:
        UserCelebrateObj.query.filter_by(fk_group_id=group_to_delete).delete()
      except:
        pass
      try:
        UserFeatureRequestObj.query.filter_by(fk_group_id=group_to_delete).delete()
      except:
        pass
      try:
        UserSignupFeedbackObj.query.filter_by(fk_group_id=group_to_delete, question='birthday_choice').delete()
      except:
        pass
      try:
        UserSignupFeedbackObj.query.filter_by(fk_group_id=group_to_delete, question='job_start_date_choice').delete()
      except:
        pass
      db.session.commit()
      return redirect(url_for('admin_views_interior.admin_delete_page_function', url_redirect_code='w1'))
    # ------------------------ DeleteOneGroupAllEmployeesTables end ------------------------
    # ------------------------ DeleteOneUserInAllGroupsAllEmployeesTables start ------------------------
    user_to_delete_from_groups = request.form.get('DeleteOneUserInAllGroupsAllEmployeesTables')
    if user_to_delete_from_groups != None:
      try:
        db_users_obj = UserObj.query.filter_by(email=user_to_delete_from_groups).first()
        db_users_dict = arr_of_dict_all_columns_single_item_function(db_users_obj)
        # ------------------------ check if alone start ------------------------
        db_all_users_obj = UserObj.query.filter_by(company_name=db_users_dict['company_name']).all()
        if len(db_all_users_obj) == 1:
          return redirect(url_for('admin_views_interior.admin_delete_page_function', url_redirect_code='e11'))
        # ------------------------ check if alone end ------------------------
      except:
        return redirect(url_for('admin_views_interior.admin_delete_page_function', url_redirect_code='e10'))
      UserFeatureRequestObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
      ActivityATestGradedObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
      db.session.commit()
      return redirect(url_for('admin_views_interior.admin_delete_page_function', url_redirect_code='w1'))
    # ------------------------ DeleteOneUserInAllGroupsAllEmployeesTables end ------------------------
    # ------------------------ DeleteOneUserAllCandidatesAndEmployeesTables start ------------------------
    user_to_delete = request.form.get('DeleteOneUserAllCandidatesAndEmployeesTables')
    if user_to_delete != None:
      try:
        db_users_obj = UserObj.query.filter_by(email=user_to_delete).first()
        db_users_dict = arr_of_dict_all_columns_single_item_function(db_users_obj)
      except:
        return redirect(url_for('admin_views_interior.admin_delete_page_function', url_redirect_code='e10'))
      # ------------------------ check if user is subscribed start ------------------------
      if (db_users_dict['fk_stripe_subscription_id'] != '' and db_users_dict['fk_stripe_subscription_id'] != None) or (db_users_dict['employees_fk_stripe_subscription_id'] != '' and db_users_dict['employees_fk_stripe_subscription_id'] != None):
        return redirect(url_for('admin_views_interior.admin_delete_page_function', url_redirect_code='i2'))
      # ------------------------ check if user is subscribed end ------------------------
      # ------------------------ delete from employees tables start ------------------------
      db_all_users_obj = UserObj.query.filter_by(company_name=db_users_dict['company_name']).all()
      if len(db_all_users_obj) == 1:
        # ------------------------ if user is the only one from company start ------------------------
        try:
          group_to_delete = db_users_dict['group_id']
          try:
            ActivityACreatedQuestionsObj.query.filter_by(fk_user_id=db_users_dict['id'],product='birthday').delete()
          except:
            pass
          try:
            ActivityACreatedQuestionsObj.query.filter_by(fk_user_id=db_users_dict['id'],product='job_start_date').delete()
          except:
            pass
          try:
            ActivityAGroupQuestionsUsedObj.query.filter_by(fk_group_id=group_to_delete).delete()
          except:
            pass
          try:
            ActivityBGroupQuestionsUsedObj.query.filter_by(fk_group_id=group_to_delete).delete()
          except:
            pass
          try:
            ActivityASettingsObj.query.filter_by(fk_group_id=group_to_delete).delete()
          except:
            pass
          try:
            ActivityBSettingsObj.query.filter_by(fk_group_id=group_to_delete).delete()
          except:
            pass
          try:
            ActivityATestGradedObj.query.filter_by(fk_group_id=group_to_delete).delete()
          except:
            pass
          try:
            ActivityBTestGradedObj.query.filter_by(fk_group_id=group_to_delete).delete()
          except:
            pass
          try:
            ActivityATestObj.query.filter_by(fk_group_id=group_to_delete).delete()
          except:
            pass
          try:
            ActivityBTestObj.query.filter_by(fk_group_id=group_to_delete).delete()
          except:
            pass
          try:
            EmailSentObj.query.filter_by(to_email=user_to_delete).delete()
          except:
            pass
          try:
            GroupObj.query.filter_by(public_group_id=group_to_delete).delete()
          except:
            pass
          try:
            StripeCheckoutSessionObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
          except:
            pass
          try:
            UserCelebrateObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
          except:
            pass
          try:
            UserDesiredCategoriesObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
          except:
            pass
          try:
            UserFeatureRequestObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
          except:
            pass
          try:
            UserObj.query.filter_by(id=db_users_dict['id']).delete()
          except:
            pass
          try:
            UserSignupFeedbackObj.query.filter_by(fk_email=user_to_delete).delete()
          except:
            pass
        except:
          pass
        # ------------------------ if user is the only one from company end ------------------------
      # ------------------------ delete from employees tables end ------------------------
      elif len(db_all_users_obj) > 1:
        try:
          try:
            ActivityACreatedQuestionsObj.query.filter_by(fk_user_id=db_users_dict['id'],product='birthday').delete()
          except:
            pass
          try:
            ActivityACreatedQuestionsObj.query.filter_by(fk_user_id=db_users_dict['id'],product='job_start_date').delete()
          except:
            pass
          try:
            ActivityATestGradedObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
          except:
            pass
          try:
            ActivityBTestGradedObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
          except:
            pass
          try:
            EmailSentObj.query.filter_by(to_email=user_to_delete).delete()
          except:
            pass
          try:
            StripeCheckoutSessionObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
          except:
            pass
          try:
            UserCelebrateObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
          except:
            pass
          try:
            UserDesiredCategoriesObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
          except:
            pass
          try:
            UserFeatureRequestObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
          except:
            pass
          try:
            UserObj.query.filter_by(id=db_users_dict['id']).delete()
          except:
            pass
          try:
            UserSignupFeedbackObj.query.filter_by(fk_email=user_to_delete).delete()
          except:
            pass
        except:
          pass
      # ------------------------ delete from user table start ------------------------
      # ------------------------ add unique removed email to db start ------------------------
      try:
        new_row = EmailDeletedObj(
          id=create_uuid_function('removed_'),
          created_timestamp=create_timestamp_function(),
          email=user_to_delete,
          uuid_archive=db_users_dict['id']
        )
        db.session.add(new_row)
      except:
        pass
      # ------------------------ add unique removed email to db end ------------------------
      db.session.commit()
      # ------------------------ delete from user table end ------------------------
      return redirect(url_for('admin_views_interior.admin_delete_page_function', url_redirect_code='w1'))
    # ------------------------ DeleteOneUserAllCandidatesAndEmployeesTables end ------------------------
    # ------------------------ DeleteRedisDeletedCookies start ------------------------
    delete_unused_cookies_from_redis = request.form.get('DeleteRedisDeletedCookies')
    if delete_unused_cookies_from_redis != None:
      # ------------------------ delete from redis start ------------------------
      # ------------------------ get all current user id's as set start ------------------------
      postgres_connection, postgres_cursor = postgres_connect_to_database_function()
      sql_input = 'user_obj'
      query_result_arr_of_dicts = select_general_v1_jobs_function(postgres_connection, postgres_cursor, 'select_table1_id', additional_input=sql_input)

      user_ids_set = {'a'}
      for i in query_result_arr_of_dicts:
        if i['id'] not in user_ids_set:
          user_ids_set.add(i['id'])
      user_ids_set.remove('a')
      # ------------------------ get all current user id's as set end ------------------------
      # ------------------------ loop through redis start ------------------------
      # Connect to redis database pool (no need to close)
      redis_connection = redis_connect_to_database_function()
      redis_keys = redis_connection.keys()
      for key in redis_keys:
        value = redis_connection.get(key).decode('utf-8')
        # ------------------------ remove stored cookies of deleted users start ------------------------
        if 'bcooke' in str(key):
          if value not in user_ids_set:
            localhost_print_function(f'deleting key: {key} | value: {value}')
            redis_connection.delete(key)
        # ------------------------ remove stored cookies of deleted users end ------------------------
        # ------------------------ delete keys not related to triviafy start ------------------------
        if 'bcooke' not in str(key):
          localhost_print_function(f'deleting key: {key} | value: {value}')
          redis_connection.delete(key)
        # ------------------------ delete keys not related to triviafy end ------------------------
      # ------------------------ loop through redis end ------------------------
      postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
      # ------------------------ delete from redis end ------------------------
      return redirect(url_for('admin_views_interior.admin_delete_page_function', url_redirect_code='w1'))
    # ------------------------ DeleteRedisDeletedCookies end ------------------------
  return render_template('admin_page/delete/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@admin_views_interior.route('/admin/a', methods=['GET', 'POST'])
@admin_views_interior.route('/admin/a/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def admin_analytics_page_function(url_redirect_code=None):
  # ------------------------ ensure correct email start ------------------------
  if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
    return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e9'))
  # ------------------------ ensure correct email end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  master_arr_of_dicts_01 = []
  db_groups_obj = GroupObj.query.all()
  """
  # ------------------------ loop groups start ------------------------
  for i_group_obj in db_groups_obj:
    # ------------------------ new i_dict start ------------------------
    i_dict = {}
    i_dict['group_progress'] = 'no tests yet'
    # ------------------------ new i_dict end ------------------------
    i_group_dict = arr_of_dict_all_columns_single_item_function(i_group_obj)
    i_dict['created_timestamp'] = i_group_dict['created_timestamp']
    i_dict['company_name'] = i_group_dict['fk_company_name']
    i_dict['public_group_id'] = i_group_dict['public_group_id']
    # ------------------------ total users start ------------------------
    db_all_users_obj = UserObj.query.filter_by(company_name=i_group_dict['fk_company_name']).all()
    i_dict['total_users_with_same_company_name'] = len(db_all_users_obj)
    # ------------------------ total users end ------------------------
    # ------------------------ latest test start ------------------------
    db_latest_test_obj = ActivityATestObj.query.filter_by(fk_group_id=i_group_dict['public_group_id'],product='trivia').order_by(ActivityATestObj.created_timestamp.desc()).first()
    i_dict['latest_test_id'] = None
    i_dict['latest_test_participation'] = 0
    try:
      i_dict['latest_test_id'] = db_latest_test_obj.id
      # ------------------------ latest test graded start ------------------------
      try:
        db_latest_test_graded_obj = ActivityATestGradedObj.query.filter_by(fk_group_id=i_group_dict['public_group_id'], status='complete',product='trivia').all()
        i_dict['latest_test_participation'] = len(db_latest_test_graded_obj)
        if int(i_dict['latest_test_participation']) > 0:
          if int(i_dict['latest_test_participation']) == int(i_dict['total_users_with_same_company_name']):
            if int(i_dict['total_users_with_same_company_name']) == 1:
              i_dict['group_progress'] = 'complete full alone'
            else:
              i_dict['group_progress'] = 'complete full'
          else:
            i_dict['group_progress'] = 'complete partial'
      except:
        pass
      # ------------------------ latest test graded end ------------------------
    except:
      pass
    # ------------------------ latest test end ------------------------
    # ------------------------ append i_dict start ------------------------
    master_arr_of_dicts_01.append(i_dict)
    # ------------------------ append i_dict end ------------------------
  # ------------------------ loop groups end ------------------------
  """
  page_dict['master_arr_of_dicts_01'] = master_arr_of_dicts_01
  # ------------------------ candidate_only_emails_arr start ------------------------
  candidate_only_emails_arr = []
  db_users_obj = UserObj.query.all()
  for i_obj in db_users_obj:
    db_group_obj = GroupObj.query.filter_by(fk_company_name=i_obj.company_name).first()
    if db_group_obj == None or db_group_obj == []:
      if i_obj.email not in candidate_only_emails_arr:
        candidate_only_emails_arr.append(i_obj.email)
  page_dict['candidate_only_emails_arr'] = candidate_only_emails_arr
  page_dict['total_candidate_only_emails'] = len(candidate_only_emails_arr)
  # ------------------------ candidate_only_emails_arr end ------------------------
  # ------------------------ landing_collect_emails_arr start ------------------------
  landing_collect_emails_arr = []
  db_collected_obj = EmailCollectObj.query.filter_by(unsubscribed=False).all()
  for i_obj in db_collected_obj:
    landing_collect_emails_arr.append(i_obj.email)
  page_dict['landing_collect_emails_arr'] = landing_collect_emails_arr
  page_dict['total_landing_collect_emails_arr'] = len(landing_collect_emails_arr)
  # ------------------------ landing_collect_emails_arr end ------------------------
  # ------------------------ scraped_collect_emails_arr start ------------------------
  scraped_emails_arr = []
  db_scraped_obj = EmailScrapedObj.query.filter_by(unsubscribed=False).all()
  for i_obj in db_scraped_obj:
    scraped_emails_arr.append(i_obj.email)
  page_dict['scraped_emails_arr'] = scraped_emails_arr
  page_dict['total_scraped_emails_arr'] = len(scraped_emails_arr)
  # ------------------------ scraped_collect_emails_arr end ------------------------
  # ------------------------ post method start ------------------------
  if request.method == 'POST':
    # ------------------------ initialize on post start ------------------------
    # ------------------------ get today's date start ------------------------
    todays_date_str = datetime.today().strftime('%Y-%m-%d')   # 2023-02-25
    # ------------------------ get today's date end ------------------------
    # ------------------------ append all team member emails start ------------------------
    for i_dict in page_dict['master_arr_of_dicts_01']:
      team_member_emails_arr = []
      db_all_users_obj = UserObj.query.filter_by(company_name=i_dict['company_name']).all()
      for i in db_all_users_obj:
        if i.email not in team_member_emails_arr:
          team_member_emails_arr.append(i.email)
      i_dict['team_member_emails_arr'] = team_member_emails_arr
    # ------------------------ append all team member emails end ------------------------
    # ------------------------ initialize on post end ------------------------
    # ------------------------ SendStatusEmails start ------------------------
    status_email_hit = request.form.get('SendStatusEmails')
    if status_email_hit == 'all':
      for i_dict in page_dict['master_arr_of_dicts_01']:
        # ------------------------ progress option start ------------------------
        if i_dict['group_progress'] == 'no tests yet':
          for i_email in i_dict['team_member_emails_arr']:
            # ------------------------ send email start ------------------------
            guessed_name = breakup_email_function(i_email)
            output_to_email = i_email
            output_subject = f"Action Required: {todays_date_str}"
            output_body = f"Hi {guessed_name},\n\nYour team's latest trivia contest https://triviafy.com/dashboard \n\nBest,\nTriviafy Support Team\nReply 'stop' to unsubscribe."
            # ------------------------ check if email+subject already sent today start ------------------------
            db_email_sent_obj = EmailSentObj.query.filter_by(to_email=output_to_email, subject=output_subject).first()
            if db_email_sent_obj != None and db_email_sent_obj != []:
              localhost_print_function(f'email already sent to this {output_to_email} - {output_subject}')
              continue
            # ------------------------ check if email+subject already sent today end ------------------------
            else:
              send_email_template_function(output_to_email, output_subject, output_body)
              # ------------------------ send email end ------------------------
              # ------------------------ insert email to db start ------------------------
              new_row = EmailSentObj(
                id = create_uuid_function('progress_'),
                created_timestamp = create_timestamp_function(),
                from_user_id_fk = current_user.id,
                to_email = output_to_email,
                subject = output_subject,
                body = output_body
              )
              db.session.add(new_row)
              db.session.commit()
              # ------------------------ insert email to db end ------------------------
        # ------------------------ progress option end ------------------------
      return redirect(url_for('admin_views_interior.admin_analytics_page_function', url_redirect_code='s7'))
    # ------------------------ SendStatusEmails end ------------------------
    # ------------------------ SendTryEmployeesEmails start ------------------------
    status_email_hit = request.form.get('SendTryEmployeesEmails')
    if status_email_hit == 'all':
      for i_email in page_dict['candidate_only_emails_arr']:
        # ------------------------ send email start ------------------------
        guessed_name = breakup_email_function(i_email)
        output_to_email = i_email
        output_subject = f"Your Recognition {todays_date_str}"
        output_body = f"<p>Hi {guessed_name},</p>\
                        <p>As someone who is always looking for new and exciting ways to build strong teams and advance your career, I want to introduce you to Triviafy - the leading team building software platform that is taking the corporate world by storm.</p>\
                        <p>With Triviafy, you'll gain access to a vast array of team-building activities that will help you engage with your colleagues, build stronger relationships, and ultimately, advance your career. With features such as trivia games, picture quizzes, icebreakers, birthday games, personality tests, employee surveys, and daily questionnaires, Triviafy provides a unique and fun way to bond with your team. The best part is that all team-building activities are asynchronous!</p>\
                        <p>But that's not all. By using Triviafy, you'll also get exposure within your company and increase your chances of getting that promotion you've been working towards. With higher employee engagement metrics and improved collaboration, your managers will see you as a standout performer and someone who is committed to the success of the team.</p>\
                        <p>Don't just take my word for it - give Triviafy a try and see for yourself how it can help you achieve your career goals. Sign up today and start building stronger relationships with your colleagues while advancing your career.</p>\
                        <p>Thank you for considering Triviafy.</p>\
                        <p style='margin:0;'>Best,</p>\
                        <p style='margin:0;'>Triviafy Support Team</p>\
                        <p style='margin:0;font-size:9px;'>Reply 'stop' to unsubscribe.</p>"
        # ------------------------ check if email+subject already sent today start ------------------------
        db_email_sent_obj = EmailSentObj.query.filter_by(to_email=output_to_email, subject=output_subject).first()
        if db_email_sent_obj != None and db_email_sent_obj != []:
          localhost_print_function(f'email already sent to this {output_to_email} - {output_subject}')
          continue
        # ------------------------ check if email+subject already sent today end ------------------------
        else:
          send_email_template_function(output_to_email, output_subject, output_body)
          # ------------------------ send email end ------------------------
          # ------------------------ insert email to db start ------------------------
          new_row = EmailSentObj(
            id = create_uuid_function('progress_'),
            created_timestamp = create_timestamp_function(),
            from_user_id_fk = current_user.id,
            to_email = output_to_email,
            subject = output_subject,
            body = output_body
          )
          db.session.add(new_row)
          db.session.commit()
          # ------------------------ insert email to db end ------------------------
      return redirect(url_for('admin_views_interior.admin_analytics_page_function', url_redirect_code='s7'))
    # ------------------------ SendTryEmployeesEmails end ------------------------
    # ------------------------ SendCollectedEmailsTryProduct start ------------------------
    status_email_hit = request.form.get('SendCollectedEmailsTryProduct')
    if status_email_hit == 'all':
      for i_email in page_dict['landing_collect_emails_arr']:
        # ------------------------ send email start ------------------------
        guessed_name = breakup_email_function(i_email)
        output_to_email = i_email
        output_subject = f"Your Recognition {todays_date_str}"
        output_body = f"<p>Hi {guessed_name},</p>\
                        <p>As someone who is always looking for new and exciting ways to build strong teams and advance your career, I want to introduce you to Triviafy - the leading team building software platform that is taking the corporate world by storm.</p>\
                        <p>With Triviafy, you'll gain access to a vast array of team-building activities that will help you engage with your colleagues, build stronger relationships, and ultimately, advance your career. With features such as trivia games, picture quizzes, icebreakers, birthday games, personality tests, employee surveys, and daily questionnaires, Triviafy provides a unique and fun way to bond with your team. The best part is that all team-building activities are asynchronous!</p>\
                        <p>But that's not all. By using Triviafy, you'll also get exposure within your company and increase your chances of getting that promotion you've been working towards. With higher employee engagement metrics and improved collaboration, your managers will see you as a standout performer and someone who is committed to the success of the team.</p>\
                        <p>Don't just take my word for it - give Triviafy a try and see for yourself how it can help you achieve your career goals. Sign up today and start building stronger relationships with your colleagues while advancing your career.</p>\
                        <p>Thank you for considering Triviafy.</p>\
                        <p style='margin:0;'>Best,</p>\
                        <p style='margin:0;'>Triviafy Support Team</p>\
                        <p style='margin:0;font-size:9px;'>Reply 'stop' to unsubscribe.</p>"
        # ------------------------ check if email+subject already sent today start ------------------------
        db_email_sent_obj = EmailSentObj.query.filter_by(to_email=output_to_email, subject=output_subject).first()
        if db_email_sent_obj != None and db_email_sent_obj != []:
          localhost_print_function(f'email already sent to this {output_to_email} - {output_subject}')
          continue
        # ------------------------ check if email+subject already sent today end ------------------------
        else:
          send_email_template_function(output_to_email, output_subject, output_body)
          # ------------------------ send email end ------------------------
          # ------------------------ insert email to db start ------------------------
          new_row = EmailSentObj(
            id = create_uuid_function('collected_'),
            created_timestamp = create_timestamp_function(),
            from_user_id_fk = current_user.id,
            to_email = output_to_email,
            subject = output_subject,
            body = output_body
          )
          db.session.add(new_row)
          db.session.commit()
          # ------------------------ insert email to db end ------------------------
      return redirect(url_for('admin_views_interior.admin_analytics_page_function', url_redirect_code='s7'))
    # ------------------------ SendCollectedEmailsTryProduct end ------------------------
    # ------------------------ ScrapedEmailsTryProduct start ------------------------
    status_email_hit = request.form.get('ScrapedEmailsTryProduct')
    if status_email_hit == 'all':
      for i_email in page_dict['scraped_emails_arr']:
        # ------------------------ send email start ------------------------
        guessed_name = breakup_email_function(i_email)
        output_to_email = i_email
        output_subject = f"Your Recognition {todays_date_str}"
        output_body = f"<p>Hi {guessed_name},</p>\
                        <p>As someone who is always looking for new and exciting ways to build strong teams and advance your career, I want to introduce you to Triviafy - the leading team building software platform that is taking the corporate world by storm.</p>\
                        <p>With Triviafy, you'll gain access to a vast array of team-building activities that will help you engage with your colleagues, build stronger relationships, and ultimately, advance your career. With features such as trivia games, picture quizzes, icebreakers, birthday games, personality tests, employee surveys, and daily questionnaires, Triviafy provides a unique and fun way to bond with your team. The best part is that all team-building activities are asynchronous!</p>\
                        <p>But that's not all. By using Triviafy, you'll also get exposure within your company and increase your chances of getting that promotion you've been working towards. With higher employee engagement metrics and improved collaboration, your managers will see you as a standout performer and someone who is committed to the success of the team.</p>\
                        <p>Don't just take my word for it - give Triviafy a try and see for yourself how it can help you achieve your career goals. Sign up today and start building stronger relationships with your colleagues while advancing your career.</p>\
                        <p>Thank you for considering Triviafy.</p>\
                        <p style='margin:0;'>Best,</p>\
                        <p style='margin:0;'>Triviafy Support Team</p>\
                        <p style='margin:0;font-size:9px;'>Reply 'stop' to unsubscribe.</p>"
        # ------------------------ check if email+subject already sent today start ------------------------
        db_email_sent_obj = EmailSentObj.query.filter_by(to_email=output_to_email, subject=output_subject).first()
        if db_email_sent_obj != None and db_email_sent_obj != []:
          localhost_print_function(f'email already sent to this {output_to_email} - {output_subject}')
          continue
        # ------------------------ check if email+subject already sent today end ------------------------
        else:
          send_email_template_function(output_to_email, output_subject, output_body)
          # ------------------------ send email end ------------------------
          # ------------------------ insert email to db start ------------------------
          new_row = EmailSentObj(
            id = create_uuid_function('collected_'),
            created_timestamp = create_timestamp_function(),
            from_user_id_fk = current_user.id,
            to_email = output_to_email,
            subject = output_subject,
            body = output_body
          )
          db.session.add(new_row)
          db.session.commit()
          # ------------------------ insert email to db end ------------------------
      return redirect(url_for('admin_views_interior.admin_analytics_page_function', url_redirect_code='s7'))
    # ------------------------ ScrapedEmailsTryProduct end ------------------------
  # ------------------------ post method end ------------------------
  return render_template('admin_page/analytics/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------
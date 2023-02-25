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
from website.models import EmployeesGroupQuestionsUsedObj, EmployeesGroupSettingsObj, EmployeesGroupsObj, EmployeesTestsGradedObj, EmployeesTestsObj, UserObj, CandidatesAssessmentGradedObj, CandidatesAssessmentsCreatedObj, CandidatesScheduleObj, CandidatesUploadedCandidatesObj, StripeCheckoutSessionObj, DeletedEmailsObj
import os
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
from website.backend.candidates.sql_statements.sql_statements_select_general_v1_jobs import select_general_v1_jobs_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
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
  localhost_print_function(' ------------------------ admin_dashboard_page_function start ------------------------ ')
  # ------------------------ ensure correct email start ------------------------
  if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
    return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e9'))
  # ------------------------ ensure correct email end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  localhost_print_function(' ------------------------ admin_dashboard_page_function end ------------------------ ')
  return render_template('admin_page/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@admin_views_interior.route('/admin/d', methods=['GET', 'POST'])
@admin_views_interior.route('/admin/d/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def admin_delete_page_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ admin_delete_page_function start ------------------------ ')
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
      EmployeesGroupQuestionsUsedObj.query.filter_by(fk_group_id=group_to_delete).delete()
      EmployeesGroupSettingsObj.query.filter_by(fk_group_id=group_to_delete).delete()
      EmployeesGroupsObj.query.filter_by(public_group_id=group_to_delete).delete()
      EmployeesTestsGradedObj.query.filter_by(fk_group_id=group_to_delete).delete()
      EmployeesTestsObj.query.filter_by(fk_group_id=group_to_delete).delete()
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
      EmployeesTestsGradedObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
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
      # ------------------------ delete from candidates tables start ------------------------
      try:
        CandidatesAssessmentGradedObj.query.filter_by(created_assessment_user_id_fk=db_users_dict['id']).delete()
        CandidatesAssessmentsCreatedObj.query.filter_by(user_id_fk=db_users_dict['id']).delete()
        CandidatesScheduleObj.query.filter_by(user_id_fk=db_users_dict['id']).delete()
        CandidatesUploadedCandidatesObj.query.filter_by(user_id_fk=db_users_dict['id']).delete()
      except:
        pass
      # ------------------------ delete from candidates tables end ------------------------
      # ------------------------ delete from employees tables start ------------------------
      db_all_users_obj = UserObj.query.filter_by(company_name=db_users_dict['company_name']).all()
      if len(db_all_users_obj) == 1:
        # ------------------------ if user is the only one from company start ------------------------
        try:
          db_group_obj = EmployeesGroupsObj.query.filter_by(fk_company_name=db_users_dict['company_name']).all()
          for i_group_obj in db_group_obj:
            db_group_dict = arr_of_dict_all_columns_single_item_function(i_group_obj)
            group_to_delete = db_group_dict['public_group_id']
            EmployeesGroupQuestionsUsedObj.query.filter_by(fk_group_id=group_to_delete).delete()
            EmployeesGroupSettingsObj.query.filter_by(fk_group_id=group_to_delete).delete()
            EmployeesGroupsObj.query.filter_by(public_group_id=group_to_delete).delete()
            EmployeesTestsGradedObj.query.filter_by(fk_group_id=group_to_delete).delete()
            EmployeesTestsObj.query.filter_by(fk_group_id=group_to_delete).delete()
        except:
          pass
        # ------------------------ if user is the only one from company end ------------------------
      # ------------------------ delete from employees tables end ------------------------
      elif len(db_all_users_obj) > 1:
        try:
          db_group_obj = EmployeesGroupsObj.query.filter_by(fk_company_name=db_users_dict['company_name']).all()
          for i_group_obj in db_group_obj:
            db_group_dict = arr_of_dict_all_columns_single_item_function(i_group_obj)
            group_to_delete = db_group_dict['public_group_id']
            EmployeesTestsGradedObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
        except:
          pass
      # ------------------------ delete from user table start ------------------------
      StripeCheckoutSessionObj.query.filter_by(fk_user_id=db_users_dict['id']).delete()
      UserObj.query.filter_by(id=db_users_dict['id']).delete()
      # ------------------------ add unique removed email to db start ------------------------
      try:
        new_row = DeletedEmailsObj(
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
      redis_candidates_deleted_counter = 0
      for key in redis_keys:
        if 'bcooke' in str(key):
          value = redis_connection.get(key).decode('utf-8')
          if value not in user_ids_set:
            redis_connection.delete(key)
            redis_candidates_deleted_counter += 1
      localhost_print_function(f'redis_candidates_deleted_counter: {redis_candidates_deleted_counter}')
      # ------------------------ loop through redis end ------------------------
      postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
      # ------------------------ delete from redis end ------------------------
      return redirect(url_for('admin_views_interior.admin_delete_page_function', url_redirect_code='w1'))
    # ------------------------ DeleteRedisDeletedCookies end ------------------------
  localhost_print_function(' ------------------------ admin_delete_page_function end ------------------------ ')
  return render_template('admin_page/delete/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@admin_views_interior.route('/admin/a', methods=['GET', 'POST'])
@admin_views_interior.route('/admin/a/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def admin_analytics_page_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ admin_analytics_page_function start ------------------------ ')
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
  db_groups_obj = EmployeesGroupsObj.query.all()
  # ------------------------ loop groups start ------------------------
  for i_group_obj in db_groups_obj:
    # ------------------------ new i_dict start ------------------------
    i_dict = {}
    i_dict['group_progress'] = 'no tests yet'
    # ------------------------ new i_dict end ------------------------
    i_group_dict = arr_of_dict_all_columns_single_item_function(i_group_obj)
    i_dict['company_name'] = i_group_dict['fk_company_name']
    i_dict['public_group_id'] = i_group_dict['public_group_id']
    i_dict['created_timestamp'] = i_group_dict['created_timestamp']
    # ------------------------ total users start ------------------------
    db_all_users_obj = UserObj.query.filter_by(company_name=i_group_dict['fk_company_name']).all()
    i_dict['total_users_with_same_company_name'] = len(db_all_users_obj)
    # ------------------------ total users end ------------------------
    # ------------------------ latest test start ------------------------
    db_latest_test_obj = EmployeesTestsObj.query.filter_by(fk_group_id=i_group_dict['public_group_id']).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
    i_dict['latest_test_id'] = None
    i_dict['latest_test_participation'] = 0
    try:
      i_dict['latest_test_id'] = db_latest_test_obj.id
      # ------------------------ latest test graded start ------------------------
      try:
        db_latest_test_graded_obj = EmployeesTestsGradedObj.query.filter_by(fk_group_id=i_group_dict['public_group_id'], status='complete').all()
        i_dict['latest_test_participation'] = len(db_latest_test_graded_obj)
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
  if request.method == 'POST':
    pass
  localhost_print_function(' ------------------------ admin_analytics_page_function end ------------------------ ')
  return render_template('admin_page/analytics/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import re
from website.models import CandidatesUploadedCandidatesObj
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.models import EmployeesGroupSettingsObj, EmployeesTestsObj
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
from website import db
from website.backend.candidates.datetime_manipulation import get_current_weekday_function, get_current_hour_function, get_upcoming_date_function, build_out_datetime_from_parts_function
import os, time
# ------------------------ imports end ------------------------


localhost_print_function(' ------------------------ user_inputs __init__ start ------------------------ ')
# ------------------------ Set Timezone START ------------------------
# Set the timezone of the application when user creates account is will be in US/Easterm time
os.environ['TZ'] = 'US/Eastern'
time.tzset()
# ------------------------ Set Timezone END ------------------------
# ------------------------ individual function start ------------------------
def create_quiz_function(group_id, immediate=False):
  localhost_print_function(' ------------------------ create_quiz_function start ------------------------ ')
  # ------------------------ Set Timezone START ------------------------
  # Set the timezone of the application when user creates account is will be in US/Easterm time
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  # ------------------------ Set Timezone END ------------------------
  # ------------------------ pull group settings start ------------------------
  db_group_settings_obj = EmployeesGroupSettingsObj.query.filter_by(fk_group_id=group_id).order_by(EmployeesGroupSettingsObj.created_timestamp.desc()).first()
  db_group_settings_dict = arr_of_dict_all_columns_single_item_function(db_group_settings_obj)
  # ------------------------ pull group settings end ------------------------
  # ------------------------ pull latest tests check start ------------------------
  correct_cadence = False
  db_tests_obj = EmployeesTestsObj.query.filter_by(fk_group_id=db_group_settings_dict['fk_group_id']).order_by(EmployeesTestsObj.created_timestamp.desc()).all()
  if db_tests_obj == None or db_tests_obj == []:
    correct_cadence = True
  else:
    # ------------------------ update correct_cadence based on previous two quizzes start ------------------------
    # <- - - - - Code to be added
    # ------------------------ update correct_cadence based on previous two quizzes end ------------------------
    pass
  # ------------------------ pull latest tests check end ------------------------
  # ------------------------ create quiz start ------------------------
  if correct_cadence == True:
    # ------------------------ if quiz to be made immediately (first quiz) start ------------------------
    if immediate == True:
      db_group_settings_dict['start_day'] = get_current_weekday_function()
      db_group_settings_dict['start_time'] = get_current_hour_function()  # will return current hour in EST
    # ------------------------ if quiz to be made immediately (first quiz) end ------------------------
    # ------------------------ construct start/end timestamps start ------------------------
    start_date_str = get_upcoming_date_function(db_group_settings_dict['start_day'])
    end_date_str = get_upcoming_date_function(db_group_settings_dict['end_day'])
    start_timestamp_created = build_out_datetime_from_parts_function(start_date_str, db_group_settings_dict['start_time'], db_group_settings_dict['timezone'])
    if immediate == True:
      start_timestamp_created = build_out_datetime_from_parts_function(start_date_str, db_group_settings_dict['start_time'], 'EST')
    end_timestamp_created = build_out_datetime_from_parts_function(end_date_str, db_group_settings_dict['end_time'], db_group_settings_dict['timezone'])
    # ------------------------ construct start/end timestamps end ------------------------
    # ------------------------ insert to db start ------------------------
    try:
      new_row = EmployeesTestsObj(
        id = create_uuid_function('test_'),
        created_timestamp = create_timestamp_function(),
        fk_group_id = db_group_settings_dict['fk_group_id'],
        timezone = db_group_settings_dict['timezone'],
        start_day = db_group_settings_dict['start_day'],
        start_time = db_group_settings_dict['start_time'],
        start_timestamp = start_timestamp_created,
        end_day = db_group_settings_dict['end_day'],
        end_time = db_group_settings_dict['end_time'],
        end_timestamp = end_timestamp_created,
        total_questions = db_group_settings_dict['total_questions'],
        question_type = db_group_settings_dict['question_type'],
        categories = db_group_settings_dict['categories'],
        question_ids = 'tbd',
        status = 'Open'
      )
      # db.session.add(new_row)
      # db.session.commit()
    except:
      pass
    # ------------------------ insert to db end ------------------------
  # ------------------------ create quiz end ------------------------
  localhost_print_function(' ------------------------ create_quiz_function end ------------------------ ')
  return False
# ------------------------ individual function end ------------------------
localhost_print_function(' ------------------------ user_inputs __init__ end ------------------------ ')
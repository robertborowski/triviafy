# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import re
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.models import EmployeesGroupSettingsObj, EmployeesTestsObj, EmployeesGroupQuestionsUsedObj
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
from website import db
from website.backend.candidates.datetime_manipulation import get_current_weekday_function, get_current_hour_function, get_upcoming_date_function, build_out_datetime_from_parts_function
import os, time
from website.backend.candidates.sql_statements.sql_prep import prepare_where_clause_function
# ------------------------ imports end ------------------------


localhost_print_function(' ------------------------ quiz __init__ start ------------------------ ')

# ------------------------ Set Timezone START ------------------------
# Set the timezone of the application when user creates account is will be in US/Easterm time
os.environ['TZ'] = 'US/Eastern'
time.tzset()
# ------------------------ Set Timezone END ------------------------

# ------------------------ individual function start ------------------------
def build_question_type_arr_function(input_type, input_total_questions):
  localhost_print_function(' ------------------------ build_question_type_arr_function start ------------------------ ')
  input_total_questions = int(input_total_questions)
  options_arr = ['Fill in the blank', 'Multiple choice', 'Mixed']
  question_types_arr = []
  counter=0
  while counter < input_total_questions:
    counter+=1
    if input_type == options_arr[0]:
      question_types_arr.append(options_arr[0])
    if input_type == options_arr[1]:
      question_types_arr.append(options_arr[1])
    if input_type == options_arr[2]:
      if counter % 2 == 0:
        question_types_arr.append(options_arr[1])
      else:
        question_types_arr.append(options_arr[0])
  question_types_str = ','.join(question_types_arr)
  localhost_print_function(' ------------------------ build_question_type_arr_function end ------------------------ ')
  return question_types_str
# ------------------------ individual function end ------------------------

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
    localhost_print_function(' ------------- 0 ------------- ')
    localhost_print_function('Need to check cadence before creating new test')
    localhost_print_function(' ------------- 0 ------------- ')
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
    start_timestamp_created = build_out_datetime_from_parts_function(start_date_str, db_group_settings_dict['start_time'], db_group_settings_dict['timezone'])    # converted to EST for job runs
    if immediate == True:
      start_timestamp_created = build_out_datetime_from_parts_function(start_date_str, db_group_settings_dict['start_time'], 'EST')
    end_timestamp_created = build_out_datetime_from_parts_function(end_date_str, db_group_settings_dict['end_time'], db_group_settings_dict['timezone'])    # converted to EST for job runs
    # ------------------------ construct start/end timestamps end ------------------------
    # ------------------------ pull question id's start ------------------------
    final_uuids_arr = []
    where_clause_str = None
    where_clause_arr = prepare_where_clause_function(db_group_settings_dict['categories'])
    where_clause_str = where_clause_arr[0]
    query_result_arr_of_dicts = select_general_function('select_all_questions_for_x_categories_v4', where_clause_str, db_group_settings_dict['total_questions'], db_group_settings_dict['fk_group_id'])
    for i in query_result_arr_of_dicts:
      final_uuids_arr.append(i['id'])
    remainder_questions_needed = db_group_settings_dict['total_questions'] - len(query_result_arr_of_dicts)
    if remainder_questions_needed > 0:
      # ------------------------ exclude wip id's start ------------------------
      exclude_where_clause = '/* AND id NOT IN () */'
      wip_question_ids_arr = []
      for i in query_result_arr_of_dicts:
        i_id = "'" + i['id'] + "'"
        wip_question_ids_arr.append(i_id)
      if len(wip_question_ids_arr) == 0:
        pass
      else:
        in_string = ','.join(wip_question_ids_arr)
        exclude_where_clause = 'AND id NOT IN (' + in_string + ')'
      # ------------------------ exclude wip id's end ------------------------
      # ------------------------ second pull if remainder start ------------------------
      query_result_arr_of_dicts_remainder = select_general_function('select_all_questions_for_x_categories_v5', remainder_questions_needed, db_group_settings_dict['fk_group_id'], exclude_where_clause)
      for i in query_result_arr_of_dicts_remainder:
        final_uuids_arr.append(i['id'])
      # ------------------------ second pull if remainder end ------------------------
    final_uuids_str = ','.join(final_uuids_arr)
    # ------------------------ pull question id's end ------------------------
    # ------------------------ question type order start ------------------------
    question_types_str = build_question_type_arr_function(db_group_settings_dict['question_type'], db_group_settings_dict['total_questions'])
    # ------------------------ question type order end ------------------------
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
        question_ids = final_uuids_str,
        question_types_order = question_types_str,
        status = 'Open'
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ insert to db end ------------------------
    # ------------------------ insert to db start ------------------------
    for i in final_uuids_arr:
      try:
        new_row = EmployeesGroupQuestionsUsedObj(
          id = create_uuid_function('used_'),
          created_timestamp = create_timestamp_function(),
          fk_group_id = db_group_settings_dict['fk_group_id'],
          fk_question_id = i
        )
        db.session.add(new_row)
        db.session.commit()
      except:
        pass
    # ------------------------ insert to db end ------------------------
  # ------------------------ create quiz end ------------------------
  localhost_print_function(' ------------------------ create_quiz_function end ------------------------ ')
  return True
# ------------------------ individual function end ------------------------
localhost_print_function(' ------------------------ quiz __init__ end ------------------------ ')
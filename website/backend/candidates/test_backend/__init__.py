# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import re
from website.models import UserObj, ActivityATestGradedObj, ActivityATestObj, GroupObj, ActivityAGroupQuestionsUsedObj, ActivityBTestObj
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
from datetime import datetime
from website import db
from website.backend.candidates.quiz import create_quiz_function_v2
from website.backend.candidates.datetime_manipulation import convert_timestamp_to_month_day_string_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_test_winner(input_test_id, result_id=False):
  # ------------------------ check if test is closed start ------------------------
  db_tests_obj = ActivityATestObj.query.filter_by(id=input_test_id).first()
  if db_tests_obj.status == 'Closed':
    # ------------------------ check if test is closed end ------------------------
    # ------------------------ assign variables start ------------------------
    current_max_final_score = float(0)
    current_max_final_score_user_id = 'No participation'
    latest_test_winner_score = float(0)
    latest_test_winner = 'No participation'
    # ------------------------ assign variables end ------------------------
    # ------------------------ pull winner start ------------------------
    db_test_grading_obj = ActivityATestGradedObj.query.filter_by(fk_test_id=input_test_id, status='complete').order_by(ActivityATestGradedObj.created_timestamp.asc()).all()
    for i_obj in db_test_grading_obj:
      i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
      i_final_score = float(i_dict['final_score'])
      if i_final_score > current_max_final_score:
        current_max_final_score = i_final_score
        current_max_final_score_user_id = i_dict['fk_user_id']
        latest_test_winner_score = float(i_final_score) * float(100)
    if current_max_final_score_user_id != 'No participation':
      db_user_obj = UserObj.query.filter_by(id=current_max_final_score_user_id).first()
      latest_test_winner_email = db_user_obj.email
      # ------------------------ clean winner email start ------------------------
      latest_test_winner_email_arr = latest_test_winner_email.split('@')
      latest_test_winner = latest_test_winner_email_arr[0]
      # ------------------------ clean winner email end ------------------------
    # ------------------------ pull winner end ------------------------
    # ------------------------ specific call start ------------------------
    if result_id == True:
      return current_max_final_score_user_id, latest_test_winner_score
    # ------------------------ specific call end ------------------------
    return latest_test_winner, latest_test_winner_score
  else:
    return 'Quiz not yet closed', 'Quiz not yet closed'
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def first_user_first_quiz_check_function(company_name):
  check_first_user_first_quiz_can_replace = False
  try:
    user_group_id = GroupObj.query.filter_by(fk_company_name=company_name).order_by(GroupObj.created_timestamp.desc()).first()
    fufq_check_test_count_obj = ActivityATestObj.query.filter_by(fk_group_id=user_group_id.public_group_id,product='trivia').all()
    if len(fufq_check_test_count_obj) == 1:
      fufq_check_test_graded_count_obj = ActivityATestGradedObj.query.filter_by(fk_group_id=user_group_id.public_group_id,product='trivia').all()
      # ------------------------ check if none start ------------------------
      if fufq_check_test_graded_count_obj == None or fufq_check_test_graded_count_obj == []:
        check_first_user_first_quiz_can_replace = True
      # ------------------------ check if none end ------------------------
      # ------------------------ check if at least 1 person from team already completed start ------------------------
      at_least_one_test_completed = False
      for i_obj in fufq_check_test_graded_count_obj:
        if i_obj.status == 'complete':
          at_least_one_test_completed = True
      if at_least_one_test_completed == False:
        check_first_user_first_quiz_can_replace = True
      # ------------------------ check if at least 1 person from team already completed end ------------------------
  except:
    pass
  return check_first_user_first_quiz_can_replace
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def first_user_latest_quiz_check_function(current_user, url_activity_code):
  check_first_user_latest_quiz_can_replace = False
  # ------------------------ latest objs start ------------------------
  user_test_obj = ActivityATestObj.query.filter_by(fk_group_id=current_user.group_id,product=url_activity_code).order_by(ActivityATestObj.created_timestamp.desc()).first()
  user_test_graded_obj = ActivityATestGradedObj.query.filter_by(fk_group_id=current_user.group_id, fk_test_id=user_test_obj.id, status='complete',product=url_activity_code).all()
  # ------------------------ latest objs end ------------------------
  # ------------------------ check if none completed yet start ------------------------
  if user_test_graded_obj == None or user_test_graded_obj == []:
    check_first_user_latest_quiz_can_replace = True
  # ------------------------ check if none completed yet end ------------------------
  return check_first_user_latest_quiz_can_replace
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def close_historical_activity_tests_function(current_user, activity_name, activity_type):
  # ------------------------ ensure all historical tests are closed start ------------------------
  historical_activity_tests_were_closed = False
  current_datetime_str = datetime.now().strftime("%m/%d/%Y %H:%M:%S")   # str
  current_datetime_datetime = datetime.strptime(current_datetime_str, "%m/%d/%Y %H:%M:%S")  # datetime
  db_tests_obj = None
  if activity_type == 'activity_type_a':
    db_tests_obj = ActivityATestObj.query.filter_by(fk_group_id=current_user.group_id,product=activity_name).order_by(ActivityATestObj.created_timestamp.desc()).all()
  elif activity_type == 'activity_type_b':
    db_tests_obj = ActivityBTestObj.query.filter_by(fk_group_id=current_user.group_id,product=activity_name).order_by(ActivityBTestObj.created_timestamp.desc()).all()
  try:
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
          historical_activity_tests_were_closed = True
    if historical_activity_tests_were_closed == True:
      db.session.commit()
  except:
    pass
  # ------------------------ ensure all historical tests are closed end ------------------------
  return historical_activity_tests_were_closed
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def delete_historical_activity_a_tests_no_participation_function(current_user, activity_name, page_dict):
  # ------------------------ delete all historical closed tests with 'No participation' start ------------------------
  historical_activity_a_tests_were_deleted = False
  db_historical_tests_obj = ActivityATestObj.query.filter_by(fk_group_id=current_user.group_id, status='Closed',product=activity_name).order_by(ActivityATestObj.created_timestamp.desc()).all()
  try:
    if db_historical_tests_obj != None and db_historical_tests_obj != []:
      for i_historical_test_obj in db_historical_tests_obj:
        i_historical_test_dict = arr_of_dict_all_columns_single_item_function(i_historical_test_obj)
        # ------------------------ winner start ------------------------
        page_dict[activity_name+'_latest_winner'], page_dict[activity_name+'_latest_winner_score'] = get_test_winner(i_historical_test_dict['id'])
        # ------------------------ winner end ------------------------
        # ------------------------ delete histoical no participation start ------------------------
        if page_dict[activity_name+'_latest_winner'] == 'No participation':
          ActivityAGroupQuestionsUsedObj.query.filter_by(fk_test_id=i_historical_test_dict['id']).delete()
          ActivityATestGradedObj.query.filter_by(fk_test_id=i_historical_test_dict['id']).delete()
          ActivityATestObj.query.filter_by(id=i_historical_test_dict['id']).delete()
          historical_activity_a_tests_were_deleted = True
          db.session.commit()
        # ------------------------ delete histoical no participation end ------------------------
      # ------------------------ redirect start ------------------------
      if historical_activity_a_tests_were_deleted == True:
        db.session.commit()
      # ------------------------ redirect end ------------------------
  except:
    pass
  # ------------------------ delete all historical closed tests with 'No participation' end ------------------------
  return historical_activity_a_tests_were_deleted, page_dict
# ------------------------ individual function end ------------------------
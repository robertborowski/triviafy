# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import re
from website.models import UserObj, EmployeesTestsGradedObj, EmployeesTestsObj, EmployeesGroupsObj
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== test_backend __init__ START ===========================================')
# ------------------------ individual function start ------------------------
def get_test_winner(input_test_id, result_id=False):
  localhost_print_function(' ------------------------ get_test_winner start ------------------------ ')
  # ------------------------ check if test is closed start ------------------------
  db_tests_obj = EmployeesTestsObj.query.filter_by(id=input_test_id).first()
  if db_tests_obj.status == 'Closed':
    # ------------------------ check if test is closed end ------------------------
    # ------------------------ assign variables start ------------------------
    current_max_final_score = float(0)
    current_max_final_score_user_id = 'No participation'
    latest_test_winner_score = float(0)
    latest_test_winner = 'No participation'
    # ------------------------ assign variables end ------------------------
    # ------------------------ pull winner start ------------------------
    db_test_grading_obj = EmployeesTestsGradedObj.query.filter_by(fk_test_id=input_test_id, status='complete').order_by(EmployeesTestsGradedObj.created_timestamp.asc()).all()
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
      localhost_print_function(' ------------------------ get_test_winner end ------------------------ ')
      return current_max_final_score_user_id, latest_test_winner_score
    # ------------------------ specific call end ------------------------
    localhost_print_function(' ------------------------ get_test_winner end ------------------------ ')
    return latest_test_winner, latest_test_winner_score
  else:
    localhost_print_function(' ------------------------ get_test_winner end ------------------------ ')
    return 'Quiz not yet closed', 'Quiz not yet closed'
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def first_user_first_quiz_check_function(company_name):
  localhost_print_function(' ------------------------ first_user_first_quiz_check_function start ------------------------ ')
  check_first_user_first_quiz_can_replace = False
  try:
    user_group_id = EmployeesGroupsObj.query.filter_by(fk_company_name=company_name).order_by(EmployeesGroupsObj.created_timestamp.desc()).first()
    fufq_check_test_count_obj = EmployeesTestsObj.query.filter_by(fk_group_id=user_group_id.public_group_id).all()
    if len(fufq_check_test_count_obj) == 1:
      fufq_check_test_graded_count_obj = EmployeesTestsGradedObj.query.filter_by(fk_group_id=user_group_id.public_group_id).all()
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
  localhost_print_function(' ------------------------ first_user_first_quiz_check_function end ------------------------ ')
  return check_first_user_first_quiz_can_replace
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def first_user_latest_quiz_check_function(company_name):
  localhost_print_function(' ------------------------ first_user_latest_quiz_check_function start ------------------------ ')
  check_first_user_latest_quiz_can_replace = False
  # ------------------------ latest objs start ------------------------
  user_group_id = EmployeesGroupsObj.query.filter_by(fk_company_name=company_name).order_by(EmployeesGroupsObj.created_timestamp.desc()).first()
  user_test_obj = EmployeesTestsObj.query.filter_by(fk_group_id=user_group_id.public_group_id).order_by(EmployeesTestsObj.created_timestamp.desc()).first()
  user_test_graded_obj = EmployeesTestsGradedObj.query.filter_by(fk_group_id=user_group_id.public_group_id, fk_test_id=user_test_obj.id, status='complete').all()
  # ------------------------ latest objs end ------------------------
  # ------------------------ check if none completed yet start ------------------------
  if user_test_graded_obj == None or user_test_graded_obj == []:
    check_first_user_latest_quiz_can_replace = True
  # ------------------------ check if none completed yet end ------------------------
  localhost_print_function(' ------------------------ first_user_latest_quiz_check_function end ------------------------ ')
  return check_first_user_latest_quiz_can_replace
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== test_backend __init__ END ===========================================')
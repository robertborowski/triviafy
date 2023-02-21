# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import re
from website.models import UserObj, EmployeesTestsGradedObj
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== test_backend __init__ START ===========================================')
# ------------------------ individual function start ------------------------
def get_test_winner(input_test_id, result_id=False):
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
    return current_max_final_score_user_id, latest_test_winner_score
  # ------------------------ specific call end ------------------------
  return latest_test_winner, latest_test_winner_score
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== test_backend __init__ END ===========================================')
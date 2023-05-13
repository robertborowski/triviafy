# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.candidates.pull_create_logic import pull_create_activity_a_settings_obj_function, pull_latest_activity_a_test_obj_function, pull_latest_activity_a_test_graded_obj_function
from website.backend.candidates.test_backend import get_test_winner, close_historical_activity_a_tests_function, delete_historical_activity_a_tests_no_participation_function
from website.backend.candidates.datetime_manipulation import convert_timestamp_to_month_day_string_function
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
from website.backend.candidates.quiz import get_next_quiz_open_function, compare_candence_vs_previous_quiz_function_v2
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def activity_a_dashboard_function(current_user, page_dict, activity_name):
  redirect_code = None
  # ------------------------ pull/create group settings activities start ------------------------
  db_activity_settings_obj = pull_create_activity_a_settings_obj_function(current_user, activity_name)
  # categories fix
  db_activity_settings_dict = arr_of_dict_all_columns_single_item_function(db_activity_settings_obj)
  categories_edit = db_activity_settings_dict['categories'].replace(',',', ')
  db_activity_settings_dict['categories'] = categories_edit
  page_dict[activity_name+'_settings_dict'] = db_activity_settings_dict
  # ------------------------ pull/create group settings activities end ------------------------
  # ------------------------ ensure all historical tests are closed start ------------------------
  historical_activity_a_tests_were_closed = close_historical_activity_a_tests_function(current_user, activity_name)
  if historical_activity_a_tests_were_closed == True:
    return 'dashboard', page_dict
  # ------------------------ ensure all historical tests are closed end ------------------------
  # ------------------------ delete all historical closed tests with 'No participation' start ------------------------
  historical_activity_a_tests_were_deleted, page_dict = delete_historical_activity_a_tests_no_participation_function(current_user, activity_name, page_dict)
  if historical_activity_a_tests_were_deleted == True:
    return 'dashboard', page_dict
  # ------------------------ delete all historical closed tests with 'No participation' end ------------------------
  # ------------------------ pull latest test start ------------------------
  page_dict[activity_name+'_first_created'] = False
  db_tests_obj = pull_latest_activity_a_test_obj_function(current_user, activity_name)
  if db_tests_obj != None:
    page_dict[activity_name+'_first_created'] = True
  # ------------------------ pull latest test end ------------------------
  # ------------------------ latest test end time info start ------------------------
  page_dict[activity_name+'_participation_end'] = False
  page_dict[activity_name+'_participation_timeframe'] = False
  if page_dict[activity_name+'_first_created'] == True:
    start_month_day_str = convert_timestamp_to_month_day_string_function(db_tests_obj.start_timestamp)
    end_month_day_str = convert_timestamp_to_month_day_string_function(db_tests_obj.end_timestamp)
    page_dict[activity_name+'_participation_timeframe'] = start_month_day_str + ', ' + db_tests_obj.start_time + ' - ' + end_month_day_str + ', ' + db_tests_obj.end_time + ' ' + db_tests_obj.timezone
    page_dict[activity_name+'_participation_end'] = end_month_day_str + ', ' + db_tests_obj.end_time + ' ' + db_tests_obj.timezone
  # ------------------------ latest test end time info end ------------------------
  # ------------------------ pull latest graded start ------------------------
  page_dict[activity_name+'_latest_completed'] = False
  try:
    db_test_grading_obj = pull_latest_activity_a_test_graded_obj_function(db_tests_obj, current_user, activity_name)
    if db_test_grading_obj.status == 'complete':
      page_dict[activity_name+'_latest_completed'] = True
  except:
    pass
  # ------------------------ pull latest graded end ------------------------
  # ------------------------ if latest closed then pull winner start ------------------------
  page_dict[activity_name+'_latest_closed'] = False
  page_dict[activity_name+'_latest_winner'] = ''
  page_dict[activity_name+'_latest_winner_score'] = float(0)
  page_dict[activity_name+'_next_open'] = False
  try:
    db_tests_dict = arr_of_dict_all_columns_single_item_function(db_tests_obj)
    if db_tests_dict['status'] == 'Closed':
      page_dict[activity_name+'_latest_closed'] = True
    # ------------------------ winner start ------------------------
    page_dict[activity_name+'_latest_winner'], page_dict[activity_name+'_latest_winner_score'] = get_test_winner(db_tests_dict['id'])
    # ------------------------ winner end ------------------------
    # ------------------------ if latest closed then pull next quiz open datetime start ------------------------
    page_dict[activity_name+'_next_open'] = get_next_quiz_open_function(current_user.group_id, activity_name)
    # ------------------------ if latest closed then pull next quiz open datetime end ------------------------
  except:
    pass
  # ------------------------ if latest closed then pull winner end ------------------------
  # ------------------------ cadence check to see if a new activity should be created start ------------------------
  page_dict[activity_name+'_cadence_valid'] = False
  if db_tests_obj != None:
    page_dict[activity_name+'_cadence_valid'] = compare_candence_vs_previous_quiz_function_v2(current_user, db_tests_obj, activity_name)
  # ------------------------ cadence check to see if a new activity should be created end ------------------------
  return redirect_code, page_dict
# ------------------------ individual function end ------------------------
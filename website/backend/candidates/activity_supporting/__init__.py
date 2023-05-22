# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.candidates.pull_create_logic import pull_create_activity_settings_obj_function, pull_latest_activity_test_obj_function, pull_latest_activity_test_graded_obj_function
from website.backend.candidates.test_backend import get_test_winner, close_historical_activity_tests_function, delete_historical_activity_tests_no_participation_function
from website.backend.candidates.datetime_manipulation import convert_timestamp_to_month_day_string_function
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function, categories_tuple_function
from website.backend.candidates.quiz import get_next_quiz_open_function, compare_candence_vs_previous_quiz_function_v2
from website.backend.candidates.pull_create_logic import pull_create_group_obj_function
from website.models import ActivityATestObj, ActivityATestGradedObj, ActivityAGroupQuestionsUsedObj, ActivityACreatedQuestionsObj, UserObj
from website import db
from website.backend.candidates.test_backend import get_test_winner, first_user_latest_quiz_check_function
import json
from website.backend.candidates.pull_create_logic import pull_group_obj_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def activity_dashboard_function(current_user, page_dict, activity_name, activity_type):
  redirect_code = None
  # ------------------------ pull/create group settings activities start ------------------------
  db_activity_settings_obj = pull_create_activity_settings_obj_function(current_user, activity_name, activity_type)
  db_activity_settings_dict = arr_of_dict_all_columns_single_item_function(db_activity_settings_obj)
  if activity_type == 'activity_type_a':
    categories_edit = db_activity_settings_dict['categories'].replace(',',', ')
    db_activity_settings_dict['categories'] = categories_edit
  page_dict[activity_name+'_settings_dict'] = db_activity_settings_dict
  # ------------------------ pull/create group settings activities end ------------------------
  # ------------------------ ensure all historical tests are closed start ------------------------
  historical_activity_tests_were_closed = close_historical_activity_tests_function(current_user, activity_name, activity_type)
  if historical_activity_tests_were_closed == True:
    return 'dashboard', page_dict
  # ------------------------ ensure all historical tests are closed end ------------------------
  # ------------------------ delete all historical closed tests with 'No participation' start ------------------------
  historical_activity_tests_were_deleted, page_dict = delete_historical_activity_tests_no_participation_function(current_user, activity_name, page_dict, activity_type)
  if historical_activity_tests_were_deleted == True:
    return 'dashboard', page_dict
  # ------------------------ delete all historical closed tests with 'No participation' end ------------------------
  # ------------------------ pull latest test start ------------------------
  page_dict[activity_name+'_first_created'] = False
  db_tests_obj = pull_latest_activity_test_obj_function(current_user, activity_name, activity_type)
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
    db_test_grading_obj = pull_latest_activity_test_graded_obj_function(db_tests_obj, current_user, activity_name, activity_type)
    if db_test_grading_obj.status == 'complete':
      page_dict[activity_name+'_latest_completed'] = True
  except:
    pass
  # ------------------------ pull latest graded end ------------------------
  # ------------------------ if latest closed then pull winner start ------------------------
  if activity_type == 'activity_type_a':
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
    page_dict[activity_name+'_cadence_valid'] = compare_candence_vs_previous_quiz_function_v2(current_user, db_tests_obj, activity_name, activity_type)
  # ------------------------ cadence check to see if a new activity should be created end ------------------------
  # ------------------------ get group activity status start ------------------------
  db_group_obj = pull_create_group_obj_function(current_user)
  db_group_dict = arr_of_dict_all_columns_single_item_function(db_group_obj)
  page_dict[activity_name+'_on_off_status'] = db_group_dict[activity_name]
  # ------------------------ get group activity status end ------------------------
  return redirect_code, page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def activity_a_live_function(page_dict, current_user, url_test_id, url_question_number, url_initial_page_load, url_activity_code):
  page_dict['latest_test_id'] = url_test_id
  # ------------------------ redirect to latest test id start ------------------------
  if url_test_id == None:
    db_tests_obj = ActivityATestObj.query.filter_by(fk_group_id=current_user.group_id,product=url_activity_code).order_by(ActivityATestObj.created_timestamp.desc()).first()
    if db_tests_obj == None or db_tests_obj == []:
      return page_dict, 'no_activity'
    else:
      page_dict['latest_test_id'] = db_tests_obj.id
      return page_dict, 'init_activity'
  # ------------------------ redirect to latest test id end ------------------------
  # ------------------------ first user first quiz delete logic start ------------------------
  page_dict['first_user_latest_quiz_can_replace'] = first_user_latest_quiz_check_function(current_user, url_activity_code)
  if url_test_id == 'fufq_remove':
    if page_dict['first_user_latest_quiz_can_replace'] == True:
      check_latest_test_obj = ActivityATestObj.query.filter_by(fk_group_id=current_user.group_id,product=url_activity_code).order_by(ActivityATestObj.created_timestamp.desc()).first()
      ActivityATestObj.query.filter_by(id=check_latest_test_obj.id).delete()
      ActivityATestGradedObj.query.filter_by(fk_test_id=check_latest_test_obj.id).delete()
      ActivityAGroupQuestionsUsedObj.query.filter_by(fk_test_id=check_latest_test_obj.id).delete()
      db.session.commit()
      return page_dict, 'replace_activity'
  # ------------------------ first user first quiz delete logic end ------------------------
  # ------------------------ on initial page load - redirect to first unanswered question start ------------------------
  # ------------------------ pull latest graded start ------------------------
  if url_initial_page_load == 'init':
    db_test_grading_obj = ActivityATestGradedObj.query.filter_by(fk_test_id=url_test_id, fk_user_id=current_user.id, status='wip',product=url_activity_code).first()
    try:
      db_test_grading_dict = arr_of_dict_all_columns_single_item_function(db_test_grading_obj)
      # ------------------------ pull latest graded end ------------------------
      # ------------------------ pull question left off on initial load only start ------------------------
      unanswered_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
      for i in json.loads(db_test_grading_dict['test_obj']):
        already_answered_question_number = str(i['question_number'])
        if already_answered_question_number in unanswered_arr:
          unanswered_arr.remove(already_answered_question_number)
      if str(url_question_number) != unanswered_arr[0]:
        page_dict['earliest_unanswered_question_number'] = unanswered_arr[0]
        return page_dict, 'redirect_earliest_unanswered'
      # ------------------------ pull question left off on initial load only end ------------------------
    except:
      pass
  # ------------------------ on initial page load - redirect to first unanswered question end ------------------------
  # ------------------------ pull test id start ------------------------
  db_tests_obj = ActivityATestObj.query.filter_by(id=url_test_id).first()
  if db_tests_obj == None or db_tests_obj == []:
    return page_dict, 'no_activity'
  # ------------------------ pull test id end ------------------------
  # ------------------------ validate question number start ------------------------
  total_questions = int(db_tests_obj.total_questions)
  try:
    url_question_number = int(url_question_number)
  except:
    return page_dict, 'correct_redirect'
  if url_question_number > total_questions or url_question_number < 1:
    return page_dict, 'correct_redirect'
  # ------------------------ validate question number end ------------------------
  # ------------------------ pull specific question id start ------------------------
  question_ids_str = db_tests_obj.question_ids
  question_ids_arr = question_ids_str.split(',')
  desired_question_id = question_ids_arr[url_question_number-1]
  # ------------------------ pull specific question id end ------------------------
  # ------------------------ pull question from db start ------------------------
  db_question_obj = ActivityACreatedQuestionsObj.query.filter_by(id=desired_question_id).first()
  db_question_dict = arr_of_dict_all_columns_single_item_function(db_question_obj, for_json_dumps=True)
  # ------------------------ append question type start ------------------------
  question_type_order_str = db_tests_obj.question_types_order
  question_type_order_arr = question_type_order_str.split(',')
  desired_question_type = question_type_order_arr[url_question_number-1]
  db_question_dict['desired_question_type'] = desired_question_type
  # ------------------------ append question type end ------------------------
  page_dict['activity_type'] = url_activity_code
  page_dict['db_question_dict'] = db_question_dict
  # ------------------------ pull question from db end ------------------------
  # ------------------------ fix categories presentation start ------------------------
  page_dict['db_question_dict']['categories'] = categories_tuple_function(page_dict['db_question_dict']['categories'])
  # ------------------------ fix categories presentation end ------------------------
  # ------------------------ pull user info start ------------------------
  page_dict['user_company_name'] = current_user.company_name
  # ------------------------ pull user info end ------------------------
  # ------------------------ question order logic start ------------------------
  page_dict['current_question_number'] = str(int(url_question_number))
  page_dict['next_question_number'] = str(int(url_question_number) + 1)
  page_dict['previous_question_number'] = str(int(url_question_number) - 1)
  if int(db_tests_obj.total_questions) == int(url_question_number):
    page_dict['next_question_number'] = 'submit'
  # ------------------------ question order logic end ------------------------
  # ------------------------ test variables start ------------------------
  page_dict['test_total_questions'] = db_tests_obj.total_questions
  test_total_questions_arr = []
  for i in range(int(db_tests_obj.total_questions)):
    test_total_questions_arr.append(str(i+1))
  page_dict['test_total_questions_arr'] = test_total_questions_arr
  page_dict['url_test_id'] = url_test_id
  # ------------------------ test variables end ------------------------
  # ------------------------ contains image check start ------------------------
  contains_img = False
  if 'amazonaws.com' in page_dict['db_question_dict']['aws_image_url']:
    contains_img = True
  page_dict['question_contains_image'] = contains_img
  # ------------------------ contains image check end ------------------------
  # ------------------------ redirect variables start ------------------------
  page_dict['db_question_dict']['redirect_ui_answer'] = ''
  page_dict['latest_test_completed'] = False
  try:
    db_test_grading_obj = ActivityATestGradedObj.query.filter_by(fk_test_id=url_test_id, fk_user_id=current_user.id,product=url_activity_code).first()
    db_test_grading_dict = arr_of_dict_all_columns_single_item_function(db_test_grading_obj)
    master_answer_arr_of_dict = json.loads(db_test_grading_dict['test_obj'])
    for i in master_answer_arr_of_dict:
      if int(i['question_number']) == int(url_question_number):
        page_dict['db_question_dict']['redirect_ui_answer'] = i['ui_answer']
    if db_test_grading_dict['status'] == 'complete':
      page_dict['latest_test_completed'] = True
  except:
    pass
  # ------------------------ redirect variables end ------------------------
  # ------------------------ archive logic start ------------------------
  page_dict['view_as_archive'] = False
  try:
    if db_tests_obj.status == 'Closed':
      page_dict['view_as_archive'] = True
      # ------------------------ get teammate answers start ------------------------
      teammate_answers_tuple = []
      db_test_grading_obj = ActivityATestGradedObj.query.filter_by(fk_test_id=url_test_id,product=url_activity_code).all()
      for i_obj in db_test_grading_obj:
        db_user_obj = UserObj.query.filter_by(id=i_obj.fk_user_id).first()
        users_master_test_results_arr_of_dict = json.loads(i_obj.test_obj)
        for i_dict in users_master_test_results_arr_of_dict:
          i_question_number = i_dict['question_number']
          if int(i_question_number) == int(url_question_number):
            i_ui_answer = i_dict['ui_answer']
            i_ui_answer_is_correct = i_dict['ui_answer_is_correct']
            # ------------------------ capitalize mcq answer start ------------------------
            if len(i_ui_answer) == 1:
              i_ui_answer = i_ui_answer.upper()
            # ------------------------ capitalize mcq answer end ------------------------
            # ------------------------ shorten email start ------------------------
            i_email = db_user_obj.email
            i_email_arr = i_email.split('@')
            i_email = i_email_arr[0]
            if len(i_email) > 15:
              i_email = i_email[0:15]
            # ------------------------ shorten email end ------------------------
            teammate_answers_tuple.append((i_email, i_ui_answer, i_ui_answer_is_correct))
            break
      page_dict['teammate_answers_tuple'] = teammate_answers_tuple
      # ------------------------ get teammate answers end ------------------------
  except:
    pass
  # ------------------------ archive logic end ------------------------
  return page_dict, True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def turn_activity_auto_on_function(current_user, url_activity_code):
  # ------------------------ turn on auto start stop start ------------------------
  try:
    on_off_change_occured = False
    db_group_obj = pull_group_obj_function(current_user)
    if url_activity_code in db_group_obj.__table__.columns:
      if getattr(db_group_obj, url_activity_code) != True:
        setattr(db_group_obj, url_activity_code, True)
        on_off_change_occured = True
    if on_off_change_occured == True:
      db.session.commit()
  except:
    pass
  # ------------------------ turn on auto start stop end ------------------------
  return True
# ------------------------ individual function end ------------------------
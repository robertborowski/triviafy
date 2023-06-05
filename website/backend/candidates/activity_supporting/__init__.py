# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.candidates.pull_create_logic import pull_create_activity_settings_obj_function, pull_latest_activity_test_obj_function, pull_latest_activity_test_graded_obj_function
from website.backend.candidates.test_backend import get_test_winner, close_historical_activity_tests_function, delete_historical_activity_tests_no_participation_function
from website.backend.candidates.datetime_manipulation import convert_timestamp_to_month_day_string_function
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function, categories_tuple_function, construct_time_presentation_function
from website.backend.candidates.quiz import get_next_quiz_open_function, compare_candence_vs_previous_quiz_function_v2
from website.backend.candidates.pull_create_logic import pull_create_group_obj_function
from website.models import ActivityATestObj, ActivityATestGradedObj, ActivityAGroupQuestionsUsedObj, ActivityACreatedQuestionsObj, UserObj, ActivityBTestObj, ActivityBTestGradedObj, ActivityBGroupQuestionsUsedObj, ActivityBCreatedQuestionsObj, UserCelebrateObj
from website import db
from website.backend.candidates.test_backend import get_test_winner, first_user_latest_quiz_check_function
import json
from website.backend.candidates.pull_create_logic import pull_group_obj_function
from datetime import datetime, date
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def activity_dashboard_function(current_user, page_dict, url_activity_code, url_activity_type):
  redirect_code = None
  # ------------------------ pull/create group settings activities start ------------------------
  db_activity_settings_obj = pull_create_activity_settings_obj_function(current_user, url_activity_code, url_activity_type)
  db_activity_settings_dict = arr_of_dict_all_columns_single_item_function(db_activity_settings_obj)
  if url_activity_type == 'activity_type_a':
    categories_edit = db_activity_settings_dict['categories'].replace(',',', ')
    db_activity_settings_dict['categories'] = categories_edit
  page_dict[url_activity_code+'_settings_dict'] = db_activity_settings_dict
  # ------------------------ pull/create group settings activities end ------------------------
  # ------------------------ ensure all historical tests are closed start ------------------------
  historical_activity_tests_were_closed = close_historical_activity_tests_function(current_user, url_activity_code, url_activity_type)
  if historical_activity_tests_were_closed == True:
    return 'dashboard', page_dict
  # ------------------------ ensure all historical tests are closed end ------------------------
  # ------------------------ delete all historical closed tests with 'No participation' start ------------------------
  historical_activity_tests_were_deleted, page_dict = delete_historical_activity_tests_no_participation_function(current_user, url_activity_code, page_dict, url_activity_type)
  if historical_activity_tests_were_deleted == True:
    return 'dashboard', page_dict
  # ------------------------ delete all historical closed tests with 'No participation' end ------------------------
  # ------------------------ pull latest test start ------------------------
  page_dict[url_activity_code+'_first_created'] = False
  db_tests_obj = pull_latest_activity_test_obj_function(current_user, url_activity_code, url_activity_type)
  if db_tests_obj != None:
    page_dict[url_activity_code+'_first_created'] = True
  # ------------------------ pull latest test end ------------------------
  # ------------------------ latest test end time info start ------------------------
  page_dict[url_activity_code+'_participation_end'] = False
  page_dict[url_activity_code+'_participation_timeframe'] = False
  if page_dict[url_activity_code+'_first_created'] == True:
    start_month_day_str = convert_timestamp_to_month_day_string_function(db_tests_obj.start_timestamp)
    end_month_day_str = convert_timestamp_to_month_day_string_function(db_tests_obj.end_timestamp)
    page_dict[url_activity_code+'_participation_timeframe'] = start_month_day_str + ', ' + db_tests_obj.start_time + ' - ' + end_month_day_str + ', ' + db_tests_obj.end_time + ' ' + db_tests_obj.timezone
    page_dict[url_activity_code+'_participation_end'] = end_month_day_str + ', ' + db_tests_obj.end_time + ' ' + db_tests_obj.timezone
  # ------------------------ latest test end time info end ------------------------
  # ------------------------ pull latest graded start ------------------------
  page_dict[url_activity_code+'_latest_completed'] = False
  try:
    db_test_grading_obj = pull_latest_activity_test_graded_obj_function(db_tests_obj, current_user, url_activity_code, url_activity_type)
    if db_test_grading_obj.status == 'complete':
      page_dict[url_activity_code+'_latest_completed'] = True
  except:
    pass
  # ------------------------ pull latest graded end ------------------------
  # ------------------------ if latest closed then pull winner start ------------------------
  page_dict[url_activity_code+'_latest_closed'] = False
  page_dict[url_activity_code+'_next_open'] = False
  try:
    page_dict[url_activity_code+'_next_open'] = get_next_quiz_open_function(current_user, url_activity_code, url_activity_type)
  except:
    pass
  if url_activity_type == 'activity_type_a':
    page_dict[url_activity_code+'_latest_winner'] = ''
    page_dict[url_activity_code+'_latest_winner_score'] = float(0)
  try:
    db_tests_dict = arr_of_dict_all_columns_single_item_function(db_tests_obj)
    if db_tests_dict['status'] == 'Closed':
      page_dict[url_activity_code+'_latest_closed'] = True
    if url_activity_type == 'activity_type_a':
      # ------------------------ winner start ------------------------
      page_dict[url_activity_code+'_latest_winner'], page_dict[url_activity_code+'_latest_winner_score'] = get_test_winner(db_tests_dict['id'])
      # ------------------------ winner end ------------------------
  except:
    pass
  # ------------------------ if latest closed then pull winner end ------------------------
  # ------------------------ cadence check to see if a new activity should be created start ------------------------
  page_dict[url_activity_code+'_cadence_valid'] = False
  if db_tests_obj != None:
    page_dict[url_activity_code+'_cadence_valid'] = compare_candence_vs_previous_quiz_function_v2(current_user, db_tests_obj, url_activity_code, url_activity_type)
  # ------------------------ cadence check to see if a new activity should be created end ------------------------
  # ------------------------ get group activity status start ------------------------
  db_group_obj = pull_create_group_obj_function(current_user)
  db_group_dict = arr_of_dict_all_columns_single_item_function(db_group_obj)
  page_dict[url_activity_code+'_on_off_status'] = db_group_dict[url_activity_code]
  # ------------------------ get group activity status end ------------------------
  return redirect_code, page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def activity_live_function(page_dict, current_user, url_test_id, url_question_number, url_initial_page_load, url_activity_code, url_activity_type):
  page_dict['latest_test_id'] = url_test_id
  page_dict['url_activity_type'] = url_activity_type
  page_dict['url_activity_code'] = url_activity_code
  page_dict['user_company_name'] = current_user.company_name
  # ------------------------ redirect to latest test id start ------------------------
  if url_test_id == None:
    db_tests_obj = pull_latest_activity_test_obj_function(current_user, url_activity_code, url_activity_type)
    if db_tests_obj == None or db_tests_obj == []:
      return page_dict, 'no_activity'
    else:
      page_dict['latest_test_id'] = db_tests_obj.id
      return page_dict, 'init_activity'
  # ------------------------ redirect to latest test id end ------------------------
  # ------------------------ first user first quiz delete logic start ------------------------
  db_tests_obj = pull_latest_activity_test_obj_function(current_user, url_activity_code, url_activity_type)
  page_dict['first_user_latest_quiz_can_replace'] = first_user_latest_quiz_check_function(current_user, db_tests_obj, url_activity_code, url_activity_type)
  page_dict['current_test_end_str'] = construct_time_presentation_function(db_tests_obj, 'end', 'v1')
  if url_test_id == 'fufq_remove':
    if page_dict['first_user_latest_quiz_can_replace'] == True:
      if url_activity_type == 'activity_type_a':
        ActivityATestObj.query.filter_by(id=db_tests_obj.id).delete()
        ActivityATestGradedObj.query.filter_by(fk_test_id=db_tests_obj.id).delete()
        ActivityAGroupQuestionsUsedObj.query.filter_by(fk_test_id=db_tests_obj.id).delete()
      elif url_activity_type == 'activity_type_b':
        ActivityBTestObj.query.filter_by(id=db_tests_obj.id).delete()
        ActivityBTestGradedObj.query.filter_by(fk_test_id=db_tests_obj.id).delete()
        ActivityBGroupQuestionsUsedObj.query.filter_by(fk_test_id=db_tests_obj.id).delete()
      db.session.commit()
      return page_dict, 'replace_activity'
  # ------------------------ first user first quiz delete logic end ------------------------
  # ------------------------ on initial page load - redirect to first unanswered question start ------------------------
  if url_activity_type == 'activity_type_a':
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
  # ------------------------ pull test obj start ------------------------
  db_tests_obj = None
  if url_activity_type == 'activity_type_a':
    db_tests_obj = ActivityATestObj.query.filter_by(id=url_test_id).first()
  elif url_activity_type == 'activity_type_b':
    db_tests_obj = ActivityBTestObj.query.filter_by(id=url_test_id).first()
  if db_tests_obj == None or db_tests_obj == []:
    return page_dict, 'no_activity'
  # ------------------------ pull test obj end ------------------------
  # ------------------------ activity_type_b start ------------------------
  if url_activity_type == 'activity_type_b':
    page_dict['latest_question_id'] = db_tests_obj.fk_question_id
    db_question_obj = ActivityBCreatedQuestionsObj.query.filter_by(id=page_dict['latest_question_id']).first()
    db_question_dict = arr_of_dict_all_columns_single_item_function(db_question_obj, for_json_dumps=True)
    page_dict['db_question_dict'] = db_question_dict
  # ------------------------ activity_type_b end ------------------------
  # ------------------------ additional activity_type_a logic start ------------------------
  if url_activity_type == 'activity_type_a':
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
    page_dict['db_question_dict'] = db_question_dict
    # ------------------------ pull question from db end ------------------------
    # ------------------------ fix categories presentation start ------------------------
    page_dict['db_question_dict']['categories'] = categories_tuple_function(page_dict['db_question_dict']['categories'])
    # ------------------------ fix categories presentation end ------------------------
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
  # ------------------------ additional activity_type_a logic end ------------------------
  # ------------------------ additional activity_type_b logic start ------------------------
  elif url_activity_type == 'activity_type_b':
    # ------------------------ get users latest response start ------------------------
    page_dict['users_latest_response'] = None
    try:
      db_test_grading_obj = ActivityBTestGradedObj.query.filter_by(fk_test_id=url_test_id, fk_user_id=current_user.id).first()
      if db_test_grading_obj != None and db_test_grading_obj != '':
        page_dict['users_latest_response'] = db_test_grading_obj.test_obj
    except:
      pass
    # ------------------------ get users latest response end ------------------------
  # ------------------------ additional activity_type_b logic end ------------------------
  # ------------------------ archive logic start ------------------------
  page_dict['view_as_archive'] = False
  page_dict['teammate_responses_dict'] = False
  try:
    if db_tests_obj.status == 'Closed':
      page_dict['view_as_archive'] = True
      page_dict['current_test_end_str'] = construct_time_presentation_function(db_tests_obj, 'end', 'v1')
      # ------------------------ get teammate answers activity_type_a start ------------------------
      if url_activity_type == 'activity_type_a':
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
              i_name = db_user_obj.name
              if len(i_name) > 15:
                i_name = i_name[0:15]
              # ------------------------ shorten email end ------------------------
              teammate_answers_tuple.append((i_name, i_ui_answer, i_ui_answer_is_correct))
              break
        page_dict['teammate_answers_tuple'] = teammate_answers_tuple
      # ------------------------ get teammate answers activity_type_a end ------------------------
      # ------------------------ get teammate answers activity_type_b start ------------------------
      if url_activity_type == 'activity_type_b':
        teammate_responses_dict = {}
        db_test_grading_obj = ActivityBTestGradedObj.query.filter_by(fk_test_id=url_test_id,product=url_activity_code).all()
        i_obj_counter = -1
        for i_obj in db_test_grading_obj:
          i_obj_counter += 1
          teammate_responses_dict['user_'+str(i_obj_counter)] = {}
          teammate_responses_dict['user_'+str(i_obj_counter)]['fk_user_id'] = i_obj.fk_user_id
          teammate_responses_dict['user_'+str(i_obj_counter)]['test_obj'] = i_obj.test_obj
          db_user_obj = UserObj.query.filter_by(id=i_obj.fk_user_id).first()
          teammate_responses_dict['user_'+str(i_obj_counter)]['name'] = db_user_obj.name
          teammate_responses_dict['user_'+str(i_obj_counter)]['email'] = db_user_obj.email
        page_dict['teammate_responses_dict'] = teammate_responses_dict
      # ------------------------ get teammate answers activity_type_b end ------------------------
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

# ------------------------ individual function start ------------------------
def get_all_teammate_ids_function(current_user):
  teammate_ids_arr = []
  db_teammates_obj = UserObj.query.filter_by(group_id=current_user.group_id).all()
  for i_obj in db_teammates_obj:
    teammate_ids_arr.append(i_obj.id)
  return teammate_ids_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def check_if_teammate_celebration_function(teammate_ids_arr):
  teammate_completed_check = False
  for i in teammate_ids_arr:
    db_celebrate_obj = UserCelebrateObj.query.filter_by(fk_user_id=i).first()
    if db_celebrate_obj != None and db_celebrate_obj != []:
      teammate_completed_check = True
      break
  return teammate_completed_check
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_upcoming_celebration_function(teammate_ids_arr, page_dict):
  # ------------------------ get todays variables start ------------------------
  today = date.today()    # <class 'datetime.date'> | 2023-06-03
  current_day = today.day
  current_month = today.month
  current_year = today.year
  minimum_date = date(int(2100), int(12), int(1))
  # ------------------------ get todays variables end ------------------------
  # ------------------------ loop checks start ------------------------
  for i in teammate_ids_arr:
    # ------------------------ pull variables start ------------------------
    db_celebrate_obj = UserCelebrateObj.query.filter_by(fk_user_id=i).all()
    if db_celebrate_obj != None and db_celebrate_obj != []:
      for i_celebrate_obj in db_celebrate_obj:
        i_celebrate_month = int(i_celebrate_obj.celebrate_month)
        i_celebrate_day = int(i_celebrate_obj.celebrate_day)
        i_celebrate_year = int(current_year)
        if i_celebrate_month < current_month:
          i_celebrate_year = int(current_year) + int(1)
        # ------------------------ pull variables end ------------------------
        # ------------------------ construct date start ------------------------
        upcoming_date = date(i_celebrate_year, i_celebrate_month, i_celebrate_day)
        # ------------------------ construct date end ------------------------
        # ------------------------ compare dates and replace/append arr start ------------------------
        if upcoming_date < minimum_date:
          minimum_date = upcoming_date
        # ------------------------ compare dates and replace/append arr end ------------------------
  # ------------------------ loop checks end ------------------------
  # ------------------------ check today start ------------------------
  page_dict['celebrations_are_today'] = False
  if minimum_date == today:
    page_dict['celebrations_are_today'] = True
  # ------------------------ check today end ------------------------
  # ------------------------ get all users with min date start ------------------------
  min_day = minimum_date.day    # int
  min_month = minimum_date.month    # int
  min_year = minimum_date.year    # int
  teammate_ids_str = "'" + "','".join(teammate_ids_arr) + "'"
  query_result_arr_of_dicts = select_general_function('select_celebrations_v1', teammate_ids_str, min_month, min_day)
  master_str = ''
  for i_dict in query_result_arr_of_dicts:
    db_user_obj = UserObj.query.filter_by(id=i_dict['fk_user_id']).first()
    i_dict['name'] = db_user_obj.name
    i_dict['email'] = db_user_obj.email
    if i_dict['event'] == 'birthday':
      if master_str == '':
        master_str = master_str + f"{i_dict['name']}'s birthday on {min_month}/{min_day}/{min_year}"
      else:
        master_str = master_str + f" & {i_dict['name']}'s birthday on {min_month}/{min_day}/{min_year}"
    if i_dict['event'] == 'job_start_date':
      if master_str == '':
        master_str = master_str + f"{i_dict['name']}'s company anniversary on {min_month}/{min_day}/{min_year}"
      else:
        master_str = master_str + f" & {i_dict['name']}'s company anniversary on {min_month}/{min_day}/{min_year}"
  # ------------------------ get all users with min date end ------------------------
  page_dict['celebrations_upcoming_str'] = master_str
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_todays_celebration_function(current_user, teammate_ids_arr, page_dict):
  # ------------------------ get todays variables start ------------------------
  today = date.today()    # <class 'datetime.date'> | 2023-06-03
  current_day = today.day
  current_month = today.month
  current_year = today.year
  # ------------------------ get todays variables end ------------------------
  # ------------------------ pull all teammates start ------------------------
  teammates_arr_of_dict = []
  db_teammates_obj = UserObj.query.filter_by(group_id=current_user.group_id).all()
  for i_obj in db_teammates_obj:
    i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
    teammates_arr_of_dict.append(i_dict)
  # ------------------------ pull all teammates end ------------------------
  # ------------------------ pull todays celebrations start ------------------------
  teammate_ids_str = "'" + "','".join(teammate_ids_arr) + "'"
  celebrations_today_arr_of_dicts = select_general_function('select_celebrations_v1', teammate_ids_str, current_month, current_day)
  # ------------------------ pull todays celebrations end ------------------------
  # ------------------------ data for table start ------------------------
  for i_celebrate_dict in celebrations_today_arr_of_dicts:
    for i_user_dict in teammates_arr_of_dict:
      if i_celebrate_dict['fk_user_id'] == i_user_dict['id']:
        i_celebrate_dict['name'] = i_user_dict['name']
    if i_celebrate_dict['event'] == 'birthday':
      i_celebrate_dict['event_str'] = i_celebrate_dict['name'] + "'s birthday is today, click here to participate! "
    if i_celebrate_dict['event'] == 'job_start_date':
      i_celebrate_dict['event_str'] = i_celebrate_dict['name'] + "'s company anniversary is today, click here to participate! "
  page_dict['celebrations_today_arr_of_dicts'] = celebrations_today_arr_of_dicts
  # ------------------------ data for table end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def dashboard_celebrations_function(current_user, page_dict):
  redirect_code = None
  # ------------------------ check if at least 1 user celebration question/answer participation start ------------------------
  teammate_ids_arr = get_all_teammate_ids_function(current_user)
  teammate_completed_check = check_if_teammate_celebration_function(teammate_ids_arr)
  # ------------------------ check if at least 1 user celebration question/answer participation start ------------------------
  # ------------------------ get group activity status start ------------------------
  db_group_obj = pull_create_group_obj_function(current_user)
  # ------------------------ submit new group activity status start ------------------------
  if db_group_obj.celebrations == False and teammate_completed_check == True:
    db_group_obj.celebrations = True
    db.session.commit()
    return 'dashboard', page_dict
  if db_group_obj.celebrations == True and teammate_completed_check == False:
    db_group_obj.celebrations = False
    db.session.commit()
    return 'dashboard', page_dict
  # ------------------------ submit new group activity status end ------------------------
  db_group_dict = arr_of_dict_all_columns_single_item_function(db_group_obj)
  page_dict['celebrations_on_off_status'] = db_group_dict['celebrations']
  # ------------------------ get group activity status end ------------------------
  if page_dict['celebrations_on_off_status'] == True:
    # ------------------------ get upcoming celebration start ------------------------
    page_dict = get_upcoming_celebration_function(teammate_ids_arr, page_dict)
    # ------------------------ get upcoming celebration end ------------------------
    # ------------------------ get todays celebrations start ------------------------
    if page_dict['celebrations_are_today'] == True:
      page_dict = get_todays_celebration_function(current_user, teammate_ids_arr, page_dict)
    # ------------------------ get todays celebrations end ------------------------
  return redirect_code, page_dict
# ------------------------ individual function end ------------------------
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
import re
import difflib
from datetime import datetime, date
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== dict_manipulation __init__ START ===========================================')
# ------------------------ individual function start ------------------------
def question_arr_of_dicts_manipulations_function(input_arr_of_dicts):
  localhost_print_function('=========================================== dict_arr_of_dicts_question_manipulations_function START ===========================================')
  question_counter = 0
  for i_dict in input_arr_of_dicts:
    # ------------------------ question counter start ------------------------
    question_counter += 1
    i_dict['question_counter'] = question_counter
    # ------------------------ question counter end ------------------------
    # ------------------------ question categories str to arr tuple start ------------------------
    try:
      # Assign variables
      categories_str = i_dict['categories']
      categories_str_fixed = categories_str.replace(', ',',')
      categories_arr = categories_str_fixed.split(',')
      # Loop and separate
      categories_arr_to_html = []
      for category in categories_arr:
        if category == 'Candidates' or category == 'MCQ':
          continue
        category_lower = category.lower()
        category_replace_space = category_lower.replace(' ','_')
        category_strip = category_replace_space.strip()
        # ------------------------ special characters start ------------------------
        if category_strip == 'c#':
          category_strip = 'csharp'
        if category_strip == 'c++':
          category_strip = 'cpp'
        # ------------------------ special characters end ------------------------
        categories_arr_to_html.append((category, category_strip))
      i_dict['categories'] = categories_arr_to_html
    except:
      print('Error here: question_arr_of_dicts_manipulations_function except statement...')
      return False
    # ------------------------ question categories str to arr tuple end ------------------------
  localhost_print_function('=========================================== dict_arr_of_dicts_question_manipulations_function END ===========================================')
  return input_arr_of_dicts
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def categories_tuple_function(input_categories):
  localhost_print_function('=========================================== dict_arr_of_dicts_question_manipulations_function START ===========================================')
  categories_arr_to_html = []
  try:
    # Assign variables
    categories_str = input_categories.replace(', ',',')
    categories_arr = categories_str.split(',')
    # Loop and separate
    for category in categories_arr:
      if category == 'Candidates' or category == 'MCQ':
        continue
      category_lower = category.lower()
      category_replace_space = category_lower.replace(' ','_')
      category_strip = category_replace_space.strip()
      # ------------------------ special characters start ------------------------
      if category_strip == 'c#':
        category_strip = 'csharp'
      if category_strip == 'c++':
        category_strip = 'cpp'
      # ------------------------ special characters end ------------------------
      categories_arr_to_html.append((category, category_strip))
  except:
    print('Error here: question_arr_of_dicts_manipulations_function except statement...')
    return False
  # ------------------------ question categories str to arr tuple end ------------------------
  localhost_print_function('=========================================== dict_arr_of_dicts_question_manipulations_function END ===========================================')
  return categories_arr_to_html
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_assessment_info_dict_function(db_assessment_obj):
  localhost_print_function('=========================================== create_assessment_info_dict_function START ===========================================')
  # ------------------------ init dict start ------------------------
  assessment_info_dict = {}
  # ------------------------ init dict end ------------------------
  # ------------------------ assign dict start ------------------------
  assessment_info_dict['id'] =  db_assessment_obj.id
  assessment_info_dict['name'] = db_assessment_obj.assessment_name
  assessment_info_dict['desired_languages_arr'] = db_assessment_obj.desired_languages_arr
  assessment_info_dict['total_questions'] =  db_assessment_obj.total_questions
  # ------------------------ assign dict end ------------------------
  # ------------------------ assign dict questions start ------------------------
  question_ids_str =  db_assessment_obj.question_ids_arr
  question_ids_arr = question_ids_str.split(',')
  question_ids_str = "','".join(question_ids_arr)
  question_ids_str = "'" + question_ids_str + "'"
  query_result_arr_of_dicts = select_general_function('select_specific_assessment_questions_v2', additional_input=question_ids_str)
  query_result_arr_of_dicts = question_arr_of_dicts_manipulations_function(query_result_arr_of_dicts)
  assessment_info_dict['questions_arr_of_dicts'] = query_result_arr_of_dicts
  # ------------------------ assign dict questions end ------------------------
  localhost_print_function('=========================================== create_assessment_info_dict_function END ===========================================')
  return assessment_info_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_assessment_info_dict_function_v2(db_assessment_obj, url_question_number):
  localhost_print_function('=========================================== create_assessment_info_dict_function_v2 START ===========================================')
  # ------------------------ init dict start ------------------------
  assessment_info_dict = {}
  # ------------------------ init dict end ------------------------
  # ------------------------ assign dict start ------------------------
  assessment_info_dict['id'] =  db_assessment_obj.id
  assessment_info_dict['name'] = db_assessment_obj.assessment_name
  assessment_info_dict['desired_languages_arr'] = db_assessment_obj.desired_languages_arr
  assessment_info_dict['total_questions'] =  db_assessment_obj.total_questions
  # ------------------------ assign dict end ------------------------
  # ------------------------ assign dict questions start ------------------------
  question_ids_str =  db_assessment_obj.question_ids_arr
  question_ids_arr = question_ids_str.split(',')
  search_for_question_index = int(url_question_number) - 1
  desired_question_id = question_ids_arr[search_for_question_index]
  desired_question_id_str = "'" + desired_question_id + "'"
  query_result_arr_of_dicts = select_general_function('select_specific_assessment_questions_v3', additional_input=desired_question_id_str)
  query_result_arr_of_dicts = question_arr_of_dicts_manipulations_function(query_result_arr_of_dicts)
  query_result_arr_of_dicts[0]['question_counter'] = url_question_number
  assessment_info_dict['question_details_dict'] = query_result_arr_of_dicts[0]
  # ------------------------ assign dict questions end ------------------------
  localhost_print_function('=========================================== create_assessment_info_dict_function_v2 END ===========================================')
  return assessment_info_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_question_info_dict_function(db_question_obj):
  localhost_print_function('=========================================== create_assessment_info_dict_function_v2 START ===========================================')
  # ------------------------ init dict start ------------------------
  question_info_dict = {}
  # ------------------------ init dict end ------------------------
  # ------------------------ assign dict questions start ------------------------
  desired_question_id_str = "'" + db_question_obj.id + "'"
  query_result_arr_of_dicts = select_general_function('select_specific_assessment_questions_v3', additional_input=desired_question_id_str)
  query_result_arr_of_dicts = question_arr_of_dicts_manipulations_function(query_result_arr_of_dicts)
  question_info_dict = query_result_arr_of_dicts[0]
  # ------------------------ assign dict questions end ------------------------
  localhost_print_function('=========================================== create_assessment_info_dict_function_v2 END ===========================================')
  return question_info_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def map_user_answers_to_questions_dict_function(assessment_info_dict, ui_current_answer_choice_selected, current_question_number):
  localhost_print_function('=========================================== map_user_answers_to_questions_dict_function START ===========================================')
  for i_dict in assessment_info_dict['questions_arr_of_dicts']:
    question_counter = i_dict['question_counter']
    if question_counter == current_question_number:
      i_dict['ui_answer'] = ui_current_answer_choice_selected
  localhost_print_function('=========================================== map_user_answers_to_questions_dict_function END ===========================================')
  return assessment_info_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def backend_store_question_answers_dict_function(assessment_info_dict):
  localhost_print_function('=========================================== backend_store_question_answers_dict_function START ===========================================')
  backend_store_question_answers_dict = {}
  for i_dict in assessment_info_dict['questions_arr_of_dicts']:
    backend_store_question_answers_dict[i_dict['id']] = i_dict['answer']
  localhost_print_function('=========================================== backend_store_question_answers_dict_function END ===========================================')
  return backend_store_question_answers_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def question_dict_clean_input_function(input_phrase):
  # localhost_print_function('=========================================== question_dict_clean_input_function START ===========================================')
  input_phrase = input_phrase.lower()
  input_phrase = input_phrase.strip()
  input_phrase = re.sub(' +', ' ',input_phrase)
  # localhost_print_function('=========================================== question_dict_clean_input_function END ===========================================')
  return input_phrase
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def check_two_phrase_similarity_score_function(correct_answer, ui_answer):
  # localhost_print_function('=========================================== check_two_phrase_similarity_score_function START ===========================================')
  answer_match_score = 0
  try:
    answer_match_score = difflib.SequenceMatcher(None, correct_answer, ui_answer).ratio()*100
  except:
    pass
  # localhost_print_function('=========================================== check_two_phrase_similarity_score_function END ===========================================')
  return answer_match_score
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def grade_assessment_answers_dict_function(assessment_info_dict):
  localhost_print_function('=========================================== grade_assessment_answers_dict_function START ===========================================')
  # ------------------------ set variables start ------------------------
  ui_total_correct_answers = 0
  # ------------------------ set variables end ------------------------
  # ------------------------ loop through questions 1 by 1 start ------------------------
  for i_dict in assessment_info_dict['questions_arr_of_dicts']:
    # ------------------------ pull what is needed start ------------------------
    question_answers_str_original = i_dict['answer']   # str
    ui_answer_original = i_dict['ui_answer']           # str
    # ------------------------ pull what is needed end ------------------------
    # ------------------------ compare answers start ------------------------
    i_dict['ui_answer_correct'] = False
    if question_answers_str_original.lower() == ui_answer_original.lower():
      i_dict['ui_answer_correct'] = True
      ui_total_correct_answers += 1
    # ------------------------ compare answers end ------------------------
    """
    # ------------------------ clean question answers start ------------------------
    question_answers_arr_original = question_answers_str_original.split(',')
    question_answers_arr_corrected = []
    for i_answer in question_answers_arr_original:
      i_answer_corrected = question_dict_clean_input_function(i_answer)
      question_answers_arr_corrected.append(i_answer_corrected)
    # ------------------------ clean question answers end ------------------------
    # ------------------------ clean user answer start ------------------------
    ui_answer_corrected = question_dict_clean_input_function(ui_answer_original)
    # ------------------------ clean user answer end ------------------------
    # ------------------------ compare answers start ------------------------
    # ------------------------ set variables start ------------------------
    current_question_max_score = 0
    i_dict['ui_answer_correct'] = False
    i_dict['ui_answer_max_score'] = 0
    # ------------------------ set variables end ------------------------
    for i_answer_corrected in question_answers_arr_corrected:
      i_score = check_two_phrase_similarity_score_function(i_answer_corrected, ui_answer_corrected)
      if i_score >= current_question_max_score:
        current_question_max_score = i_score
      if current_question_max_score >= 80:
        i_dict['ui_answer_correct'] = True
        i_dict['ui_answer_max_score'] = current_question_max_score
        ui_total_correct_answers += 1
        break
    # ------------------------ compare answers end ------------------------
    """
  # ------------------------ loop through questions 1 by 1 end ------------------------
  assessment_info_dict['ui_total_correct_answers'] = ui_total_correct_answers
  ui_final_score = (assessment_info_dict['ui_total_correct_answers'] / assessment_info_dict['total_questions'])
  assessment_info_dict['ui_final_score'] = ui_final_score
  localhost_print_function('=========================================== grade_assessment_answers_dict_function END ===========================================')
  return assessment_info_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def arr_of_dict_necessary_columns_function(sql_obj, desired_columns_arr):
  localhost_print_function('=========================================== arr_of_dict_necessary_columns_function START ===========================================')
  db_obj_arr_of_dict = []
  for i_dict in sql_obj:
    current_dict = {}
    for i_col in desired_columns_arr:
      current_dict[i_col] = getattr(i_dict, i_col)
    db_obj_arr_of_dict.append(current_dict)
  sql_obj = db_obj_arr_of_dict
  localhost_print_function('=========================================== arr_of_dict_necessary_columns_function END ===========================================')
  return sql_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def arr_of_dict_all_columns_single_item_function(sql_obj, for_json_dumps=False):
  # localhost_print_function(' ------------------------ arr_of_dict_all_columns_function START ------------------------ ')
  current_dict = {}
  for c in sql_obj.__table__.columns:
    current_value = getattr(sql_obj, c.name)
    if for_json_dumps == True:
      if isinstance(current_value, datetime):
        current_value = str(current_value)
    current_dict[c.name] = current_value
  # localhost_print_function(' ------------------------ arr_of_dict_all_columns_function END ------------------------ ')
  return current_dict
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== dict_manipulation __init__ END ===========================================')
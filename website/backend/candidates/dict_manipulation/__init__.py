# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
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
      categories_str = i_dict['question_categories_list']
      categories_str_fixed = categories_str.replace(', ',',')
      categories_arr = categories_str_fixed.split(',')
      # Loop and separate
      categories_arr_to_html = []
      for category in categories_arr:
        if category == 'Candidates':
          continue
        category_lower = category.lower()
        category_replace_space = category_lower.replace(' ','_')
        category_strip = category_replace_space.strip()
        categories_arr_to_html.append((category, category_strip))
      i_dict['question_categories_list'] = categories_arr_to_html
    except:
      print('Error here: question_arr_of_dicts_manipulations_function except statement...')
      return False
    # ------------------------ question categories str to arr tuple end ------------------------
  localhost_print_function('=========================================== dict_arr_of_dicts_question_manipulations_function END ===========================================')
  return input_arr_of_dicts
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
  assessment_info_dict['delivery_type'] =  db_assessment_obj.delivery_type
  # ------------------------ assign dict end ------------------------
  # ------------------------ assign dict questions start ------------------------
  question_ids_str =  db_assessment_obj.question_ids_arr
  question_ids_arr = question_ids_str.split(',')
  question_ids_str = "','".join(question_ids_arr)
  question_ids_str = "'" + question_ids_str + "'"
  query_result_arr_of_dicts = select_general_function('select_specific_assessment_questions', additional_input=question_ids_str)
  query_result_arr_of_dicts = question_arr_of_dicts_manipulations_function(query_result_arr_of_dicts)
  assessment_info_dict['questions_arr_of_dicts'] = query_result_arr_of_dicts
  # ------------------------ assign dict questions end ------------------------
  localhost_print_function('=========================================== create_assessment_info_dict_function END ===========================================')
  return assessment_info_dict
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== dict_manipulation __init__ END ===========================================')
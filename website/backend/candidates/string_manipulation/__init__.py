# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== string_manipulation __init__ START ===========================================')
# ------------------------ individual function start ------------------------
def string_to_arr_function(input_str):
  localhost_print_function('=========================================== string_to_arr_function START ===========================================')
  output_arr = []
  input_str_split_arr = input_str.split(',')
  for word in input_str_split_arr:
    word_stripped = word.strip()
    if word_stripped not in output_arr and word_stripped != 'Candidates' and word_stripped != 'MCQ':
      output_arr.append(word_stripped)
  localhost_print_function('=========================================== string_to_arr_function START ===========================================')
  return output_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def all_question_candidate_categories_sorted_function(query_result_arr_of_dicts):
  localhost_print_function('=========================================== all_question_candidate_categories_sorted_function START ===========================================')
  output_arr = []
  for i_dict in query_result_arr_of_dicts:
    categories_str = i_dict['question_categories_list']
    categories_arr = string_to_arr_function(categories_str)
    for i_category in categories_arr:
      if i_category not in output_arr:
        output_arr.append(i_category)
  output_arr = sorted(output_arr)
  localhost_print_function('=========================================== all_question_candidate_categories_sorted_function START ===========================================')
  return output_arr
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== string_manipulation __init__ END ===========================================')
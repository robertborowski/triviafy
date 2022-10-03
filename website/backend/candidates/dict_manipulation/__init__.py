# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== dict_manipulation __init__ START ===========================================')
# ------------------------ individual function start ------------------------
def question_arr_of_dicts_manipulations_function(input_arr_of_dicts):
  localhost_print_function('=========================================== dict_arr_of_dicts_question_manipulations_function START ===========================================')
  localhost_print_function('- - - - - - - 0 - - - - - - -')
  question_counter = 0
  for i_dict in input_arr_of_dicts:
    question_counter += 1
    i_dict['question_counter'] = question_counter
    localhost_print_function('i_dict')
    localhost_print_function(i_dict)
    localhost_print_function(type(i_dict))
    localhost_print_function(' ')
  localhost_print_function('- - - - - - - 0 - - - - - - -')
  localhost_print_function('=========================================== dict_arr_of_dicts_question_manipulations_function END ===========================================')
  return input_arr_of_dicts
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== dict_manipulation __init__ END ===========================================')
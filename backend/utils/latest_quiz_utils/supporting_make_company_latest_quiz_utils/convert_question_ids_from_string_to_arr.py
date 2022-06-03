# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def convert_question_ids_from_string_to_arr_function(quiz_question_ids_str):
  localhost_print_function('=========================================== convert_question_ids_from_string_to_arr_function START ===========================================')
  
  # Remove the beginning and ending {}
  quiz_question_ids_str_removed_brackets = quiz_question_ids_str[1:-1]

  # Split the string
  quiz_question_ids_arr = quiz_question_ids_str_removed_brackets.split(',')

  # localhost_print_function('returning quiz_question_ids_arr')
  localhost_print_function('=========================================== convert_question_ids_from_string_to_arr_function END ===========================================')
  return quiz_question_ids_arr
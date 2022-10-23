# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.candidates.string_manipulation import string_to_arr_function
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== sqlalchemy_manipulation __init__ START ===========================================')
# ------------------------ individual function start ------------------------
def pull_desired_languages_arr_function(db_obj):
  localhost_print_function('=========================================== pull_desired_languages_arr_function START ===========================================')
  output_arr = []
  for i_obj in db_obj:
    i_str = i_obj.desired_languages_str
    i_arr = string_to_arr_function(i_str)
    for i in i_arr:
      if i not in output_arr:
        output_arr.append(i)
  localhost_print_function('=========================================== pull_desired_languages_arr_function START ===========================================')
  return output_arr
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== sqlalchemy_manipulation __init__ END ===========================================')
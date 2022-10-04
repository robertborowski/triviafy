# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
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
localhost_print_function('=========================================== dict_manipulation __init__ END ===========================================')
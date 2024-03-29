# ------------------------ imports start ------------------------
from datetime import datetime
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def arr_of_dict_all_columns_single_item_function(sql_obj, for_json_dumps=False):
  current_dict = {}
  for c in sql_obj.__table__.columns:
    current_value = getattr(sql_obj, c.name)
    if for_json_dumps == True:
      if isinstance(current_value, datetime):
        current_value = str(current_value)
    current_dict[c.name] = current_value
  return current_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_answers_with_letter_choices_dict(input_arr):
  letters_arr = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
  # letters_arr = sorted(letters_arr)
  final_dict = {}
  for i in range(len(input_arr)):
    final_dict[letters_arr[i]] = input_arr[i]
  return final_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def prep_poll_dict_function(poll_dict):
  # ------------------------ separate answer choices start ------------------------
  poll_dict['answer_choices'] = poll_dict['answer_choices'].split('~')
  # ------------------------ separate answer choices end ------------------------
  # ------------------------ dict for answer + letter association start ------------------------
  poll_dict['answer_choices_dict'] = get_answers_with_letter_choices_dict(poll_dict['answer_choices'])
  # ------------------------ dict for answer + letter association end ------------------------
  return poll_dict
# ------------------------ individual function end ------------------------
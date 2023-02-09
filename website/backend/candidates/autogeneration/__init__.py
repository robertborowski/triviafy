# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import random
import string
# ------------------------ imports end ------------------------


localhost_print_function(' ------------------------ autogeneration __init__ start ------------------------ ')
# ------------------------ individual function start ------------------------
def generate_random_length_uuid_function(num_characters):
  localhost_print_function(' ------------------------ generate_random_length_uuid_function start ------------------------')
  generated_value = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(num_characters))
  localhost_print_function(' ------------------------ generate_random_length_uuid_function end ------------------------')
  return generated_value
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def question_choices_function():
  localhost_print_function(' ------------------------ question_choices_function start ------------------------')
  question_num_arr = [5,10]
  question_type_arr = ['Multiple choice','Fill in the blank','Mixed']
  localhost_print_function(' ------------------------ question_choices_function end ------------------------')
  return question_num_arr, question_type_arr
# ------------------------ individual function end ------------------------
localhost_print_function(' ------------------------ autogeneration __init__ end ------------------------ ')
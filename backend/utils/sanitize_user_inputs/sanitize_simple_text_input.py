# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import re

# -------------------------------------------------------------- Main Function
def sanitize_simple_text_input_function(user_input_form):
  localhost_print_function('=========================================== sanitize_simple_text_input_function START ===========================================')

  regex = r"\b[a-zA-Z0-9\s']{1,50}\b"

  if(re.fullmatch(regex, user_input_form)):
    try:
      user_input_form = user_input_form.strip()
      user_input_words_arr = user_input_form.split()
      user_input_form = '_'.join(user_input_words_arr)
    except:
      user_input_form = user_input_form
    localhost_print_function('=========================================== sanitize_simple_text_input_function END ===========================================')
    return user_input_form.lower()
 
  else:
    localhost_print_function('invalid form input')
    localhost_print_function('=========================================== sanitize_simple_text_input_function END ===========================================')
    return None
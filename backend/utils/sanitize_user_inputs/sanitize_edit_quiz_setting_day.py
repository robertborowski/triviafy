# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def sanitize_edit_quiz_setting_day_function(user_input_form):
  localhost_print_function('=========================================== sanitize_edit_quiz_setting_day_function START ===========================================')
  
  if (user_input_form != 'monday' and len(user_input_form) != 6) and (user_input_form != 'tuesday' and len(user_input_form) != 7) and (user_input_form != 'wednesday' and len(user_input_form) != 9) and (user_input_form != 'thursday' and len(user_input_form) != 8) and (user_input_form != 'friday' and len(user_input_form) != 6):
    localhost_print_function('=========================================== sanitize_edit_quiz_setting_day_function END ===========================================')
    return None

  localhost_print_function('=========================================== sanitize_edit_quiz_setting_day_function END ===========================================')
  return user_input_form
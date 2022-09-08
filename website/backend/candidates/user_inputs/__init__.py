# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import re
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== user_inputs __init__ START ===========================================')

# ------------------------ individual function start ------------------------
def sanitize_email_function(user_input_email):
  localhost_print_function('=========================================== sanitize_email_function START ===========================================')
  desired_regex_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  if(re.fullmatch(desired_regex_pattern, user_input_email)):
    localhost_print_function('=========================================== sanitize_email_function END ===========================================')
    return user_input_email
  localhost_print_function('=========================================== sanitize_email_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------


# ------------------------ individual function start ------------------------
def sanitize_password_function(user_input_password):
  localhost_print_function('=========================================== sanitize_password_function START ===========================================')
  desired_regex_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
  if(re.fullmatch(desired_regex_pattern, user_input_password)):
    localhost_print_function('=========================================== sanitize_password_function END ===========================================')
    return user_input_password
  localhost_print_function('=========================================== sanitize_password_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------




localhost_print_function('=========================================== user_inputs __init__ END ===========================================')
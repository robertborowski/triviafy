# ------------------------ imports start ------------------------
import re
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_letters_numbers_spaces_only_function(user_input):
  if len(user_input) == 0 or len(user_input) > 100:
    return False
  desired_regex_pattern = "^[a-zA-Z0-9 ]{1,100}$"
  if(re.fullmatch(desired_regex_pattern, user_input)):
    return user_input
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_letters_numbers_spaces_specials_only_function(user_input):
  if len(user_input) == 0 or len(user_input) > 100:
    return False
  desired_regex_pattern = r'^[a-zA-Z0-9\s\-\$\@\!\?\,]{1,100}$'
  if(re.fullmatch(desired_regex_pattern, user_input)):
    return user_input
  return False
# ------------------------ individual function end ------------------------
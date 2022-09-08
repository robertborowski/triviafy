# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import re
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== user_inputs __init__ START ===========================================')
# ------------------------ block email list start ------------------------
blocked_email_arr = [
  '@gmail.com',
  '@yahoo.',
  '@ymail.com',
  '@mail.com',
  '@msn.',
  '@aol.',
  '@fb.com',
  '@hotmail.',
  '@outlook.',
  '@topmail.ws',
  '@iopmail.com',
  '@mailinator.com',
  '@onmicrosoft.com',
  '@bingzone.net',
  '@msgsafe.io',
  '@sharklasers.com',
  '@ttirv.com',
  '@pm.me',
  '@protonmail.com',
  '@qq.com',
  '@gamil.com',
  '@gmal.com',
  '@me.com',
  '@yopmail.com',
  '@hey.com',
  '@icloud.com',
  '@fastmail.fm',
  '@mail.ru',
  '@web.de',
  '@ya.ru',
  '@vp.pl',
  '@inboxbear.com',
  '@tuks.co.za',
  '@kiabws.com',
  '@cikuh.com',
  '@relay.firefox.com',
  '@citromail.hu',
  '@mailpoof.com',
  '@biyac.com',
  '@byom.de',
  '@yandex.ru',
  '@naver.com',
  '@ukr.net',
  '@cuoly.com',
  '@zohomail.in',
  '@sltn.net',
  '@laposte.sn',
  '.edu'
]
# ------------------------ block email list end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_email_function(user_input_email):
  localhost_print_function('=========================================== sanitize_email_function START ===========================================')
  desired_regex_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  if(re.fullmatch(desired_regex_pattern, user_input_email)):
    # Check email for personal tags
    user_input_email = check_email_personal_tags_function(user_input_email)
    localhost_print_function('=========================================== sanitize_email_function END ===========================================')
    return user_input_email
  localhost_print_function('=========================================== sanitize_email_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------


# ------------------------ individual function start ------------------------
def check_email_personal_tags_function(user_input_email):
  localhost_print_function('=========================================== check_email_personal_tags_function START ===========================================')
  for i_email in blocked_email_arr:
    if i_email in user_input_email:
      print('yes!')
      localhost_print_function('=========================================== check_email_personal_tags_function END ===========================================')
      return False
  localhost_print_function('=========================================== check_email_personal_tags_function END ===========================================')
  return user_input_email
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
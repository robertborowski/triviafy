# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import re
from website.models import CandidatesUploadedCandidatesObj
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== user_inputs __init__ START ===========================================')

# ------------------------ individual function start ------------------------
def sanitize_email_function(user_input_email, is_signup='false'):
  localhost_print_function('=========================================== sanitize_email_function START ===========================================')
  desired_regex_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  if(re.fullmatch(desired_regex_pattern, user_input_email)):
    # Check email for personal tags
    if is_signup == 'true':
      user_input_email = check_email_personal_tags_function(user_input_email)
    localhost_print_function('=========================================== sanitize_email_function END ===========================================')
    return user_input_email
  localhost_print_function('=========================================== sanitize_email_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
# ------------------------ block email list start ------------------------
blocked_email_arr = [
  '@gmail.com',
  '@gmail',
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
  '.edu']
# ------------------------ block email list end ------------------------
def check_email_personal_tags_function(user_input_email):
  localhost_print_function('=========================================== check_email_personal_tags_function START ===========================================')
  for i_email in blocked_email_arr:
    if i_email in user_input_email:
      localhost_print_function('=========================================== check_email_personal_tags_function END ===========================================')
      return False
  localhost_print_function('=========================================== check_email_personal_tags_function END ===========================================')
  return user_input_email
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_password_archive_v1_function(user_input_password):
  localhost_print_function('=========================================== sanitize_password_function START ===========================================')
  desired_regex_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
  if(re.fullmatch(desired_regex_pattern, user_input_password)):
    localhost_print_function('=========================================== sanitize_password_function END ===========================================')
    return user_input_password
  localhost_print_function('=========================================== sanitize_password_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_password_function(user_input_password):
  localhost_print_function('=========================================== sanitize_password_function START ===========================================')
  if len(user_input_password) > 150 or len(user_input_password) < 4:
    localhost_print_function('=========================================== sanitize_password_function END ===========================================')
    return False
  localhost_print_function('=========================================== sanitize_password_function END ===========================================')
  return user_input_password
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_account_text_inputs_function(user_input):
  localhost_print_function('=========================================== sanitize_create_account_text_inputs_function START ===========================================')
  desired_regex_pattern = "^[\w\s-]{0,20}$"
  if(re.fullmatch(desired_regex_pattern, user_input)):
    localhost_print_function('=========================================== sanitize_create_account_text_inputs_function END ===========================================')
    return user_input
  localhost_print_function('=========================================== sanitize_create_account_text_inputs_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_desired_langs_text_inputs_function(user_input):
  localhost_print_function('=========================================== sanitize_create_account_text_inputs_function START ===========================================')
  desired_regex_pattern = "^[\w\s,-]{1,150}$"
  if(re.fullmatch(desired_regex_pattern, user_input)):
    localhost_print_function('=========================================== sanitize_create_account_text_inputs_function END ===========================================')
    return user_input
  localhost_print_function('=========================================== sanitize_create_account_text_inputs_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_account_text_inputs_large_function(user_input):
  localhost_print_function('=========================================== sanitize_create_account_text_inputs_large_function START ===========================================')
  if len(user_input) == 0:
    localhost_print_function('=========================================== sanitize_create_account_text_inputs_function END ===========================================')
    return False
  desired_regex_pattern = "^[\w\s-]{1,50}$"
  if(re.fullmatch(desired_regex_pattern, user_input)):
    localhost_print_function('=========================================== sanitize_create_account_text_inputs_large_function END ===========================================')
    return user_input
  localhost_print_function('=========================================== sanitize_create_account_text_inputs_large_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_candidate_ui_answer_text_function(user_input):
  localhost_print_function('=========================================== sanitize_candidate_ui_answer_text_function START ===========================================')
  if len(user_input) == 0:
    localhost_print_function('=========================================== sanitize_candidate_ui_answer_text_function END ===========================================')
    return False
  desired_regex_pattern = "^[*]{1,100}$"
  if(re.fullmatch(desired_regex_pattern, user_input)):
    localhost_print_function('=========================================== sanitize_candidate_ui_answer_text_function END ===========================================')
    return user_input
  localhost_print_function('=========================================== sanitize_candidate_ui_answer_text_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_question_categories_function(user_input):
  localhost_print_function('=========================================== sanitize_create_question_categories_function START ===========================================')
  if len(user_input) == 0 or len(user_input) > 50:
    localhost_print_function('=========================================== sanitize_create_question_categories_function END ===========================================')
    return False
  localhost_print_function('=========================================== sanitize_create_question_categories_function END ===========================================')
  return user_input
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_char_count_1_function(user_input):
  localhost_print_function('=========================================== sanitize_char_count_1_function START ===========================================')
  if len(user_input) == 0 or len(user_input) > 100:
    localhost_print_function('=========================================== sanitize_char_count_1_function END ===========================================')
    return False
  localhost_print_function('=========================================== sanitize_char_count_1_function END ===========================================')
  return user_input
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_question_question_function(user_input):
  localhost_print_function('=========================================== sanitize_create_question_question_function START ===========================================')
  if len(user_input) == 0 or len(user_input) > 750:
    localhost_print_function('=========================================== sanitize_create_question_question_function END ===========================================')
    return False
  localhost_print_function('=========================================== sanitize_create_question_question_function END ===========================================')
  return user_input
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_question_options_function(user_input):
  localhost_print_function('=========================================== sanitize_create_question_options_function START ===========================================')
  if len(user_input) == 0 or len(user_input) > 280:
    localhost_print_function('=========================================== sanitize_create_question_options_function END ===========================================')
    return False
  localhost_print_function('=========================================== sanitize_create_question_options_function END ===========================================')
  return user_input
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_question_option_e_function(user_input):
  localhost_print_function('=========================================== sanitize_create_question_options_function START ===========================================')
  if user_input == None or user_input == '':
    localhost_print_function('=========================================== sanitize_create_question_options_function END ===========================================')
    return user_input
  if len(user_input) > 280:
    localhost_print_function('=========================================== sanitize_create_question_options_function END ===========================================')
    return False
  localhost_print_function('=========================================== sanitize_create_question_options_function END ===========================================')
  return user_input
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_question_answer_function(user_input):
  localhost_print_function('=========================================== sanitize_create_question_answer_function START ===========================================')
  if len(user_input) == 0 or len(user_input) > 2:
    localhost_print_function('=========================================== sanitize_create_question_answer_function END ===========================================')
    return False
  allowed_answers_arr = ['a','b','c','d','e']
  if user_input.lower() in allowed_answers_arr:
    localhost_print_function('=========================================== sanitize_create_question_answer_function END ===========================================')
    return user_input
  localhost_print_function('=========================================== sanitize_create_question_answer_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_question_difficulty_function(user_input):
  localhost_print_function('=========================================== sanitize_create_question_difficulty_function START ===========================================')
  if len(user_input) == 0 or len(user_input) > 7:
    localhost_print_function('=========================================== sanitize_create_question_difficulty_function END ===========================================')
    return False
  allowed_answers_arr = ['easy','medium','hard']
  if user_input.lower() in allowed_answers_arr:
    localhost_print_function('=========================================== sanitize_create_question_difficulty_function END ===========================================')
    return user_input
  localhost_print_function('=========================================== sanitize_create_question_difficulty_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_candidate_ui_answer_radio_function(user_input):
  localhost_print_function('=========================================== sanitize_candidate_ui_answer_text_function START ===========================================')
  if len(user_input) == 0 or len(user_input) > 2:
    localhost_print_function('=========================================== sanitize_candidate_ui_answer_text_function END ===========================================')
    return False
  allowed_answers_arr = ['a','b','c','d','e']
  if user_input.lower() in allowed_answers_arr:
    localhost_print_function('=========================================== sanitize_candidate_ui_answer_text_function END ===========================================')
    return user_input
  localhost_print_function('=========================================== sanitize_candidate_ui_answer_text_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_loop_check_if_exists_within_arr_function(user_input_arr, correct_master_arr):
  localhost_print_function('=========================================== sanitize_loop_check_if_exists_within_arr_function START ===========================================')
  if user_input_arr == None or len(user_input_arr) == 0 or user_input_arr == []:
    localhost_print_function('=========================================== sanitize_loop_check_if_exists_within_arr_function END ===========================================')
    return False
  for i_str in user_input_arr:
    if i_str not in correct_master_arr:
      localhost_print_function('user input provided is not an option')
      localhost_print_function('=========================================== sanitize_loop_check_if_exists_within_arr_function END ===========================================')
      return False
  localhost_print_function('=========================================== sanitize_loop_check_if_exists_within_arr_function END ===========================================')
  return user_input_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_check_if_str_exists_within_arr_function(user_input_str, correct_master_arr):
  localhost_print_function('=========================================== sanitize_loop_check_if_exists_within_arr_function START ===========================================')
  if user_input_str == None:
    localhost_print_function('=========================================== sanitize_loop_check_if_exists_within_arr_function END ===========================================')
    return False
  if len(user_input_str) == 0:
    localhost_print_function('=========================================== sanitize_loop_check_if_exists_within_arr_function END ===========================================')
    return False
  if user_input_str not in correct_master_arr:
    localhost_print_function('user input provided is not an option')
    localhost_print_function('=========================================== sanitize_loop_check_if_exists_within_arr_function END ===========================================')
    return False
  localhost_print_function('=========================================== sanitize_loop_check_if_exists_within_arr_function END ===========================================')
  return user_input_str
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def validate_upload_candidate_function(db, current_user, ui_email, user_input_type):
  localhost_print_function('=========================================== validate_upload_candidate_function START ===========================================')
  post_result = ''
  # ------------------------ ui_email start ------------------------
  # ------------------------ sanitize/check user input email start ------------------------
  if ui_email != None:
    ui_email_cleaned = sanitize_email_function(ui_email)
    if ui_email_cleaned == False and user_input_type == 'individual':
      post_result = 'e1'
    # ------------------------ sanitize/check user input email end ------------------------
    if ui_email_cleaned != False:
      # ------------------------ check if exists in db start ------------------------
      candidate_uploaded_email_exists = CandidatesUploadedCandidatesObj.query.filter_by(user_id_fk=current_user.id).filter_by(email=ui_email_cleaned).first()
      # ------------------------ check if exists in db end ------------------------
      if candidate_uploaded_email_exists != None and user_input_type == 'individual':
        post_result = f'e2'
      if candidate_uploaded_email_exists == None:
        # ------------------------ create new user in db start ------------------------
        new_user = CandidatesUploadedCandidatesObj(
          id=create_uuid_function('candup_'),
          created_timestamp=create_timestamp_function(),
          user_id_fk=current_user.id,
          candidate_id=create_uuid_function('cand_'),
          email = ui_email_cleaned,
          upload_type = user_input_type
        )
        db.session.add(new_user)
        db.session.commit()
        # ------------------------ create new user in db end ------------------------
  # ------------------------ ui_email end ------------------------
  if post_result == '':
    post_result = 'success'
  localhost_print_function('=========================================== validate_upload_candidate_function END ===========================================')
  return post_result
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def check_if_question_id_arr_exists_function(user_input_arr):
  localhost_print_function('=========================================== sanitize_loop_check_if_exists_within_arr_function START ===========================================')
  for i in user_input_arr:
    sql_result = select_general_function('select_question_id_actually_exists_v2', i)
    if sql_result == [] or len(sql_result) == 0:
      return False
  localhost_print_function('=========================================== sanitize_loop_check_if_exists_within_arr_function END ===========================================')
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_letters_numbers_spaces_only_function(user_input):
  localhost_print_function('=========================================== sanitize_letters_numbers_spaces_only_function START ===========================================')
  if len(user_input) == 0 or len(user_input) > 100:
    localhost_print_function('=========================================== sanitize_letters_numbers_spaces_only_function END ===========================================')
    return False
  desired_regex_pattern = "^[a-zA-Z0-9 ]{1,100}$"
  if(re.fullmatch(desired_regex_pattern, user_input)):
    localhost_print_function('=========================================== sanitize_letters_numbers_spaces_only_function END ===========================================')
    return user_input
  localhost_print_function('=========================================== sanitize_letters_numbers_spaces_only_function END ===========================================')
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def alert_message_default_function():
  # localhost_print_function('=========================================== alert_message_default_function START ===========================================')
  alert_message_page = ''
  alert_message_type = 'danger'
  # localhost_print_function('=========================================== alert_message_default_function END ===========================================')
  return alert_message_page, alert_message_type
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def alert_message_default_function_v2(redirect_var=None):
  # localhost_print_function('=========================================== alert_message_default_function_v2 START ===========================================')
  # ------------------------ errors start ------------------------
  alert_message_dict = {
      'message':'',
      'type':'danger'
    }
  if redirect_var == None:
    pass
  elif redirect_var == 'e1':
    alert_message_dict = {
      'message':'Please enter a valid work email.',
      'type':'danger'
    }
  elif redirect_var == 'e2':
    alert_message_dict = {
      'message':'Please enter a valid password.',
      'type':'danger'
    }
  elif redirect_var == 'e3':
    alert_message_dict = {
      'message':'Account already created for email.',
      'type':'danger'
    }
  elif redirect_var == 'e4':
    alert_message_dict = {
      'message':'Incorrect username/password.',
      'type':'danger'
    }
  elif redirect_var == 'e5':
    alert_message_dict = {
      'message':'Requested categories should be 1-100 characters long.',
      'type':'danger'
    }
  elif redirect_var == 'e6':
    alert_message_dict = {
      'message':'Invalid inputs.',
      'type':'danger'
    }
  elif redirect_var == 'e7':
    alert_message_dict = {
      'message':'You must select at least 1 triviafy category.',
      'type':'danger'
    }
  elif redirect_var == 'e8':
    alert_message_dict = {
      'message':'Your quiz start day/time must be at least 1 hour before your quiz end day/time.',
      'type':'danger'
    }
  # ------------------------ errors end ------------------------
  # ------------------------ success start ------------------------
  elif redirect_var == 's1':
    alert_message_dict = {
      'message':'Request sent.',
      'type':'success'
    }
  elif redirect_var == 's2':
    alert_message_dict = {
      'message':'Schedule settings successfully updated.',
      'type':'success'
    }
  elif redirect_var == 's3':
    alert_message_dict = {
      'message':'Quiz successfully created.',
      'type':'success'
    }
  elif redirect_var == 's4':
    alert_message_dict = {
      'message':'Quiz successfully submitted.',
      'type':'success'
    }
  # ------------------------ success end ------------------------
  # ------------------------ info end ------------------------
  elif redirect_var == 'i1':
    alert_message_dict = {
      'message':'Schedule settings unchanged.',
      'type':'info'
    }
  # ------------------------ info end ------------------------
  # localhost_print_function('=========================================== alert_message_default_function_v2 END ===========================================')
  return alert_message_dict
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== user_inputs __init__ END ===========================================')
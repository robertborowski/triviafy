# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import re
from website.models import CandidatesUploadedCandidatesObj
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== user_inputs __init__ START ===========================================')

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
# ------------------------ block email list start ------------------------
blocked_email_arr = [
  # '@gmail.com',
  # '@yahoo.',
  # '@ymail.com',
  # '@mail.com',
  # '@msn.',
  # '@aol.',
  # '@fb.com',
  # '@hotmail.',
  # '@outlook.',
  # '@topmail.ws',
  # '@iopmail.com',
  # '@mailinator.com',
  # '@onmicrosoft.com',
  # '@bingzone.net',
  # '@msgsafe.io',
  # '@sharklasers.com',
  # '@ttirv.com',
  # '@pm.me',
  # '@protonmail.com',
  # '@qq.com',
  # '@gamil.com',
  # '@gmal.com',
  # '@me.com',
  # '@yopmail.com',
  # '@hey.com',
  # '@icloud.com',
  # '@fastmail.fm',
  # '@mail.ru',
  # '@web.de',
  # '@ya.ru',
  # '@vp.pl',
  # '@inboxbear.com',
  # '@tuks.co.za',
  # '@kiabws.com',
  # '@cikuh.com',
  # '@relay.firefox.com',
  # '@citromail.hu',
  # '@mailpoof.com',
  # '@biyac.com',
  # '@byom.de',
  # '@yandex.ru',
  # '@naver.com',
  # '@ukr.net',
  # '@cuoly.com',
  # '@zohomail.in',
  # '@sltn.net',
  # '@laposte.sn',
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
def sanitize_password_function(user_input_password):
  localhost_print_function('=========================================== sanitize_password_function START ===========================================')
  desired_regex_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
  if(re.fullmatch(desired_regex_pattern, user_input_password)):
    localhost_print_function('=========================================== sanitize_password_function END ===========================================')
    return user_input_password
  localhost_print_function('=========================================== sanitize_password_function END ===========================================')
  return False
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
def sanitize_loop_check_if_exists_within_arr_function(user_input_arr, correct_master_arr):
  localhost_print_function('=========================================== sanitize_loop_check_if_exists_within_arr_function START ===========================================')
  if len(user_input_arr) == 0:
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
def validate_upload_candidate_function(db, current_user, ui_email, user_input_type):
  localhost_print_function('=========================================== validate_upload_candidate_function START ===========================================')
  candidate_upload_error_statement = ''
  # ------------------------ ui_email start ------------------------
  # ------------------------ sanitize/check user input email start ------------------------
  if ui_email != None:
    ui_email_cleaned = sanitize_email_function(ui_email)
    if ui_email_cleaned == False and user_input_type == 'individual':
      candidate_upload_error_statement = 'Please enter a valid email.'
    # ------------------------ sanitize/check user input email end ------------------------
    if ui_email_cleaned != False:
      # ------------------------ check if exists in db start ------------------------
      candidate_uploaded_email_exists = CandidatesUploadedCandidatesObj.query.filter_by(user_id_fk=current_user.id).filter_by(email=ui_email_cleaned).first()
      # ------------------------ check if exists in db end ------------------------
      if candidate_uploaded_email_exists != None and user_input_type == 'individual':
        candidate_upload_error_statement = f'Candidate email: {ui_email_cleaned} already added.'
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
  if candidate_upload_error_statement == '':
    candidate_upload_error_statement = 'Uploaded successfully!'
  localhost_print_function('=========================================== validate_upload_candidate_function END ===========================================')
  return candidate_upload_error_statement
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== user_inputs __init__ END ===========================================')
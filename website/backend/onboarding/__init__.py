# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.models import UserSignupFeedbackObj
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def search_feedback_function(current_user, input_feedback):
  feedback_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question=input_feedback).first()
  if feedback_obj == None or feedback_obj == []:
    return input_feedback
  else:
    return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def onboarding_checks_v2_function(current_user):
  # ------------------------ check if email verified start ------------------------
  if current_user.verified_email == False:
    return 'verify'
  # ------------------------ check if email verified end ------------------------
  # ------------------------ check if feedback given start ------------------------
  search_feedback_arr = ['polling_terms_of_service']
  for i_feedback in search_feedback_arr:
    feedback_obj = search_feedback_function(current_user,i_feedback)
    if feedback_obj == i_feedback:
      return i_feedback
  # name
  if current_user.name == None or current_user.name == '' or current_user.last_name == None or current_user.last_name == '':
    return 'name'
  """
  # primary
  feedback_primary_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='primary_product_choice').first()
  if feedback_primary_obj == None or feedback_primary_obj == []:
    return 'primary'
  # secondary
  feedback_secondary_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='secondary_product_choice').first()
  if feedback_secondary_obj == None or feedback_secondary_obj == []:
    return 'secondary'
  # birthday
  feedback_birthday_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='birthday_choice').first()
  if feedback_birthday_obj == None or feedback_birthday_obj == []:
    return 'birthday'
  # job_start_date
  feedback_birthday_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='job_start_date_choice').first()
  if feedback_birthday_obj == None or feedback_birthday_obj == []:
    return 'job_start_date'
  # how did you hear about triviafy?
  feedback_marketing_obj = UserSignupFeedbackObj.query.filter_by(fk_user_id=current_user.id,question='marketing_choice').first()
  if feedback_marketing_obj == None or feedback_marketing_obj == []:
    return 'marketing'
  # ------------------------ check if feedback given end ------------------------
  """
  return False
# ------------------------ individual function end ------------------------
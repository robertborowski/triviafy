# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import stripe
from datetime import datetime
import os
from website.models import UserObj
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def check_stripe_subscription_status_function(current_user):
  # ------------------------ stripe subscription status check start ------------------------
  fk_stripe_subscription_id = current_user.fk_stripe_subscription_id
  stripe_subscription_obj = ''
  stripe_subscription_obj_status = 'not active'
  try:
    stripe_subscription_obj = stripe.Subscription.retrieve(fk_stripe_subscription_id)
    stripe_subscription_obj_status = stripe_subscription_obj.status
  except:
    pass
  # ------------------------ delete this, only for testing start ------------------------
  # stripe_subscription_obj_status = 'active'
  # ------------------------ delete this, only for testing end ------------------------
  # ------------------------ stripe subscription status check end ------------------------
  return stripe_subscription_obj_status
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def check_stripe_subscription_status_function_v2(current_user, product, attempting_user=None):
  # ------------------------ stripe subscription status check start ------------------------
  if product == 'candidates':
    fk_stripe_subscription_id = current_user.fk_stripe_subscription_id
  if product == 'employees':
    fk_stripe_subscription_id = current_user.employees_fk_stripe_subscription_id
    # ------------------------ loop through whole team's subscription status start ------------------------
    try:
      db_user_obj = UserObj.query.filter_by(email=attempting_user).first()
      db_users_obj = UserObj.query.filter_by(group_id=db_user_obj.group_id).all()
      for i_user in db_users_obj:
        if i_user.employees_fk_stripe_subscription_id != None and i_user.employees_fk_stripe_subscription_id != '':
          fk_stripe_subscription_id = i_user.employees_fk_stripe_subscription_id
    except:
      pass
    # ------------------------ loop through whole team's subscription status end ------------------------
  else:
    return 'invalid product'
  stripe_subscription_obj = ''
  stripe_subscription_obj_status = 'not active'
  try:
    stripe_subscription_obj = stripe.Subscription.retrieve(fk_stripe_subscription_id)
    stripe_subscription_obj_status = stripe_subscription_obj.status
  except:
    pass
  # ------------------------ auto subscribed email list start ------------------------
  # if attempting_user == os.environ.get('RUN_TEST_EMAIL'):
  #   stripe_subscription_obj_status = 'active'
  # ------------------------ auto subscribed email list end ------------------------
  # ------------------------ stripe subscription status check end ------------------------
  return stripe_subscription_obj_status
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def convert_current_period_end_function(stripe_subscription_obj):
  # ------------------------ convert unix timestamp to regular start ------------------------
  stripe_current_period_end_unix = stripe_subscription_obj.current_period_end
  ts = int(stripe_current_period_end_unix)
  # stripe_current_period_end = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  stripe_current_period_end = datetime.utcfromtimestamp(ts).strftime('%m/%d')
  # ------------------------ convert unix timestamp to regular end ------------------------
  return stripe_current_period_end
# ------------------------ individual function end ------------------------
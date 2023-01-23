# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import stripe
from datetime import datetime
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== stripe __init__ START ===========================================')
# ------------------------ individual function start ------------------------
def check_stripe_subscription_status_function(current_user):
  localhost_print_function('=========================================== check_stripe_subscription_status_function START ===========================================')
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
  localhost_print_function('=========================================== check_stripe_subscription_status_function END ===========================================')
  return stripe_subscription_obj_status
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def convert_current_period_end_function(stripe_subscription_obj):
  localhost_print_function('=========================================== convert_current_period_end_function START ===========================================')
  # ------------------------ convert unix timestamp to regular start ------------------------
  stripe_current_period_end_unix = stripe_subscription_obj.current_period_end
  ts = int(stripe_current_period_end_unix)
  # stripe_current_period_end = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  stripe_current_period_end = datetime.utcfromtimestamp(ts).strftime('%m/%d')
  # ------------------------ convert unix timestamp to regular end ------------------------
  localhost_print_function('=========================================== convert_current_period_end_function END ===========================================')
  return stripe_current_period_end
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== stripe __init__ END ===========================================')
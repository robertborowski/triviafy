# ------------------------ imports start ------------------------
import email
from importlib.metadata import metadata
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os
import stripe
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def testing_stripe_function():
  localhost_print_function('=========================================== testing_stripe_function start ===========================================')
  # ------------------------ stripe api environment start ------------------------
  stripe.api_key = os.environ.get('STRIPE_API_KEY')
  # stripe.api_key = os.environ.get('STRIPE_TEST_API_KEY')
  # ------------------------ stripe api environment end ------------------------
  # ------------------------ testing start ------------------------
  print(stripe.Customer.retrieve('abc'))
  # ------------------------ testing end ------------------------
  localhost_print_function('=========================================== testing_stripe_function end ===========================================')
  return True
# ------------------------ individual function end ------------------------

# ------------------------ call function directly start ------------------------
if __name__ == '__main__':
  localhost_print_function('=========================================== if __name__ == "__main__": START ===========================================')
  testing_stripe_function()
  localhost_print_function('=========================================== if __name__ == "__main__": END ===========================================')
# ------------------------ call function directly end ------------------------
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os, time
import datetime
# ------------------------ imports end ------------------------

# ------------------------ set timezone start ------------------------
# Set the timezone of the application when user creates account is will be in US/Easterm time
os.environ['TZ'] = 'US/Eastern'
time.tzset()
# ------------------------ set timezone end ------------------------

localhost_print_function('=========================================== datetime_manipulation __init__ START ===========================================')
# ------------------------ individual function start ------------------------
def next_x_days_function():
  localhost_print_function('=========================================== next_x_days_function START ===========================================')
  # ------------------------ get todays date start ------------------------
  days_counter = 0
  days_counter_limit = 40
  next_x_days_arr = []
  while days_counter < days_counter_limit:
    current_date_str = (datetime.datetime.now() + datetime.timedelta(days=days_counter)).strftime('%m-%d-%Y')
    days_counter += 1
    next_x_days_arr.append(current_date_str)
  # ------------------------ get todays date end ------------------------
  localhost_print_function('=========================================== next_x_days_function END ===========================================')
  return next_x_days_arr
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== datetime_manipulation __init__ END ===========================================')
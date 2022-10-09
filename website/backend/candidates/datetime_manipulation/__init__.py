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

# ------------------------ individual function start ------------------------
def times_arr_function():
  localhost_print_function('=========================================== next_x_days_function START ===========================================')
  # ------------------------ get todays date start ------------------------
  times_arr = [
    '12 AM',
    '1 AM',
    '2 AM',
    '3 AM',
    '4 AM',
    '5 AM',
    '6 AM',
    '7 AM',
    '8 AM',
    '9 AM',
    '10 AM',
    '11 AM',
    '12 PM',
    '1 PM',
    '2 PM',
    '3 PM',
    '4 PM',
    '5 PM',
    '6 PM',
    '7 PM',
    '8 PM',
    '9 PM',
    '10 PM',
    '11 PM'
  ]
  # ------------------------ get todays date end ------------------------
  localhost_print_function('=========================================== next_x_days_function END ===========================================')
  return times_arr
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== datetime_manipulation __init__ END ===========================================')
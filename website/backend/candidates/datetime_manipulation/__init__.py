# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os, time
from datetime import datetime, timedelta
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
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
    current_date_str = (datetime.now() + timedelta(days=days_counter)).strftime('%m-%d-%Y')
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
  timezone_arr = [
    'CST',
    'EST',
    'MST',
    'PST'
  ]
  # ------------------------ get todays date end ------------------------
  localhost_print_function('=========================================== next_x_days_function END ===========================================')
  return times_arr, timezone_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def days_times_timezone_arr_function():
  localhost_print_function(' ------------------------ days_times_timezone_arr_function start ------------------------ ')
  # ------------------------ get todays date start ------------------------
  weekdays_arr = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday'
  ]
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
  timezone_arr = [
    'CST',
    'EST',
    'MST',
    'PST'
  ]
  # ------------------------ get todays date end ------------------------
  localhost_print_function(' ------------------------ days_times_timezone_arr_function end ------------------------ ')
  return weekdays_arr, times_arr, timezone_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def expired_assessment_check_function(input_timestamp):
  localhost_print_function('=========================================== expired_assessment_check_function START ===========================================')
  # ------------------------ expire settings start ------------------------  
  expire_limit = 60 * 60
  is_expired = False
  not_open_yet = False
  # ------------------------ expire settings end ------------------------  
  # ------------------------ current time start ------------------------  
  current_datetime_str = create_timestamp_function()
  current_datetime = datetime.strptime(current_datetime_str, '%Y-%m-%d %H:%M:%S')
  # ------------------------ current time end ------------------------  
  # ------------------------ schedule time start ------------------------  
  schedule_timestamp_str = input_timestamp.strftime('%Y-%m-%d %H:%M:%S')
  schedule_timestamp = datetime.strptime(schedule_timestamp_str, '%Y-%m-%d %H:%M:%S')
  # ------------------------ schedule time end ------------------------
  # ------------------------ compare start ------------------------
  difference_datetime = (current_datetime - schedule_timestamp).total_seconds()
  if difference_datetime > expire_limit:
    is_expired = True
  if difference_datetime <= -1:
    not_open_yet = True
    is_expired = not_open_yet
  # ------------------------ compare end ------------------------
  localhost_print_function('=========================================== expired_assessment_check_function END ===========================================')
  return is_expired, not_open_yet
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def times_dict_mapping_function():
  localhost_print_function('=========================================== next_x_days_function START ===========================================')
  # ------------------------ get todays date start ------------------------
  time_mapping_dict = {
    '12 AM': '00:00:00',
    '1 AM': '01:00:00',
    '2 AM': '02:00:00',
    '3 AM': '03:00:00',
    '4 AM': '04:00:00',
    '5 AM': '05:00:00',
    '6 AM': '06:00:00',
    '7 AM': '07:00:00',
    '8 AM': '08:00:00',
    '9 AM': '09:00:00',
    '10 AM': '10:00:00',
    '11 AM': '11:00:00',
    '12 PM': '12:00:00',
    '1 PM': '13:00:00',
    '2 PM': '14:00:00',
    '3 PM': '15:00:00',
    '4 PM': '16:00:00',
    '5 PM': '17:00:00',
    '6 PM': '18:00:00',
    '7 PM': '19:00:00',
    '8 PM': '20:00:00',
    '9 PM': '21:00:00',
    '10 PM': '22:00:00',
    '11 PM': '23:00:00'
  }
  # ------------------------ get todays date end ------------------------
  localhost_print_function('=========================================== next_x_days_function END ===========================================')
  return time_mapping_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def build_out_datetime_from_parts_function(input_date, input_time, input_timezone):
  localhost_print_function('=========================================== expired_assessment_check_function START ===========================================')
  # Current = '10-17-2022', '7 AM', 'EST'
  # Goal = '2022-10-17 07:00:00'
  # ------------------------ fix date start ------------------------
  input_date_arr = input_date.split('-')
  input_date_month = input_date_arr[0]
  input_date_day = input_date_arr[1]
  input_date_year = input_date_arr[2]
  goal_date_str = input_date_year + '-' + input_date_month + '-' + input_date_day
  # ------------------------ fix date end ------------------------
  # ------------------------ fix time based on timezone start ------------------------
  time_mapping_dict = times_dict_mapping_function()
  goal_time_str = ''
  hour_times_arr = ['12 AM', '1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM', '7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM', '10 PM', '11 PM']
  input_time_index_position = hour_times_arr.index(input_time)
  if input_timezone == 'EST':
    goal_time_str = time_mapping_dict[hour_times_arr[input_time_index_position]]
  elif input_timezone == 'PST':
    goal_time_str = time_mapping_dict[hour_times_arr[input_time_index_position-3]]
  elif input_timezone == 'MST':
    goal_time_str = time_mapping_dict[hour_times_arr[input_time_index_position-2]]
  elif input_timezone == 'CST':
    goal_time_str = time_mapping_dict[hour_times_arr[input_time_index_position-1]]
  # ------------------------ fix time based on timezone end ------------------------
  # ------------------------ output manipulation start ------------------------
  goal_str = goal_date_str + ' ' + goal_time_str
  goal_timestamp = datetime.strptime(goal_str, '%Y-%m-%d %H:%M:%S')
  # ------------------------ output manipulation end ------------------------
  localhost_print_function('=========================================== expired_assessment_check_function END ===========================================')
  return goal_timestamp
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_current_weekday_function():
  localhost_print_function(' ------------------------ get_current_weekday_function start ------------------------ ')
  weekday_dict = {
    0 : 'Monday',
    1 : 'Tuesday',
    2 : 'Wednesday',
    3 : 'Thursday',
    4 : 'Friday',
    5 : 'Saturday',
    6 : 'Sunday'
  }
  weekday_num = datetime.today().weekday()
  weekday = weekday_dict[weekday_num]
  localhost_print_function(' ------------------------ get_current_weekday_function end ------------------------ ')
  return weekday
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_current_hour_function():
  localhost_print_function(' ------------------------ get_current_hour_function start ------------------------ ')
  time_mapping_dict = {
    0 : '12 AM',
    1 : '1 AM',
    2 : '2 AM',
    3 : '3 AM',
    4 : '4 AM',
    5 : '5 AM',
    6 : '6 AM',
    7 : '7 AM',
    8 : '8 AM',
    9 : '9 AM',
    10 : '10 AM',
    11 : '11 AM',
    12: '12 PM',
    13: '1 PM',
    14: '2 PM',
    15: '3 PM',
    16: '4 PM',
    17: '5 PM',
    18: '6 PM',
    19: '7 PM',
    20: '8 PM',
    21: '9 PM',
    22: '10 PM',
    23: '11 PM'
  }
  current_hour_num = datetime.now().hour
  current_hour = time_mapping_dict[current_hour_num]
  localhost_print_function(' ------------------------ get_current_hour_function end ------------------------ ')
  return current_hour
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== datetime_manipulation __init__ END ===========================================')
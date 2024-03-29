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

# ------------------------ individual function start ------------------------
def next_x_days_function():
  # ------------------------ get todays date start ------------------------
  days_counter = 0
  days_counter_limit = 40
  next_x_days_arr = []
  while days_counter < days_counter_limit:
    current_date_str = (datetime.now() + timedelta(days=days_counter)).strftime('%m-%d-%Y')
    days_counter += 1
    next_x_days_arr.append(current_date_str)
  # ------------------------ get todays date end ------------------------
  return next_x_days_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def times_arr_function():
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
  return times_arr, timezone_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def days_times_timezone_arr_function():
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
  return weekdays_arr, times_arr, timezone_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def expired_assessment_check_function(input_timestamp):
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
  return is_expired, not_open_yet
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def times_dict_mapping_function():
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
  return time_mapping_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def build_out_datetime_from_parts_function(input_date, input_time, input_timezone):
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
    goal_time_str = time_mapping_dict[hour_times_arr[input_time_index_position+3]]
  elif input_timezone == 'MST':
    goal_time_str = time_mapping_dict[hour_times_arr[input_time_index_position+2]]
  elif input_timezone == 'CST':
    goal_time_str = time_mapping_dict[hour_times_arr[input_time_index_position+1]]
  # ------------------------ fix time based on timezone end ------------------------
  # ------------------------ output manipulation start ------------------------
  goal_str = goal_date_str + ' ' + goal_time_str
  goal_timestamp = datetime.strptime(goal_str, '%Y-%m-%d %H:%M:%S')
  # ------------------------ output manipulation end ------------------------
  return goal_timestamp
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_weekday_dict_function():
  weekday_dict = {
    0 : 'Monday',
    1 : 'Tuesday',
    2 : 'Wednesday',
    3 : 'Thursday',
    4 : 'Friday',
    5 : 'Saturday',
    6 : 'Sunday'
  }
  return weekday_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_weekday_dict_function_v2():
  weekday_dict = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
  }
  return weekday_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_time_mapping_dict_function():
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
  return time_mapping_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_current_weekday_function():
  weekday_dict = get_weekday_dict_function()
  weekday_num = datetime.today().weekday()
  weekday = weekday_dict[weekday_num]
  return weekday
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_current_hour_function():
  time_mapping_dict = get_time_mapping_dict_function()
  current_hour_num = datetime.now().hour
  current_hour = time_mapping_dict[current_hour_num]
  return current_hour
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_upcoming_date_function(goal_day_of_week, cannot_be_less_than_date=None):
  if cannot_be_less_than_date != None:
    cannot_be_less_than_date = datetime.strptime(cannot_be_less_than_date, '%m-%d-%Y').date()
  weekday_dict = get_weekday_dict_function()
  weekday_found = False
  counter = 0
  result_date = '1/1/1901'
  while weekday_found == False:
    i_date = datetime.today()+timedelta(days=counter)
    i_weekday_num = i_date.weekday()
    i_weekday = weekday_dict[i_weekday_num]
    if (i_weekday == goal_day_of_week and cannot_be_less_than_date==None) or (i_weekday == goal_day_of_week and i_date.date() > cannot_be_less_than_date):
      weekday_found = True
      result_date = i_date.strftime('%m-%d-%Y')
    else:
      counter += 1
  return result_date
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_week_dates_function(date_var):
  weekday_var = date_var.weekday()
  # ------------------------ define variables start ------------------------
  monday = 0
  tuesday = 0
  wednesday = 0
  thursday = 0
  friday = 0
  saturday = 0
  sunday = 0
  # ------------------------ define variables end ------------------------
  # Monday
  if weekday_var == 0:
    monday = date_var
    tuesday = date_var + timedelta(days=1)
    wednesday = date_var + timedelta(days=2)
    thursday = date_var + timedelta(days=3)
    friday = date_var + timedelta(days=4)
    saturday = date_var + timedelta(days=5)
    sunday = date_var + timedelta(days=6)
  # Tuesday
  if weekday_var == 1:
    monday = date_var - timedelta(days=1)
    tuesday = date_var
    wednesday = date_var + timedelta(days=1)
    thursday = date_var + timedelta(days=2)
    friday = date_var + timedelta(days=3)
    saturday = date_var + timedelta(days=4)
    sunday = date_var + timedelta(days=5)
  # Wednesday
  if weekday_var == 2:
    monday = date_var - timedelta(days=2)
    tuesday = date_var - timedelta(days=1)
    wednesday = date_var
    thursday = date_var + timedelta(days=1)
    friday = date_var + timedelta(days=2)
    saturday = date_var + timedelta(days=3)
    sunday = date_var + timedelta(days=4)
  # Thursday
  if weekday_var == 3:
    monday = date_var - timedelta(days=3)
    tuesday = date_var - timedelta(days=2)
    wednesday = date_var - timedelta(days=1)
    thursday = date_var
    friday = date_var + timedelta(days=1)
    saturday = date_var + timedelta(days=2)
    sunday = date_var + timedelta(days=3)
  # Friday
  if weekday_var == 4:
    monday = date_var - timedelta(days=4)
    tuesday = date_var - timedelta(days=3)
    wednesday = date_var - timedelta(days=2)
    thursday = date_var - timedelta(days=1)
    friday = date_var
    saturday = date_var + timedelta(days=1)
    sunday = date_var + timedelta(days=2)
  # Saturday
  if weekday_var == 5:
    monday = date_var - timedelta(days=5)
    tuesday = date_var - timedelta(days=4)
    wednesday = date_var - timedelta(days=3)
    thursday = date_var - timedelta(days=2)
    friday = date_var - timedelta(days=1)
    saturday = date_var
    sunday = date_var + timedelta(days=1)
  # Sunday
  if weekday_var == 6:
    monday = date_var - timedelta(days=6)
    tuesday = date_var - timedelta(days=5)
    wednesday = date_var - timedelta(days=4)
    thursday = date_var - timedelta(days=3)
    friday = date_var - timedelta(days=2)
    saturday = date_var - timedelta(days=1)
    sunday = date_var
  # ------------------------ arr append start ------------------------
  weekdays_arr = []
  weekdays_arr.append(monday)
  weekdays_arr.append(tuesday)
  weekdays_arr.append(wednesday)
  weekdays_arr.append(thursday)
  weekdays_arr.append(friday)
  weekdays_arr.append(saturday)
  weekdays_arr.append(sunday)
  # ------------------------ arr append end ------------------------
  return weekdays_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def lookup_months_dict_function():
  months_dict = {
    1 : 'Jan',
    2 : 'Feb',
    3 : 'Mar',
    4 : 'Apr',
    5 : 'May',
    6 : 'June',
    7 : 'July',
    8 : 'Aug',
    9 : 'Sept',
    10 : 'Oct',
    11 : 'Nov',
    12 : 'Dec'
  }
  return months_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def convert_timestamp_to_month_day_string_function(input_timestamp):
  str_date = input_timestamp.date().strftime('%m-%d-%Y')
  date_parts_arr = str_date.split('-')
  date_month = int(date_parts_arr[0])
  months_dict = lookup_months_dict_function()
  month_str = months_dict[date_month]
  month_day_str = month_str + f' {int(date_parts_arr[1])}'
  return month_day_str
# ------------------------ individual function end ------------------------
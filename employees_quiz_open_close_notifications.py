# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.employees import select_manual_function
from datetime import datetime, timedelta
import os, time
# ------------------------ imports end ------------------------

# ------------------------ set timezone start ------------------------
# Set the timezone of the application when user creates account is will be in US/Easterm time
os.environ['TZ'] = 'US/Eastern'
time.tzset()
# ------------------------ set timezone end ------------------------

# ------------------------ individual function start ------------------------
# fix issue: "can't compare offset-naive and offset-aware datetimes"
def timestamp_offset_convert_function(input_dt):
  input_dt = input_dt.strftime("%Y-%m-%d %H:%M:%S")
  input_dt = datetime.strptime(input_dt, "%Y-%m-%d %H:%M:%S")
  return input_dt
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_current_timestamp_function():
  current_timestamp = datetime.now()
  current_timestamp = timestamp_offset_convert_function(current_timestamp)
  return current_timestamp
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_week_dates_function(date_var):
  # localhost_print_function(' ------------------------ get_week_dates_function start ------------------------ ')
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
  # localhost_print_function(' ------------------------ get_week_dates_function end ------------------------ ')
  return weekdays_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def employees_quiz_open_close_notifications():
  localhost_print_function(' ------------------------ employees_quiz_open_close_notifications start ------------------------ ')
  # ------------------------ open connection start ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ open connection end ------------------------
  # ------------------------ get all groups start ------------------------
  db_groups_arr_of_dict = select_manual_function(postgres_connection, postgres_cursor, 'select_groups_1')
  # ------------------------ get all groups end ------------------------
  # ------------------------ loop all groups start ------------------------
  for i_group_dict in db_groups_arr_of_dict:
    if i_group_dict['fk_company_name'] != 'gmail':
      continue
    localhost_print_function(f"i_group_dict | type: {type(i_group_dict)} | {i_group_dict}")
    # ------------------------ get all emails with group start ------------------------
    db_user_emails_arr_of_dicts = select_manual_function(postgres_connection, postgres_cursor, 'select_user_emails_1', i_group_dict['fk_company_name'])
    # ------------------------ get all emails with group end ------------------------
    # ------------------------ get latest test + status start ------------------------
    i_group_status = 'no latest test'
    latest_test_id = None
    db_latest_test_dict = {}
    db_latest_test_arr = select_manual_function(postgres_connection, postgres_cursor, 'select_latest_test_1', i_group_dict['public_group_id'])
    if db_latest_test_arr != None and db_latest_test_arr != []:
      db_latest_test_dict = db_latest_test_arr[0]
      i_group_status = 'at least 1 test exists'
      latest_test_id = db_latest_test_dict['id']
      latest_test_start_timestamp = timestamp_offset_convert_function(db_latest_test_dict['start_timestamp'])
      latest_test_end_timestamp = timestamp_offset_convert_function(db_latest_test_dict['end_timestamp'])
      current_timestamp = get_current_timestamp_function()
      if latest_test_end_timestamp >= current_timestamp:
        latest_test_remainder_timestamp = latest_test_end_timestamp - current_timestamp
        latest_test_remainder_days = latest_test_remainder_timestamp.days
        latest_test_remainder_hours = ((latest_test_remainder_timestamp.seconds / 60) / 60)
        if latest_test_remainder_days >= 0:
          i_group_status = 'latest test is open'
          if latest_test_remainder_hours <= 1:
            i_group_status = 'latest test is open with less than 1 hour'
      else:
        i_group_status = 'latest test is closed'
    # ------------------------ get latest test + status end ------------------------
    # ------------------------ get all group settings start ------------------------
    db_group_settings_arr_of_dict = select_manual_function(postgres_connection, postgres_cursor, 'select_group_settings_1', i_group_dict['public_group_id'])
    # ------------------------ get all group settings end ------------------------
    # ------------------------ if latest quiz closed, check cadence to send next email start ------------------------
    check_correct_cadence = False
    if i_group_status == 'latest test is closed':
      if db_group_settings_arr_of_dict == None or db_group_settings_arr_of_dict == []:
        check_correct_cadence = True
      else:
        db_group_settings_dict = db_group_settings_arr_of_dict[0]
        latest_test_dates_of_week_end_arr = get_week_dates_function(latest_test_end_timestamp.date())
        monday_of_lastest_test_end_week = latest_test_dates_of_week_end_arr[0]
        if db_group_settings_dict['cadence'] == 'Weekly':
          should_be_this_weeks_monday = monday_of_lastest_test_end_week + timedelta(days=7)
        if db_group_settings_dict['cadence'] == 'Biweekly':
          should_be_this_weeks_monday = monday_of_lastest_test_end_week + timedelta(days=14)
        if db_group_settings_dict['cadence'] == 'Monthly':
          should_be_this_weeks_monday = monday_of_lastest_test_end_week + timedelta(days=28)
        should_be_this_weeks_monday = timestamp_offset_convert_function(should_be_this_weeks_monday)
        if current_timestamp >= should_be_this_weeks_monday:
          check_correct_cadence = True
    # ------------------------ if latest quiz closed, check cadence to send next email end ------------------------
  # ------------------------ loop all groups end ------------------------
  # ------------------------ close connection start ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ close connection end ------------------------
  localhost_print_function(' ------------------------ employees_quiz_open_close_notifications end ------------------------ ')
  return True
# ------------------------ individual function end ------------------------

# ------------------------ run function start ------------------------
if __name__ == "__main__":
  employees_quiz_open_close_notifications()
# ------------------------ run function end ------------------------
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os, time
from datetime import datetime, timedelta
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from website.backend.candidates.sql_statements.sql_statements_select_individual.select_todays_pending_schedules import select_todays_pending_schedules_function
from website.backend.candidates.sql_statements.sql_statements_insert_individual.insert_email_sent_row import insert_email_sent_row_function
from website.backend.candidates.send_emails import send_email_template_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
# ------------------------ imports end ------------------------

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
  # Goal = '2022-10-14 06:43:18'
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

# ------------------------ main start ------------------------
def job_send_schedule_email_assessment_link_function():
  localhost_print_function('=========================================== job_send_schedule_email_assessment_link_function START ===========================================')
  # ------------------------ set timezone start ------------------------
  # Set the timezone of the application when user creates account is will be in US/Easterm time
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  # ------------------------ set timezone end ------------------------
  # ------------------------ current time start ------------------------  
  current_datetime_str = datetime.now().strftime('%m-%d-%Y')
  # ------------------------ current time end ------------------------  
  # ------------------------ Connect to Postgres DB START ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ Connect to Postgres DB END ------------------------
  # ------------------------ pull from db start ------------------------
  result_schedules_arr = select_todays_pending_schedules_function(postgres_connection, postgres_cursor, current_datetime_str)
  # ------------------------ pull from db end ------------------------
  # ------------------------ loop through each schedule item start ------------------------
  for i_schedule_arr in result_schedules_arr:
    # ------------------------ assign variables start ------------------------
    i_schedule_arr_id = i_schedule_arr[0]
    i_schedule_arr_created_timestamp = i_schedule_arr[1]
    i_schedule_arr_user_id_fk = i_schedule_arr[2]
    i_schedule_arr_assessment_id_fk = i_schedule_arr[3]
    i_schedule_arr_assessment_name = i_schedule_arr[4]
    i_schedule_arr_email = i_schedule_arr[5]
    i_schedule_arr_send_date = i_schedule_arr[6]
    i_schedule_arr_send_time = i_schedule_arr[7]
    i_schedule_arr_send_timezone = i_schedule_arr[8]
    i_schedule_arr_candidate_status = i_schedule_arr[9]
    i_schedule_arr_expiring_url = i_schedule_arr[10]
    # ------------------------ assign variables end ------------------------
    # ------------------------ convert to goal send time format start ------------------------
    db_schedule_obj_goal_timestamp = build_out_datetime_from_parts_function(i_schedule_arr_send_date, i_schedule_arr_send_time, i_schedule_arr_send_timezone)
    current_datetime_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_datetime_datetime = datetime.strptime(current_datetime_str, '%Y-%m-%d %H:%M:%S')
    if current_datetime_datetime > db_schedule_obj_goal_timestamp:
      # ------------------------ send email start ------------------------
      output_to_email = i_schedule_arr_email
      output_subject = f'Triviafy Candidate Assessment: {i_schedule_arr_assessment_name}'
      output_body = f"Hi there,\n\nYour Triviafy candidate assessment is ready!\nThe following link will expire 1 hour from the time you receive this email.\n\nPlease visit the following link to complete your assessment: https://triviafy.com/candidates/assessment/{i_schedule_arr_expiring_url} \n\nBest,\nTriviafy"
      send_email_template_function(output_to_email, output_subject, output_body)
      # ------------------------ send email end ------------------------
      # ------------------------ insert row db start ------------------------
      row_id = create_uuid_function('email_test_')
      row_created_timestamp = create_timestamp_function()
      insert_input_arr = [row_id, row_created_timestamp, 'job', output_to_email, i_schedule_arr_expiring_url, output_subject, output_body]
      insert_email_sent_row_function(postgres_connection, postgres_cursor, insert_input_arr)
      # ------------------------ insert row db end ------------------------
    else:
      pass
    # ------------------------ convert to goal send time format end ------------------------
  # ------------------------ loop through each schedule item end ------------------------
  # ------------------------ Close Postgres DB START ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Close Postgres DB END ------------------------
  localhost_print_function('=========================================== job_send_schedule_email_assessment_link_function END ===========================================')
  return True
# ------------------------ main end ------------------------

# ------------------------ run main start ------------------------
if __name__ == "__main__":
  job_send_schedule_email_assessment_link_function()
# ------------------------ run main end ------------------------
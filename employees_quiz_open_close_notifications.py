# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.employees import select_manual_function
from backend.db.queries.insert_queries.employees import insert_manual_function
from datetime import datetime, timedelta
import os, time
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
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
def send_email_template_function(output_email, output_subject_line, output_message_content):
  localhost_print_function(' ------------------------ send_email_template_function start ------------------------ ')
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY_TRIVIAFY'))
  from_email = Email(email = os.environ.get('TRIVIAFY_SUPPORT_EMAIL'), name = "Triviafy")
  to_email = To(output_email)
  subject = output_subject_line
  content = Content("text/plain", output_message_content)
  mail = Mail(from_email, to_email, subject, content)
  mail_json = mail.get()
  try:
    sg.client.mail.send.post(request_body=mail_json)
    localhost_print_function('email sent successfully! ' + output_subject_line + " - To: " + output_email)
  except:
    localhost_print_function('email did not send successfully...' + output_subject_line)
    localhost_print_function(' ------------------------ send_email_template_function end ------------------------ ')
    return False
  localhost_print_function(' ------------------------ send_email_template_function end ------------------------ ')
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def breakup_email_function(input_email):
  # localhost_print_function(' ------------------------ breakup_email_function start ------------------------ ')
  email_arr = input_email.split('@')
  try:
    email_arr = email_arr[0].split('.')
  except:
    pass
  # localhost_print_function(' ------------------------ breakup_email_function end ------------------------ ')
  return email_arr[0].title()
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
    # ------------------------ get latest test + status start ------------------------
    i_group_status = 'no latest test'
    latest_test_id = None
    db_latest_test_dict = {}
    db_latest_test_arr = select_manual_function(postgres_connection, postgres_cursor, 'select_latest_test_1', i_group_dict['public_group_id'])
    if db_latest_test_arr != None and db_latest_test_arr != []:
      db_latest_test_dict = db_latest_test_arr[0]
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
    # ------------------------ if latest quiz closed, check cadence to send next email start ------------------------
    db_group_settings_arr_of_dict = select_manual_function(postgres_connection, postgres_cursor, 'select_group_settings_1', i_group_dict['public_group_id'])
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
    # ------------------------ loop each user email start ------------------------
    db_user_emails_arr_of_dicts = select_manual_function(postgres_connection, postgres_cursor, 'select_user_emails_1', i_group_dict['fk_company_name'])
    for i_dict in db_user_emails_arr_of_dicts:
      output_to_email = i_dict['email']
      guessed_name = breakup_email_function(i_dict['email'])
      todays_date_str = datetime.today().strftime('%m/%d/%Y')   # 2023-02-25
      # ------------------------ send email start ------------------------
      if i_group_status == 'no latest test':
        output_subject = f'Action Required: First Team Trivia Contest {todays_date_str}'
        db_email_already_sent = select_manual_function(postgres_connection, postgres_cursor, 'select_check_email_sent_1', output_to_email, output_subject)
        if db_email_already_sent == None or db_email_already_sent == []:
          output_body = f"Hi {guessed_name},\n\nYour team's latest trivia contest https://triviafy.com/employees/dashboard \n\nBest,\nTriviafy Support Team\nReply 'stop' to unsubscribe."
          send_email_template_function(output_to_email, output_subject, output_body)
          # ------------------------ insert to db start ------------------------
          send_email_id = create_uuid_function('job_')
          send_email_created_timestamp = create_timestamp_function()
          insert_inputs_arr = [send_email_id, send_email_created_timestamp, 'job_heroku', output_to_email, output_subject, output_body]
          insert_manual_function(postgres_connection, postgres_cursor, 'insert_email_1', insert_inputs_arr)
          # ------------------------ insert to db end ------------------------
        else:
          pass
      # ------------------------ send email end ------------------------
      # ------------------------ check if grading exists start ------------------------
      i_user_completed_latest_test = False
      db_test_graded_arr_of_dicts = select_manual_function(postgres_connection, postgres_cursor, 'select_test_graded_1', i_dict['id'], latest_test_id)
      if db_test_graded_arr_of_dicts != None and db_test_graded_arr_of_dicts != []:
        i_user_completed_latest_test = True
      # ------------------------ check if grading exists end ------------------------
      # ------------------------ email only people who have not yet participated start ------------------------
      if i_user_completed_latest_test == False:
        # ------------------------ send email start ------------------------
        if i_group_status == 'latest test is open':
          output_subject = f'Action Required: Team Trivia Contest Open {todays_date_str}'
          db_email_already_sent = select_manual_function(postgres_connection, postgres_cursor, 'select_check_email_sent_1', output_to_email, output_subject)
          if db_email_already_sent == None or db_email_already_sent == []:
            output_body = f"Hi {guessed_name},\n\nYour team's latest trivia contest https://triviafy.com/employees/dashboard \n\nBest,\nTriviafy Support Team\nReply 'stop' to unsubscribe."
            send_email_template_function(output_to_email, output_subject, output_body)
            # ------------------------ insert to db start ------------------------
            send_email_id = create_uuid_function('job_')
            send_email_created_timestamp = create_timestamp_function()
            insert_inputs_arr = [send_email_id, send_email_created_timestamp, 'job_heroku', output_to_email, output_subject, output_body]
            insert_manual_function(postgres_connection, postgres_cursor, 'insert_email_1', insert_inputs_arr)
            # ------------------------ insert to db end ------------------------
          else:
            pass
        # ------------------------ send email end ------------------------
        # ------------------------ send email start ------------------------
        if i_group_status == 'latest test is open with less than 1 hour':
          output_subject = f'Action Required: 1 Hour Left In Team Trivia Contest {todays_date_str}'
          db_email_already_sent = select_manual_function(postgres_connection, postgres_cursor, 'select_check_email_sent_1', output_to_email, output_subject)
          if db_email_already_sent == None or db_email_already_sent == []:
            output_body = f"Hi {guessed_name},\n\nOne hour left to enter your team's latest trivia contest https://triviafy.com/employees/dashboard \n\nBest,\nTriviafy Support Team\nReply 'stop' to unsubscribe."
            send_email_template_function(output_to_email, output_subject, output_body)
            # ------------------------ insert to db start ------------------------
            send_email_id = create_uuid_function('job_')
            send_email_created_timestamp = create_timestamp_function()
            insert_inputs_arr = [send_email_id, send_email_created_timestamp, 'job_heroku', output_to_email, output_subject, output_body]
            insert_manual_function(postgres_connection, postgres_cursor, 'insert_email_1', insert_inputs_arr)
            # ------------------------ insert to db end ------------------------
          else:
            pass
        # ------------------------ send email end ------------------------
      # ------------------------ email only people who have not yet participated end ------------------------
      # ------------------------ email everyone with winner once quiz is closed start ------------------------
      
      # ------------------------ email everyone with winner once quiz is closed end ------------------------
    # ------------------------ loop each user email end ------------------------
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
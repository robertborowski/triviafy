# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.employees import select_manual_function
from backend.db.queries.insert_queries.employees import insert_manual_function
from backend.db.queries.update_queries.employees import update_manual_function
from datetime import datetime, timedelta, date
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
def send_email_template_function(output_email, output_subject_line, output_message_content):
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY_TRIVIAFY'))
  from_email = Email(email = os.environ.get('TRIVIAFY_SUPPORT_EMAIL'), name = "Triviafy")
  to_email = To(output_email)
  subject = output_subject_line
  content = Content("text/html", output_message_content)
  mail = Mail(from_email, to_email, subject, content)
  mail_json = mail.get()
  try:
    sg.client.mail.send.post(request_body=mail_json)
    localhost_print_function('email sent successfully! ' + output_subject_line + " - To: " + output_email)
  except:
    localhost_print_function('email did not send successfully...' + output_subject_line)
    return False
  return True
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
def create_celebrations_test_function(postgres_connection, postgres_cursor, db_question_dict, i_celebrate_dict, i_product, test_group_id):
  # ------------------------ variables for insert start ------------------------
  todays_str = datetime.today().strftime('%m-%d-%Y')
  test_id = create_uuid_function('test_')
  test_created_timestamp = create_timestamp_function()
  fk_group_id = test_group_id
  timezone = 'EST'
  start_day = datetime.now().strftime("%A")
  start_time = '4 AM'
  start_timestamp = build_out_datetime_from_parts_function(todays_str, start_time, timezone)
  end_day = datetime.now().strftime("%A")
  end_time = '8 PM'
  end_timestamp = build_out_datetime_from_parts_function(todays_str, end_time, timezone)
  cadence = i_product
  total_questions = int(1)
  question_type = 'Multiple choice'
  categories = 'all_categories'
  question_ids = db_question_dict['id']
  question_types_order = 'Multiple choice'
  status = 'Open'
  product = i_product
  # ------------------------ variables for insert end ------------------------
  # ------------------------ insert to db start ------------------------
  insert_inputs_arr = [test_id,test_created_timestamp,fk_group_id,timezone,start_day,start_time,start_timestamp,end_day,end_time,end_timestamp,cadence,total_questions,question_type,categories,question_ids,question_types_order,status,product]
  insert_manual_function(postgres_connection, postgres_cursor, 'insert_test_1', insert_inputs_arr)
  # ------------------------ insert to db end ------------------------
  return test_id
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def insert_question_used_for_test_function(postgres_connection, postgres_cursor, fk_group_id, fk_question_id, fk_test_id, product):
  # ------------------------ variables for insert start ------------------------
  used_id = create_uuid_function('used_')
  used_created_timestamp = create_timestamp_function()
  fk_group_id = fk_group_id
  fk_question_id = fk_question_id
  fk_test_id = fk_test_id
  product = product
  # ------------------------ variables for insert end ------------------------
  # ------------------------ insert to db start ------------------------
  insert_inputs_arr = [used_id,used_created_timestamp,fk_group_id,fk_question_id,fk_test_id,product]
  insert_manual_function(postgres_connection, postgres_cursor, 'insert_used_1', insert_inputs_arr)
  # ------------------------ insert to db end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def run_job_function():
  # ------------------------ get todays variables start ------------------------
  today = date.today()
  current_day = today.day
  current_month = today.month
  current_year = today.year
  todays_date_str = datetime.today().strftime('%m/%d/%Y')   # 02/25/2023
  # ------------------------ get todays variables end ------------------------
  # ------------------------ open connection start ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ open connection end ------------------------
  # ------------------------ lookup/celebrate birthday start ------------------------
  db_arr_of_dict_if_birthday_today = select_manual_function(postgres_connection, postgres_cursor, 'select_if_birthday_today', current_month, current_day)
  # ------------------------ if no birthday today start ------------------------
  if db_arr_of_dict_if_birthday_today == None or db_arr_of_dict_if_birthday_today == [] or len(db_arr_of_dict_if_birthday_today) == 0:
    print('no birthdays today')
  # ------------------------ if no birthday today end ------------------------
  # ------------------------ if yes birthday today start ------------------------
  else:
    for i_birthday_dict in db_arr_of_dict_if_birthday_today:
      # ------------------------ get total teammate count start ------------------------
      db_arr_of_dict_total_teammates = select_manual_function(postgres_connection, postgres_cursor, 'select_total_teammates', i_birthday_dict['fk_group_id'])
      if len(db_arr_of_dict_total_teammates) == 1:
        localhost_print_function(f"group_id: {i_birthday_dict['fk_group_id']} = 1 total user. No test created because no one else to celebrate.")
        continue
      # ------------------------ get total teammate count end ------------------------
      # ------------------------ get question obj start ------------------------
      db_arr_of_dict_question = select_manual_function(postgres_connection, postgres_cursor, 'select_question_1', i_birthday_dict['fk_question_id'])
      db_question_dict = db_arr_of_dict_question[0]
      db_group_id = db_question_dict['fk_group_id']
      # ------------------------ get question obj end ------------------------
      # ------------------------ create test start ------------------------
      create_test_id = None
      new_test_created = False
      db_arr_of_dict_test_check = select_manual_function(postgres_connection, postgres_cursor, 'select_test_1', 'birthday', i_birthday_dict['fk_question_id'])
      if db_arr_of_dict_test_check == None or db_arr_of_dict_test_check == []:
        create_test_id = create_celebrations_test_function(postgres_connection, postgres_cursor, db_question_dict, i_birthday_dict, 'birthday', db_group_id)
        new_test_created = True
      else:
        create_test_id = db_arr_of_dict_test_check[0]['id']
      # ------------------------ create test end ------------------------
      # ------------------------ if new test created start ------------------------
      if new_test_created == True:
        # ------------------------ add question used to db start ------------------------
        insert_question_used_for_test_function(postgres_connection, postgres_cursor, db_group_id, i_birthday_dict['fk_question_id'], create_test_id, 'birthday')
        # ------------------------ add question used to db end ------------------------
        # ------------------------ update celebrations db start ------------------------
        update_input_arr = [create_test_id, i_birthday_dict['fk_question_id']]
        update_manual_function(postgres_connection, postgres_cursor, 'update_celebrations_1', update_input_arr)
        # ------------------------ update celebrations db end ------------------------
      # ------------------------ if new test created end ------------------------
      # ------------------------ get user obj start ------------------------
      db_arr_of_dict_user = select_manual_function(postgres_connection, postgres_cursor, 'select_user_2', db_question_dict['fk_user_id'])
      db_user_dict = db_arr_of_dict_user[0]
      # ------------------------ get user obj end ------------------------
      # ------------------------ get teammates obj start ------------------------
      db_arr_of_dict_teammates = select_manual_function(postgres_connection, postgres_cursor, 'select_users_1', db_user_dict['group_id'])
      # ------------------------ get teammates obj end ------------------------
      # ------------------------ loop teammates start ------------------------
      for i_teammate_dict in db_arr_of_dict_teammates:
        # ------------------------ skip birthday person start ------------------------
        if i_teammate_dict['email'] == db_user_dict['email']:
          localhost_print_function('skip sending birthday email to self')
          continue
        # ------------------------ skip birthday person end ------------------------
        # ------------------------ send email start ------------------------
        output_subject = f"Birthday Trivia for {db_user_dict['name']} ({todays_date_str})"
        db_email_already_sent = select_manual_function(postgres_connection, postgres_cursor, 'select_check_email_sent_1', i_teammate_dict['email'], output_subject)
        if db_email_already_sent == None or db_email_already_sent == []:
          output_body = f"<p>Hi {i_teammate_dict['name']},</p>\
                          <p>Today is {db_user_dict['name']}'s birthday! {db_question_dict['question']}</p>\
                          <p>A: <a href='https://triviafy.com/dashboard'>{db_question_dict['option_a']}</a></p>\
                          <p>B: <a href='https://triviafy.com/dashboard'>{db_question_dict['option_b']}</a></p>\
                          <p>C: <a href='https://triviafy.com/dashboard'>{db_question_dict['option_c']}</a></p>\
                          <p>D: <a href='https://triviafy.com/dashboard'>{db_question_dict['option_d']}</a></p>\
                          <p style='margin:0;'>Best,</p>\
                          <p style='margin:0;'>Triviafy Support Team</p>\
                          <p style='margin:0;font-size:10px;'>Reply 'stop' to unsubscribe.</p>"
          send_email_template_function(i_teammate_dict['email'], output_subject, output_body)
          # ------------------------ insert to db start ------------------------
          send_email_id = create_uuid_function('job_')
          send_email_created_timestamp = create_timestamp_function()
          insert_inputs_arr = [send_email_id, send_email_created_timestamp, 'job_celebrate_birthday_email', i_teammate_dict['email'], output_subject, output_body]
          insert_manual_function(postgres_connection, postgres_cursor, 'insert_email_1', insert_inputs_arr)
          # ------------------------ insert to db end ------------------------
        else:
          localhost_print_function(f"already sent {i_teammate_dict['email']} | {output_subject}")
          pass
        # ------------------------ send email end ------------------------
      # ------------------------ loop teammates end ------------------------
  # ------------------------ if yes birthday today end ------------------------
  # ------------------------ lookup/celebrate birthday end ------------------------
  # ------------------------ lookup/celebrate anniversary start ------------------------
  if int(current_day) == int(1):
    db_arr_of_dict_if_anniversary_today = select_manual_function(postgres_connection, postgres_cursor, 'select_if_job_start_date_today', current_month, current_year)
    # ------------------------ if no anniversary today start ------------------------
    if db_arr_of_dict_if_anniversary_today == None or db_arr_of_dict_if_anniversary_today == [] or len(db_arr_of_dict_if_anniversary_today) == 0:
      print('no anniversary today')
    # ------------------------ if no anniversary today end ------------------------
    # ------------------------ if yes anniversary today start ------------------------
    else:
      for i_anniversary_dict in db_arr_of_dict_if_anniversary_today:
        # ------------------------ get total years start ------------------------
        total_years_working_str = None
        total_years_working_int = int(current_year) - int(i_anniversary_dict['celebrate_year'])
        if total_years_working_int == 1:
          total_years_working_str = f'{total_years_working_int} year'
        if total_years_working_int > 1:
          total_years_working_str = f'{total_years_working_int} years'
        if total_years_working_int < 1:
          localhost_print_function(f"Incorrect input year")
          break
        # ------------------------ get total years end ------------------------
        # ------------------------ get question obj start ------------------------
        db_arr_of_dict_question = select_manual_function(postgres_connection, postgres_cursor, 'select_question_1', i_anniversary_dict['fk_question_id'])
        db_question_dict = db_arr_of_dict_question[0]
        # ------------------------ get question obj end ------------------------
        # ------------------------ get user obj start ------------------------
        db_arr_of_dict_user = select_manual_function(postgres_connection, postgres_cursor, 'select_user_2', db_question_dict['fk_user_id'])
        db_user_dict = db_arr_of_dict_user[0]
        # ------------------------ get user obj end ------------------------
        # ------------------------ get teammates obj start ------------------------
        db_arr_of_dict_teammates = select_manual_function(postgres_connection, postgres_cursor, 'select_users_1', db_user_dict['group_id'])
        # ------------------------ get teammates obj end ------------------------
        # ------------------------ loop teammates start ------------------------
        for i_teammate_dict in db_arr_of_dict_teammates:
          # ------------------------ skip anniversary person start ------------------------
          if i_teammate_dict['email'] == db_user_dict['email']:
            localhost_print_function('skip sending job_start_date email to self')
            continue
          # ------------------------ skip anniversary person end ------------------------
          # ------------------------ send email start ------------------------
          output_subject = f"Work Anniversary Trivia for {db_user_dict['name']} ({todays_date_str})"
          db_email_already_sent = select_manual_function(postgres_connection, postgres_cursor, 'select_check_email_sent_1', i_teammate_dict['email'], output_subject)
          if db_email_already_sent == None or db_email_already_sent == []:
            output_body = f"<p>Hi {i_teammate_dict['name']},</p>\
                            <p>Today is {db_user_dict['name']}'s work anniversary of {total_years_working_str}! {db_question_dict['question']}</p>\
                            <p>A: <a href='https://triviafy.com/dashboard'>{db_question_dict['option_a']}</a></p>\
                            <p>B: <a href='https://triviafy.com/dashboard'>{db_question_dict['option_b']}</a></p>\
                            <p>C: <a href='https://triviafy.com/dashboard'>{db_question_dict['option_c']}</a></p>\
                            <p>D: <a href='https://triviafy.com/dashboard'>{db_question_dict['option_d']}</a></p>\
                            <p style='margin:0;'>Best,</p>\
                            <p style='margin:0;'>Triviafy Support Team</p>\
                            <p style='margin:0;font-size:10px;'>Reply 'stop' to unsubscribe.</p>"
            send_email_template_function(i_teammate_dict['email'], output_subject, output_body)
            # ------------------------ insert to db start ------------------------
            send_email_id = create_uuid_function('job_')
            send_email_created_timestamp = create_timestamp_function()
            insert_inputs_arr = [send_email_id, send_email_created_timestamp, 'job_celebrate_anniversary_email', i_teammate_dict['email'], output_subject, output_body]
            insert_manual_function(postgres_connection, postgres_cursor, 'insert_email_1', insert_inputs_arr)
            # ------------------------ insert to db end ------------------------
          else:
            localhost_print_function(f"already sent {i_teammate_dict['email']} | {output_subject}")
            pass
          # ------------------------ send email end ------------------------
        # ------------------------ loop teammates end ------------------------
    # ------------------------ if yes anniversary today end ------------------------
  else:
    localhost_print_function(f"Today is not the first of the month")
  # ------------------------ lookup/celebrate anniversary end ------------------------
  # ------------------------ close connection start ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ close connection end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ run function start ------------------------
if __name__ == "__main__":
  run_job_function()
# ------------------------ run function end ------------------------
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
      # ------------------------ get question obj start ------------------------
      db_arr_of_dict_question = select_manual_function(postgres_connection, postgres_cursor, 'select_question_1', i_birthday_dict['fk_question_id'])
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
        # ------------------------ skip birthday person start ------------------------
        if i_teammate_dict['email'] == db_user_dict['email']:
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
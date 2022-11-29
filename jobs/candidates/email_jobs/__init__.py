# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os, time
from datetime import datetime, timedelta
from website.backend.candidates.sql_statements.sql_statements_select_individual.select_all_collected_emails import select_all_collected_emails_function
from website.backend.candidates.sql_statements.sql_statements_insert_individual.insert_email_sent_row import insert_email_sent_row_function
from website.backend.candidates.send_emails import send_email_template_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website.backend.candidates.sql_statements.sql_statements_select_individual.select_all_users import select_all_users_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
# ------------------------ main start ------------------------
def job_candidates_email_all_collected_emails_function(postgres_connection, postgres_cursor):
  localhost_print_function('=========================================== job_candidates_email_all_collected_emails_function START ===========================================')
  # ------------------------ pull from db start ------------------------
  all_users_arr = select_all_collected_emails_function(postgres_connection, postgres_cursor)
  # ------------------------ pull from db end ------------------------
  # ------------------------ if none start ------------------------
  if all_users_arr == None:
    localhost_print_function('no schedules to send out today')
    localhost_print_function('=========================================== job_candidates_email_all_collected_emails_function_function END ===========================================')
    return True
  # ------------------------ if none end ------------------------
  # ------------------------ loop through each schedule item start ------------------------
  failed_emails_arr = []
  for i_user_arr in all_users_arr:
    # ------------------------ assign variables start ------------------------
    i_user_arr_id = i_user_arr[0]
    i_user_arr_created_timestamp = i_user_arr[1].strftime('%m/%d/%Y')
    i_user_arr_email = i_user_arr[2]
    # ------------------------ email only self start ------------------------
    # ------------------------ assign variables end -----------------------
    run_test_email = os.environ.get('RUN_TEST_EMAIL')
    if i_user_arr_email != run_test_email:
      print(f'skip: {i_user_arr_email}')
      continue
    # ------------------------ email only self end -------------------------
    # ------------------------ convert to goal send time format start ------------------------
    todays_date = datetime.today().strftime('%m-%d-%Y')
    try:
      # ------------------------ send email start ------------------------
      output_to_email = i_user_arr_email
      add_link = 'https://triviafy.com/candidates/signup'
      output_subject = f'Send Pre Employment Tests In 30 Seconds - Triviafy {todays_date}'
      output_body = f"Hi there,\n\nYou signed up to learn more about Triviafy's pre employment testing tool. You can create your candidates first pre employment test in less than 30 seconds at {add_link}\n\nBest,\nTriviafy\n\nReply 'STOP' to opt out."
      send_email_template_function(output_to_email, output_subject, output_body)
      # ------------------------ send email end ------------------------
      # ------------------------ insert row db start ------------------------
      row_id = create_uuid_function('email_ann_')
      row_created_timestamp = create_timestamp_function()
      insert_input_arr = [row_id, row_created_timestamp, 'job', output_to_email, 'announcement', output_subject, output_body]
      insert_email_sent_row_function(postgres_connection, postgres_cursor, insert_input_arr)
      # ------------------------ insert row db end ------------------------
      # ------------------------ convert to goal send time format end ------------------------
    except:
      failed_emails_arr.append(i_user_arr_email)
      pass
  # ------------------------ loop through each schedule item end ------------------------
  localhost_print_function(f'len_failed_emails_arr: {len(failed_emails_arr)} | failed_emails_arr: {failed_emails_arr}')
  localhost_print_function('=========================================== job_candidates_email_all_collected_emails_function_function END ===========================================')
  return True
# ------------------------ main end ------------------------
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
# ------------------------ main start ------------------------
def job_candidates_email_all_users_function(postgres_connection, postgres_cursor):
  localhost_print_function('=========================================== job_candidates_email_all_users_function START ===========================================')
  # ------------------------ pull from db start ------------------------
  all_users_arr = select_all_users_function(postgres_connection, postgres_cursor)
  # ------------------------ pull from db end ------------------------
  # ------------------------ if none start ------------------------
  if all_users_arr == None:
    localhost_print_function('no schedules to send out today')
    localhost_print_function('=========================================== job_candidates_email_all_users_function_function END ===========================================')
    return True
  # ------------------------ if none end ------------------------
  # ------------------------ loop through each schedule item start ------------------------
  failed_emails_arr = []
  for i_user_arr in all_users_arr:
    # ------------------------ assign variables start ------------------------
    i_user_arr_id = i_user_arr[0]
    i_user_arr_created_timestamp = i_user_arr[1].strftime('%m/%d/%Y')
    i_user_arr_email = i_user_arr[2]
    # ------------------------ email only self start ------------------------
    run_test_email = os.environ.get('RUN_TEST_EMAIL')
    if i_user_arr_email != run_test_email:
      print(f'skip: {i_user_arr_email}')
      continue
    # ------------------------ email only self end ------------------------
    i_user_arr_name = i_user_arr[4]
    if i_user_arr_name == None or i_user_arr_name == '':
      i_user_arr_name = 'there'
    i_user_arr_company_name = i_user_arr[5]
    # ------------------------ assign variables end ------------------------
    # ------------------------ convert to goal send time format start ------------------------
    todays_date = datetime.today().strftime('%m-%d-%Y')
    try:
      # ------------------------ send email start ------------------------
      output_to_email = i_user_arr_email
      add_link = 'https://triviafy.com/candidates/assessment/new'
      output_subject = f'Pre Employment Tests In 30 Seconds - Triviafy {todays_date}'
      output_body = f"Hi {i_user_arr_name},\n\nThank you for creating an account with Triviafy. We noticed that you have not yet sent out any assessments to candidates.\nAre the current assessment questions & categories not what you had in mind? Do you have any questions about our product or feedback about your experience?\n\nYou can create/send a pre employment test in less than 30 seconds at {add_link}\n\nBest,\nTriviafy\n\nReply 'STOP' to opt out."
      send_email_template_function(output_to_email, output_subject, output_body)
      # ------------------------ send email end ------------------------
      # ------------------------ insert row db start ------------------------
      row_id = create_uuid_function('email_ann_')
      row_created_timestamp = create_timestamp_function()
      insert_input_arr = [row_id, row_created_timestamp, 'job', output_to_email, 'announcement', output_subject, output_body]
      insert_email_sent_row_function(postgres_connection, postgres_cursor, insert_input_arr)
      # ------------------------ insert row db end ------------------------
      # ------------------------ convert to goal send time format end ------------------------
    except:
      failed_emails_arr.append(i_user_arr_email)
      pass
  # ------------------------ loop through each schedule item end ------------------------
  localhost_print_function(f'len_failed_emails_arr: {len(failed_emails_arr)} | failed_emails_arr: {failed_emails_arr}')
  localhost_print_function('=========================================== job_candidates_email_all_users_function_function END ===========================================')
  return True
# ------------------------ main end ------------------------
# ------------------------ individual function end ------------------------


# ------------------------ individual function start ------------------------
# ------------------------ main start ------------------------
def job_candidates_send_article_to_all_users_function(postgres_connection, postgres_cursor):
  localhost_print_function('=========================================== job_candidates_send_article_to_all_users_function START ===========================================')
  # ------------------------ pull from db start ------------------------
  all_users_arr_signed_up = select_all_users_function(postgres_connection, postgres_cursor)
  all_users_arr_collected_emails = select_all_collected_emails_function(postgres_connection, postgres_cursor)
  # ------------------------ pull from db end ------------------------
  # ------------------------ if none start ------------------------
  if all_users_arr_signed_up == None or all_users_arr_collected_emails == None:
    localhost_print_function('no emails to send out today')
    localhost_print_function('=========================================== job_candidates_send_article_to_all_users_function END ===========================================')
    return True
  # ------------------------ if none end ------------------------
  # ------------------------ get all emails arr start ------------------------
  all_user_emails_arr = []
  for i in all_users_arr_signed_up:
    if i[2] not in all_user_emails_arr:
      all_user_emails_arr.append(i[2])
  for i in all_users_arr_collected_emails:
    if i[2] not in all_user_emails_arr:
      all_user_emails_arr.append(i[2])
  # ------------------------ get all emails arr end ------------------------
  # ------------------------ loop through each schedule item start ------------------------
  failed_emails_arr = []
  for i_email in all_user_emails_arr:
    # ------------------------ email only self start ------------------------
    run_test_email = os.environ.get('RUN_TEST_EMAIL')
    if i_email != run_test_email:
      print(f'skip: {i_email}')
      continue
    # ------------------------ email only self end ------------------------
    todays_date = datetime.today().strftime('%m-%d-%Y')
    try:
      # ------------------------ send email start ------------------------
      output_to_email = i_email
      add_link = 'https://triviafy.com/candidates/blog/0002'
      output_subject = f'3 Ways To Hire An Excel Expert - Triviafy {todays_date}'
      output_body = f"Hi there,\n\nNew blog post from the friendliest pre employment testing platform, titled '3 Ways To Hire An Excel Expert' at {add_link}\n\nReply 'STOP' to opt out.\n\nBest,\nTriviafy"
      send_email_template_function(output_to_email, output_subject, output_body)
      # ------------------------ send email end ------------------------
      # ------------------------ insert row db start ------------------------
      row_id = create_uuid_function('email_ann_')
      row_created_timestamp = create_timestamp_function()
      insert_input_arr = [row_id, row_created_timestamp, 'job', output_to_email, 'announcement_blog_post', output_subject, output_body]
      insert_email_sent_row_function(postgres_connection, postgres_cursor, insert_input_arr)
      # ------------------------ insert row db end ------------------------
      # ------------------------ convert to goal send time format end ------------------------
    except:
      failed_emails_arr.append(i_email)
      pass
  # ------------------------ loop through each schedule item end ------------------------
  localhost_print_function(f'len_failed_emails_arr: {len(failed_emails_arr)} | failed_emails_arr: {failed_emails_arr}')
  localhost_print_function('=========================================== job_candidates_send_article_to_all_users_function END ===========================================')
  return True
# ------------------------ main end ------------------------
# ------------------------ individual function end ------------------------
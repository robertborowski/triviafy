# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os, time
from datetime import datetime, timedelta
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from website.backend.candidates.sql_statements.sql_statements_select_individual.select_all_collected_emails import select_all_collected_emails_function
from website.backend.candidates.sql_statements.sql_statements_insert_individual.insert_email_sent_row import insert_email_sent_row_function
from website.backend.candidates.send_emails import send_email_template_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
# ------------------------ imports end ------------------------

# ------------------------ main start ------------------------
def job_candidates_email_all_collected_emails_function():
  localhost_print_function('=========================================== job_candidates_email_all_collected_emails_function START ===========================================')
  # ------------------------ Connect to Postgres DB START ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ Connect to Postgres DB END ------------------------
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
    # if i_user_arr_email != 'robjborowski@gmail.com':
    #   continue
    # ------------------------ email only self end -------------------------
    # ------------------------ convert to goal send time format start ------------------------
    try:
      # ------------------------ send email start ------------------------
      output_to_email = i_user_arr_email
      add_link = 'https://triviafy.com/candidates/login'
      output_subject = f'Triviafy Official Release: Candidate Screening Tool'
      output_body = f"Hi there,\n\nYou signed up for 'Triviafy Candidates' on {i_user_arr_created_timestamp}, Triviafy's candidate screening tool is now LIVE!\n\nLogin to start screening candidates {add_link}\n\n\nReply 'STOP' to opt out.\n\nBest,\nTriviafy"
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
  # ------------------------ Close Postgres DB START ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Close Postgres DB END ------------------------
  localhost_print_function(f'len_failed_emails_arr: {len(failed_emails_arr)} | failed_emails_arr: {failed_emails_arr}')
  localhost_print_function('=========================================== job_candidates_email_all_collected_emails_function_function END ===========================================')
  return True
# ------------------------ main end ------------------------

# ------------------------ run main start ------------------------
if __name__ == "__main__":
  job_candidates_email_all_collected_emails_function()
# ------------------------ run main end ------------------------
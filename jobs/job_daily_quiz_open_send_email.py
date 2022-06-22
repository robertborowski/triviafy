# -------------------------------------------------------------- Imports
from datetime import date
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.latest_quiz_utils.supporting_make_company_latest_quiz_utils.get_upcoming_week_dates_data_dict import get_upcoming_week_dates_data_dict_function
from backend.db.queries.select_queries.select_queries_triviafy_quiz_master_table.select_triviafy_latest_quiz_info_all_companies import select_triviafy_latest_quiz_info_all_companies_function
from backend.utils.latest_quiz_utils.supporting_make_company_latest_quiz_utils.convert_question_ids_from_string_to_arr import convert_question_ids_from_string_to_arr_function
from backend.utils.latest_quiz_utils.check_if_today_is_greater_than_equal_to_latest_quiz_start_date_utils.check_if_today_is_greater_than_equal_to_latest_quiz_start_date import check_if_today_is_greater_than_equal_to_latest_quiz_start_date_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_company_user_uuids_for_quiz_email import select_triviafy_user_login_information_table_slack_all_company_user_uuids_for_quiz_email_function
from backend.db.queries.select_queries.select_queries_triviafy_slack_messages_sent_table.select_triviafy_slack_messages_sent_table_search_user_uuid_category import select_triviafy_slack_messages_sent_table_search_user_uuid_category_function
from backend.db.queries.select_queries.select_queries_triviafy_emails_sent_table.select_triviafy_emails_sent_table_search_user_uuid_category import select_triviafy_emails_sent_table_search_user_uuid_category_function
from backend.utils.send_emails.send_email_template import send_email_template_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.db.queries.insert_queries.insert_queries_triviafy_emails_sent_table.insert_triviafy_emails_sent_table import insert_triviafy_emails_sent_table_function
from backend.db.queries.insert_queries.insert_queries_triviafy_slack_messages_sent_table.insert_triviafy_slack_messages_sent_table import insert_triviafy_slack_messages_sent_table_function
from backend.utils.slack.send_team_channel_message_utils.send_team_channel_message_quiz_open import send_team_channel_message_quiz_open_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os, time
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_one_user_incoming_webhook import select_one_user_incoming_webhook_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_channel_name import select_triviafy_user_login_information_table_channel_name_function

# -------------------------------------------------------------- Main Function
def job_daily_quiz_open_send_email_function():
  localhost_print_function('=========================================== job_daily_quiz_open_send_email_function START ===========================================')

  
  # ------------------------ Set Timezone START ------------------------
  # Set the timezone of the application when user creates account is will be in US/Easterm time
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  # ------------------------ Set Timezone END ------------------------


  # ------------------------ Get Today's Date START ------------------------
  # Today's date
  today_date = date.today()
  # Today's date, day of week
  today_day_of_week = today_date.strftime('%A')

  if today_day_of_week == 'Saturday' or today_day_of_week == 'Sunday':
    localhost_print_function('Today is Saturday or Sunday.')
    localhost_print_function('=========================================== job_daily_quiz_open_send_email_function END ===========================================')
    return True
  # ------------------------ Get Today's Date END ------------------------


  # ------------------------ Get Upcoming Week Dates START ------------------------
  this_upcoming_week_dates_dict = get_upcoming_week_dates_data_dict_function()

  start_date_monday = this_upcoming_week_dates_dict['Monday']
  start_date_tuesday = this_upcoming_week_dates_dict['Tuesday']
  start_date_wednesday = this_upcoming_week_dates_dict['Wednesday']
  start_date_thursday = this_upcoming_week_dates_dict['Thursday']
  start_date_friday = this_upcoming_week_dates_dict['Friday']
  start_date_saturday = this_upcoming_week_dates_dict['Saturday']
  start_date_sunday = this_upcoming_week_dates_dict['Sunday']
  # ------------------------ Get Upcoming Week Dates END ------------------------


  # ------------------------ Get Company Latest Quiz Info START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()

  # Get latest company quiz info
  latest_quiz_info_all_companies_arr = select_triviafy_latest_quiz_info_all_companies_function(postgres_connection, postgres_cursor, start_date_monday, start_date_tuesday, start_date_wednesday, start_date_thursday, start_date_friday, start_date_saturday, start_date_sunday)
  # ------------------------ Get Company Latest Quiz Info END ------------------------


  # ------------------------ Loop Through Each Company Latest Weekly Quiz START ------------------------
  if latest_quiz_info_all_companies_arr != None:
    # Loop through each company latest quiz
    for company_latest_quiz_arr in latest_quiz_info_all_companies_arr:
      # ------------------------ Assign Variables for Company Quiz START ------------------------
      uuid_quiz = company_latest_quiz_arr[0]                                     # str
      quiz_timestamp_created = company_latest_quiz_arr[1].strftime('%Y-%m-%d')   # str
      quiz_slack_team_id = company_latest_quiz_arr[2]                            # str
      quiz_slack_channel_id = company_latest_quiz_arr[3]                         # str
      quiz_start_date = company_latest_quiz_arr[4].strftime('%Y-%m-%d')          # str
      quiz_start_day_of_week = company_latest_quiz_arr[5]                        # str
      quiz_start_time = company_latest_quiz_arr[6]                               # str
      quiz_end_date = company_latest_quiz_arr[7].strftime('%Y-%m-%d')            # str
      quiz_end_day_of_week = company_latest_quiz_arr[8]                          # str
      quiz_end_time = company_latest_quiz_arr[9]                                 # str
      quiz_number_of_questions = company_latest_quiz_arr[10]                     # int
      quiz_question_ids_str = company_latest_quiz_arr[11]                        # str
      quiz_company_quiz_count = company_latest_quiz_arr[12]                      # int
      # Quiz Question ID's have to be converted from 1 string to an arr
      quiz_question_ids_arr = convert_question_ids_from_string_to_arr_function(quiz_question_ids_str)   # list
      # ------------------------ Assign Variables for Company Quiz END ------------------------


      # ------------------------ Check Date Time Comparison START ------------------------
      check_if_quiz_is_open_datetime = check_if_today_is_greater_than_equal_to_latest_quiz_start_date_function(quiz_start_day_of_week, quiz_start_time)
      # ------------------------ Check Date Time Comparison END ------------------------


      # ------------------------ Pull Company User Info START ------------------------
      if check_if_quiz_is_open_datetime == True:
        company_users_arr = select_triviafy_user_login_information_table_slack_all_company_user_uuids_for_quiz_email_function(postgres_connection, postgres_cursor, quiz_slack_team_id, quiz_slack_channel_id)
        # ------------------------ Loop Through Each Company User START ------------------------
        for company_user in company_users_arr:
          company_user_uuid = company_user[0]
          company_user_email = company_user[1]
          company_user_full_name = company_user[2]
          company_user_is_payment_admin = company_user[3]
          company_user_slack_token_type = company_user[4]
          company_user_slack_access_token = company_user[5]
          user_slack_authed_id = company_user[6]
          
          email_sent_search_category = 'Quiz Open'
          check_if_email_already_sent_to_company_user = select_triviafy_emails_sent_table_search_user_uuid_category_function(postgres_connection, postgres_cursor, company_user_uuid, email_sent_search_category, uuid_quiz)

          if check_if_email_already_sent_to_company_user == None:
            # ------------------------ Send Account Created Email START ------------------------
            output_email = company_user_email
            output_subject_line = 'Triviafy ' + email_sent_search_category + ' - ' + quiz_start_date
            output_message_content = f"Hi {company_user_full_name},\n\nYour team's weekly Triviafy quiz is now open!\n\nLogin and submit your answers at: https://triviafy.com/ \n\nBest,\nRob\n\nTriviafy your workspace."
            output_message_content_str_for_db = output_message_content

            email_sent_successfully = send_email_template_function(output_email, output_subject_line, output_message_content)

            # Insert this sent email into DB
            uuid_email_sent = create_uuid_function('email_sent_')
            email_sent_timestamp = create_timestamp_function()
            output_message = insert_triviafy_emails_sent_table_function(postgres_connection, postgres_cursor, uuid_email_sent, email_sent_timestamp, company_user_uuid, email_sent_search_category, uuid_quiz, output_message_content_str_for_db)
            # ------------------------ Send Account Created Email END ------------------------
        # ------------------------ Loop Through Each Company User END ------------------------
        

        # ------------------------ Send Account Slack Message START ------------------------
        slack_message_sent_search_category = 'Quiz Open'
        check_if_slack_message_already_sent_to_company_user = select_triviafy_slack_messages_sent_table_search_user_uuid_category_function(postgres_connection, postgres_cursor, company_user_uuid, slack_message_sent_search_category, uuid_quiz)

        if check_if_slack_message_already_sent_to_company_user == None:
          # ------------------------ Select Channel Name START ------------------------
          quiz_channel_name_arr = select_triviafy_user_login_information_table_channel_name_function(postgres_connection, postgres_cursor, quiz_slack_team_id, quiz_slack_channel_id)
          quiz_channel_name = quiz_channel_name_arr[0]
          # ------------------------ Select Channel Name END ------------------------

          user_slack_authed_incoming_webhook_url = select_one_user_incoming_webhook_function(postgres_connection, postgres_cursor, quiz_slack_team_id, quiz_slack_channel_id)
          output_message_content_str_for_db = send_team_channel_message_quiz_open_function(quiz_end_day_of_week, quiz_end_time, user_slack_authed_incoming_webhook_url, quiz_channel_name)

          # Insert this sent email into DB
          uuid_slack_message_sent = create_uuid_function('slack_sent_')
          slack_message_sent_timestamp = create_timestamp_function()
          output_message = insert_triviafy_slack_messages_sent_table_function(postgres_connection, postgres_cursor, uuid_slack_message_sent, slack_message_sent_timestamp, company_user_uuid, slack_message_sent_search_category, uuid_quiz, output_message_content_str_for_db)
        # ------------------------ Send Account Slack Message START ------------------------


      # ------------------------ Pull Company User Info END ------------------------
  # ------------------------ Loop Through Each Company Latest Weekly Quiz END ------------------------



  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)

  localhost_print_function('=========================================== job_daily_quiz_open_send_email_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  job_daily_quiz_open_send_email_function()
# -------------------------------------------------------------- Imports
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_team_name_and_channel_name import select_team_name_and_channel_name_function
from backend.db.queries.select_queries.select_queries_triviafy_skipped_quiz_count_slack_team_channel_table.select_if_skipped_quiz_count_already_exists import select_if_skipped_quiz_count_already_exists_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_company_user_uuids_for_quiz_email import select_triviafy_user_login_information_table_slack_all_company_user_uuids_for_quiz_email_function
from backend.db.queries.select_queries.select_queries_triviafy_emails_sent_table.select_email_exists_skipped_quiz_request_feedback import select_email_exists_skipped_quiz_request_feedback_function
from backend.utils.send_emails.send_email_template import send_email_template_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.db.queries.insert_queries.insert_queries_triviafy_emails_sent_table.insert_triviafy_emails_sent_table import insert_triviafy_emails_sent_table_function
from datetime import date
import os, time
from backend.db.queries.select_queries.select_queries_triviafy_slack_messages_sent_table.select_triviafy_slack_messages_sent_table_search_user_uuid_category_without_quiz import select_triviafy_slack_messages_sent_table_search_user_uuid_category_without_quiz_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_channel_name import select_triviafy_user_login_information_table_channel_name_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_one_user_incoming_webhook import select_one_user_incoming_webhook_function
from backend.db.queries.insert_queries.insert_queries_triviafy_slack_messages_sent_table.insert_triviafy_slack_messages_sent_table import insert_triviafy_slack_messages_sent_table_function
from backend.utils.slack.send_team_channel_message_utils.send_team_channel_message_skipped_quiz_feedback import send_team_channel_message_skipped_quiz_feedback_function

# -------------------------------------------------------------- Main Function
def job_email_skipped_feedback_request_function(arr_to_remove):
  localhost_print_function('=========================================== job_email_skipped_feedback_request_function START ===========================================')


  # ------------------------ Set Timezone START ------------------------
  # Set the timezone of the application when user creates account is will be in US/Easterm time
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  # ------------------------ Set Timezone END ------------------------


  # ------------------------ Get Today's Date START ------------------------
  # Today's date
  today_date = date.today()
  # ------------------------ Get Today's Date END ------------------------

  # ------------------------ DB Conection START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ DB Conection End ------------------------

  for arr in arr_to_remove:
    localhost_print_function('- - - - - - - - - - - - - - - Team Channel Start - - - - - - - - - - - - - - - - - - ')
    team_id = arr[0]
    channel_id = arr[1]


    # ------------------------ State Team Channel Names START ------------------------
    try:
      team_channel_name_arr = select_team_name_and_channel_name_function(postgres_connection, postgres_cursor, team_id, channel_id)
      team_name = team_channel_name_arr[0]
      channel_name = team_channel_name_arr[1]
      localhost_print_function('Team name: {}\nChannel name: {}'.format(team_name, channel_name))
    except:
      localhost_print_function('Team name: not found on login\nChannel name: not found on login')
      localhost_print_function('- - - - - - - - - - - - - - - Team Channel End - - - - - - - - - - - - - - - - - - ')
      continue
    # ------------------------ State Team Channel Names END ------------------------


    # ------------------------ Get Total Skipped Quizzes START ------------------------
    try:
      skipped_quiz_count_arr = select_if_skipped_quiz_count_already_exists_function(postgres_connection, postgres_cursor, team_id, channel_id)
      skipped_quiz_count_int = skipped_quiz_count_arr[0]
    except:
      # If not quizzes have been skipped yet for team channel combo
      skipped_quiz_count_int = 0
    # ------------------------ Get Total Skipped Quizzes END ------------------------


    # ------------------------ Email Each Team Member START ------------------------
    company_users_arr = select_triviafy_user_login_information_table_slack_all_company_user_uuids_for_quiz_email_function(postgres_connection, postgres_cursor, team_id, channel_id)
    for company_user in company_users_arr:
      company_user_uuid = company_user[0]
      company_user_email = company_user[1]
      company_user_full_name = company_user[2]
      company_user_is_payment_admin = company_user[3]
      company_user_slack_token_type = company_user[4]
      company_user_slack_access_token = company_user[5]
      user_slack_authed_id = company_user[6]
      
      email_sent_search_category = 'Skipped Quiz Feedback Request'
      check_if_email_already_sent_to_company_user = select_email_exists_skipped_quiz_request_feedback_function(postgres_connection, postgres_cursor, company_user_uuid, email_sent_search_category)

      if check_if_email_already_sent_to_company_user != None:
        localhost_print_function('Already sent an email to {}'.format(company_user_email))
        uuid_quiz = None
        pass
      if check_if_email_already_sent_to_company_user == None:
        # ------------------------ Send Email START ------------------------
        output_email = company_user_email
        output_subject_line = 'Triviafy ' + email_sent_search_category + ' - ' + str(today_date)
        output_message_content = f"Hi {company_user_full_name},\n\nCancel Free Trial Period: If you want to stop receiving emails/Slack messages from Triviafy (end your team's free trial period early), then please reply on this email with word 'cancel.'\n\nYour team's Slack channel '{channel_name}' has skipped {skipped_quiz_count_int} Triviafy quizzes.\nWhy is no one on your team participating?\nAny feedback about our product would be greatly appreciated.\n\nCancel Free Trial Period: If you want to stop receiving emails/Slack messages from Triviafy (end your team's free trial period early), then please reply on this email with word 'cancel.'\n\nBest,\nRobert Borowski | Founder\n\nTriviafy your workspace."
        output_message_content_str_for_db = output_message_content

        email_sent_successfully = send_email_template_function(output_email, output_subject_line, output_message_content)

        # Insert this sent email into DB
        uuid_email_sent = create_uuid_function('email_sent_')
        email_sent_timestamp = create_timestamp_function()
        uuid_quiz = None
        output_message = insert_triviafy_emails_sent_table_function(postgres_connection, postgres_cursor, uuid_email_sent, email_sent_timestamp, company_user_uuid, email_sent_search_category, uuid_quiz, output_message_content_str_for_db)
        # ------------------------ Send Email END ------------------------
    # ------------------------ Email Each Team Member END ------------------------


    # ------------------------ Send Account Slack Message START ------------------------
    slack_message_sent_search_category = email_sent_search_category
    check_if_slack_message_already_sent_to_company_user = select_triviafy_slack_messages_sent_table_search_user_uuid_category_without_quiz_function(postgres_connection, postgres_cursor, company_user_uuid, slack_message_sent_search_category)

    if check_if_slack_message_already_sent_to_company_user == None:
      # ------------------------ Select Channel Name START ------------------------
      quiz_channel_name_arr = select_triviafy_user_login_information_table_channel_name_function(postgres_connection, postgres_cursor, team_id, channel_id)
      quiz_channel_name = quiz_channel_name_arr[0]
      # ------------------------ Select Channel Name END ------------------------


      user_slack_authed_incoming_webhook_url = select_one_user_incoming_webhook_function(postgres_connection, postgres_cursor, team_id, channel_id)
      output_message_content_str_for_db = send_team_channel_message_skipped_quiz_feedback_function(quiz_channel_name, skipped_quiz_count_int, user_slack_authed_incoming_webhook_url)

      # Insert this sent email into DB
      uuid_slack_message_sent = create_uuid_function('slack_sent_')
      slack_message_sent_timestamp = create_timestamp_function()
      output_message = insert_triviafy_slack_messages_sent_table_function(postgres_connection, postgres_cursor, uuid_slack_message_sent, slack_message_sent_timestamp, company_user_uuid, slack_message_sent_search_category, uuid_quiz, output_message_content_str_for_db)
      localhost_print_function('Slack message sent Successfully to:\nTeam name: {}\nChannel name: {}'.format(team_name, channel_name))
    
    else:
      localhost_print_function('Slack message already sent to:\nTeam name: {}\nChannel name: {}'.format(team_name, channel_name))
      pass
    # ------------------------ Send Account Slack Message START ------------------------

    
    localhost_print_function('- - - - - - - - - - - - - - - Team Channel End - - - - - - - - - - - - - - - - - - ')


  # ------------------------ DB Close Conection START ------------------------
  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ DB Close Conection END ------------------------

  localhost_print_function('=========================================== job_email_skipped_feedback_request_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  arr_to_remove = [
    # [SlackTeamID, SlackChannelID]
    # ['abc','xyz']
    ['abc','xyz']
  ]

  job_email_skipped_feedback_request_function(arr_to_remove)
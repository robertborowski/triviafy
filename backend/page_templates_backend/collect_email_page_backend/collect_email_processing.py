# -------------------------------------------------------------- Imports
from flask import Blueprint, redirect, request
import os
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.sanitize_user_inputs.sanitize_collect_email import sanitize_collect_email_function
from backend.utils.sanitize_user_inputs.sanitize_collect_name import sanitize_collect_name_function
from backend.utils.sanitize_user_inputs.sanitize_collect_job_title import sanitize_collect_job_title_function
from backend.db.queries.select_queries.select_queries_triviafy_landing_page_emails_collection_table.select_if_email_collected_exists import select_if_email_collected_exists_function
from backend.db.queries.insert_queries.insert_queries_triviafy_landing_page_emails_collection_table.insert_user_collected_email import insert_user_collected_email_function
from backend.utils.send_emails.send_email_template import send_email_template_function
from backend.db.queries.insert_queries.insert_queries_triviafy_emails_sent_table.insert_triviafy_emails_sent_table import insert_triviafy_emails_sent_table_function

# -------------------------------------------------------------- App Setup
collect_email_processing = Blueprint("collect_email_processing", __name__, static_folder="static", template_folder="templates")
@collect_email_processing.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@collect_email_processing.route("/collect/email/processing", methods=['GET','POST'])
def collect_email_processing_function():
  localhost_print_function('=========================================== /collect/email/processing Page START ===========================================')


  # ------------------------ Sanitize user inputs START ------------------------
  try:
    # Get/sanitize user inputs from form
    user_form_input_email = sanitize_collect_email_function(request.form.get('user_input_email'))

    # Try to get/sannitize user inputs from form demo page
    try:
      user_form_input_first_name = sanitize_collect_name_function(request.form.get('demo_user_input_first_name'))
      user_form_input_last_name = sanitize_collect_name_function(request.form.get('demo_user_input_last_name'))
      user_form_input_job_title = sanitize_collect_job_title_function(request.form.get('demo_user_input_job_title'))

      if user_form_input_first_name == None:
        user_form_input_first_name = 'zblankblank'
      if user_form_input_last_name == None:
        user_form_input_last_name = 'zblankblank'
      if user_form_input_job_title == None:
        user_form_input_job_title = 'zblankblank'

    except:
      user_form_input_first_name = 'zblankblank'
      user_form_input_last_name = 'zblankblank'
      user_form_input_job_title = 'zblankblank'

  except:
    localhost_print_function('invalid url')
    localhost_print_function('=========================================== /collect/email/processing Page END ===========================================')
    return redirect('/', code=302)
  # ------------------------ Sanitize user inputs END ------------------------


  # ------------------------ Check sanitized results START ------------------------
  # Check if sanitized inputs are valid and if code can move on
  if user_form_input_email == None:
    localhost_print_function('invalid inputs')
    localhost_print_function('=========================================== /collect/email/processing Page END ===========================================')
    return redirect('/', code=302)
  # ------------------------ Check sanitized results END ------------------------


  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()


  # ------------------------ Check If Email Already in DB START ------------------------
  email_collected_exists = select_if_email_collected_exists_function(postgres_connection, postgres_cursor, user_form_input_email)
  if email_collected_exists != None:
    localhost_print_function('email already exists in DB')
    localhost_print_function('=========================================== /collect/email/processing Page END ===========================================')
    return redirect('/employees/collect/email/confirm', code=302)
  # ------------------------ Check If Email Already in DB END ------------------------


  # ------------------------ Declare database variables START ------------------------
  # Additional variables for database
  collect_email_uuid = create_uuid_function('collect_email_')
  collect_email_timestamp = create_timestamp_function()
  # ------------------------ Declare database variables END ------------------------


  # ------------------------ Insert into DB START ------------------------
  output_message = insert_user_collected_email_function(postgres_connection, postgres_cursor, collect_email_uuid, collect_email_timestamp, user_form_input_email, user_form_input_first_name, user_form_input_last_name, user_form_input_job_title)
  # ------------------------ Insert into DB END ------------------------

  """
  # ------------------------ Email Self About New Account START ------------------------
  personal_email = os.environ.get('PERSONAL_EMAIL')
  if user_form_input_email != personal_email:
    output_email = personal_email
    output_subject_line = 'Someone Added Email - Triviafy Landing Page'
    output_message_content = f"Hi,\n\n{user_form_input_email} Added their email on the Triviafy landing page."
    output_message_content_str_for_db = output_message_content

    email_sent_successfully = send_email_template_function(output_email, output_subject_line, output_message_content)

    # Insert this sent email into DB
    uuid_email_sent = create_uuid_function('email_sent_')
    email_sent_timestamp = create_timestamp_function()
    # - - -
    email_sent_search_category = 'Notify Me Someone Created Account'
    uuid_quiz = None
    # - - -
    user_uuid = 'sent_to_personal_email'
    output_message = insert_triviafy_emails_sent_table_function(postgres_connection, postgres_cursor, uuid_email_sent, email_sent_timestamp, user_uuid, email_sent_search_category, uuid_quiz, output_message_content_str_for_db)
  # ------------------------ Email Self About New Account END ------------------------
  """

  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Upload Question to database END ------------------------

  
  localhost_print_function('=========================================== /collect/email/processing Page END ===========================================')
  return redirect('/employees/collect/email/confirm', code=302)
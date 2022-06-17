# -------------------------------------------------------------- Imports
from flask import Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.create_question_page_utils.user_upload_image_checks_aws_s3 import user_upload_image_checks_aws_s3_function
from backend.utils.sanitize_user_inputs.sanitize_create_question_categories import sanitize_create_question_categories_function
from backend.utils.sanitize_user_inputs.sanitize_create_question_title import sanitize_create_question_title_function
from backend.utils.sanitize_user_inputs.sanitize_create_question_actual_question import sanitize_create_question_actual_question_function
from backend.utils.sanitize_user_inputs.sanitize_create_question_accepted_answers import sanitize_create_question_accepted_answers_function
from backend.utils.sanitize_user_inputs.sanitize_create_question_difficulty import sanitize_create_question_difficulty_function
from backend.utils.sanitize_user_inputs.sanitize_create_question_hint import sanitize_create_question_hint_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.utils.create_question_page_utils.change_uploaded_image_filename import change_uploaded_image_filename_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.insert_queries.insert_queries_triviafy_all_questions_table.insert_triviafy_all_questions_table import insert_triviafy_all_questions_table_function
import os
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
create_question_submission_processing = Blueprint("create_question_submission_processing", __name__, static_folder="static", template_folder="templates")
@create_question_submission_processing.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@create_question_submission_processing.route("/create/question/user/form/submit/processing", methods=['GET','POST'])
def create_question_submission_processing_function():
  localhost_print_function('=========================================== /create/question/user/form/submit/processing Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/create/question/user/form/submit/processing')
    # Redirects based on returned value - pre load checks
    if user_nested_dict == '/subscription':
      return redirect('/subscription', code=302)
    elif user_nested_dict == '/notifications/email/permission':
      return redirect('/notifications/email/permission', code=302)
    elif user_nested_dict == '/new/user/questionnaire':
      return redirect('/new/user/questionnaire', code=302)
    elif user_nested_dict == '/categories/edit':
      return redirect('/categories/edit', code=302)
    elif user_nested_dict == '/logout':
      return redirect('/logout', code=302)
    # ------------------------ Pre Load Page Checks END ------------------------


    # ------------------------ Page Company Info START ------------------------
    user_company_name = user_nested_dict['user_company_name']
    user_company_name = sanitize_page_output_company_name_function(user_company_name)
    user_channel_name = user_nested_dict['user_slack_channel_name']
    # ------------------------ Page Company Info END ------------------------
    
    # Get additional variables
    user_email = user_nested_dict['user_email']
    question_author_team_id = user_nested_dict['user_slack_workspace_team_id']
    question_author_channel_id = user_nested_dict['user_slack_channel_id']
    question_author_uuid = user_nested_dict['user_uuid']

  except:
    localhost_print_function('page load except error hit - /create/question/user/form/submit/processing Page')
    localhost_print_function('=========================================== /create/question/user/form/submit/processing Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)

  """
  # ------------------------ Check create question accesss START ------------------------
  # Get personal email
  personal_email = os.environ.get('PERSONAL_EMAIL')

  # If user does not have access to create questions then redirect to waitlist page
  if user_email != personal_email:
    localhost_print_function('redirecting to the create question wait list page!')
    localhost_print_function('=========================================== /create/question/user/form/submit/processing Page END ===========================================')
    return redirect('/create/question/user/waitlist', code=302)
  # ------------------------ Check create question accesss END ------------------------
  """
  
  # ------------------------ Sanitize user inputs START ------------------------
  # Get/sanitize user inputs from form
  user_create_question_categories = sanitize_create_question_categories_function(request.form.get('input_question_categories_arr_html'))
  user_create_question_title = sanitize_create_question_title_function(request.form.get('input_question_title_str_html'))
  user_create_question_actual_question = sanitize_create_question_actual_question_function(request.form.get('input_actual_question_str_html'))
  user_create_question_accepted_answers = sanitize_create_question_accepted_answers_function(request.form.get('input_question_answers_arr_html'))
  user_create_question_difficulty = sanitize_create_question_difficulty_function(request.form.get('question-difficulty-level'))
  user_create_question_hint = sanitize_create_question_hint_function(request.form.get('input_hint_str_html'))
  create_question_upload_image_original_filename = 'no image uploaded by user'
  # ------------------------ Sanitize user inputs END ------------------------


  # ------------------------ Check sanitized results START ------------------------
  # Check if sanitized inputs are valid and if code can move on
  if user_create_question_categories == None or user_create_question_title == None or user_create_question_actual_question == None or user_create_question_accepted_answers == None or user_create_question_difficulty == None or user_create_question_hint == None:
    localhost_print_function('invalid inputs')
    localhost_print_function('=========================================== /create/question/user/form/submit/processing Page END ===========================================')
    return redirect('/create/question/user/form', code=302)
  # ------------------------ Check sanitized results END ------------------------
  

  # ------------------------ Declare database variables START ------------------------
  # Additional variables for database
  create_question_uuid = create_uuid_function('questionid_')
  create_question_timestamp = create_timestamp_function()
  user_create_question_is_deprecated = False
  user_create_question_is_approved_for_release = False
  question_submission_status = "In Review"
  user_create_question_hint_allowed = False
  if len(user_create_question_hint) >= 1 and user_create_question_hint != 'no hint':
    user_create_question_hint_allowed = True
  user_create_question_contains_image = False
  create_question_uploaded_image_uuid = 'no image uuid'
  create_question_uploaded_image_aws_url = 'no aws image url'
  # ------------------------ Declare database variables END ------------------------
  
  
  # ------------------------ Image Upload START ------------------------
  # Check the user input image upload, if correct format and size then store in aws s3
  try:
    if request.method == "POST":
      if request.files:
        if "filesize" in request.cookies:
          # Get the variables from request
          image = request.files["input_image_upload"]
          if image.filename != '' and image.filename != ' ' and image.filename != None:
            # Keep track of the original filename that someone is uploading
            create_question_upload_image_original_filename = image.filename

            # Create image uuid to store in aws
            create_question_uploaded_image_uuid = '_user_uploaded_image_' + create_question_uuid
            
            # Change the name of the image from whatever the user uploaded to the question uuid as name
            image = change_uploaded_image_filename_function(image, create_question_uploaded_image_uuid)
            
            # Get image filesize
            file_size = request.cookies["filesize"]

            # Check and upload the user file image
            user_image_upload_status = user_upload_image_checks_aws_s3_function(image, file_size)
            
            if image.filename != 'no image uuid':
              # Finalize image variables
              user_create_question_contains_image = True
              create_question_uploaded_image_aws_url = 'https://' + os.environ.get('AWS_TRIVIAFY_BUCKET_NAME') + '.s3.' + os.environ.get('AWS_TRIVIAFY_REGION') + '.amazonaws.com/' + image.filename
  except:
    localhost_print_function('user image upload did not work!')
    pass
  # ------------------------ Image Upload END ------------------------


  # ------------------------ Upload Question to database START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  
  # Attempt to upload to database
  try:
    insert_db_output_message = insert_triviafy_all_questions_table_function(postgres_connection, postgres_cursor, create_question_uuid, create_question_timestamp, user_create_question_categories, user_create_question_actual_question, user_create_question_accepted_answers, user_create_question_difficulty, user_create_question_hint_allowed, user_create_question_hint, user_create_question_is_deprecated, user_create_question_title, user_create_question_is_approved_for_release, user_create_question_contains_image, create_question_uploaded_image_uuid, create_question_uploaded_image_aws_url, create_question_upload_image_original_filename,question_submission_status, question_author_team_id, question_author_channel_id, question_author_uuid)
  except:
    localhost_print_function('failed to insert question into database')
    pass

  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Upload Question to database END ------------------------

  
  localhost_print_function('=========================================== /create/question/user/form/submit/processing Page END ===========================================')
  # Changing this temporary because it needs to break down into pages instead of one big page that pulls x thousands of images immediately.
  return redirect('/create/question/user/form/submit/success/1', code=302)
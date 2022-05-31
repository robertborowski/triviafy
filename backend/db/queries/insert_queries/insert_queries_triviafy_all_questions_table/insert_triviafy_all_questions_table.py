# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def insert_triviafy_all_questions_table_function(postgres_connection, postgres_cursor, create_question_uuid, create_question_timestamp, user_create_question_categories, user_create_question_actual_question, user_create_question_accepted_answers, user_create_question_difficulty, user_create_question_hint_allowed, user_create_question_hint, user_create_question_is_deprecated, user_create_question_title, user_create_question_is_approved_for_release, user_create_question_contains_image, create_question_uploaded_image_uuid, create_question_uploaded_image_aws_url, create_question_upload_image_original_filename,question_submission_status, question_author_team_id, question_author_channel_id, question_author_uuid):
  localhost_print_function('=========================================== insert_triviafy_all_questions_table_function START ===========================================')
  
  # ------------------------ Query START ------------------------
  postgres_insert_query = """INSERT INTO triviafy_all_questions_table(question_uuid,question_timestamp_created,question_categories_list,question_actual_question,question_answers_list,question_difficulty,question_hint_allowed,question_hint,question_deprecated,question_title,question_approved_for_release,question_contains_image,question_image_aws_uuid, question_image_aws_url,question_image_upload_original_filename,question_status_for_creator,question_author_team_id,question_author_channel_id,question_author_uuid) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
  # ------------------------ Query END ------------------------


  # ------------------------ Record row START ------------------------
  record_to_insert = (create_question_uuid, create_question_timestamp, user_create_question_categories, user_create_question_actual_question, user_create_question_accepted_answers, user_create_question_difficulty, user_create_question_hint_allowed, user_create_question_hint, user_create_question_is_deprecated, user_create_question_title, user_create_question_is_approved_for_release, user_create_question_contains_image, create_question_uploaded_image_uuid, create_question_uploaded_image_aws_url, create_question_upload_image_original_filename,question_submission_status, question_author_team_id, question_author_channel_id, question_author_uuid)
  # ------------------------ Record row END ------------------------


  # ------------------------ Insert attempt START ------------------------
  try:
    postgres_cursor.execute(postgres_insert_query, record_to_insert)
    postgres_connection.commit()
    localhost_print_function('=========================================== insert_triviafy_all_questions_table_function END ===========================================')
    return True
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== insert_triviafy_all_questions_table_function END ===========================================')
      return False
  # ------------------------ Insert attempt END ------------------------
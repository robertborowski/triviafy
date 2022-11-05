# -------------------------------------------------------------- Imports
import os
import datetime
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_all_tables.select_question_migration import select_question_migration_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.insert_queries.insert_queries_triviafy_emails_sent_table.insert_migration_questions import insert_migration_questions_function

# -------------------------------------------------------------- Main Function
def job_migrate_mcq_questions_function():
  localhost_print_function('=========================================== job_migrate_mcq_questions_function START ===========================================')
  # ------------------------ DB Conection START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ DB Conection End ------------------------

  # ------------------------ SQL Get DB Table Names START ------------------------
  # Get all table names in the current database
  db_migration_arr = select_question_migration_function(postgres_connection, postgres_cursor)
  # ------------------------ SQL Get DB Table Names END ------------------------

  # ------------------------ build export csv start ------------------------
  current_counter = 0
  for i_question_arr in db_migration_arr:
    current_counter += 1
    if current_counter == 1:
      break
    # ------------------------ initial table start ------------------------
    i_question_uuid = i_question_arr[0]
    i_question_timestamp_created = i_question_arr[1]
    i_question_categories_list = i_question_arr[2]
    i_question_actual_question = i_question_arr[3]
    i_question_answers_list = i_question_arr[4]
    i_question_difficulty = i_question_arr[5]
    i_question_hint_allowed = i_question_arr[6]
    i_question_hint = i_question_arr[7]
    i_question_deprecated = i_question_arr[8]
    i_question_deprecated_timestamp = i_question_arr[9]
    i_question_title = i_question_arr[10]
    i_question_approved_for_release = i_question_arr[11]
    i_question_contains_image = i_question_arr[12]
    i_question_image_aws_uuid = i_question_arr[13]
    i_question_image_aws_url = i_question_arr[14]
    i_question_image_upload_original_filename = i_question_arr[15]
    i_question_status_for_creator = i_question_arr[16]
    i_question_author_team_id = i_question_arr[17]
    i_question_author_channel_id = i_question_arr[18]
    i_question_author_uuid = i_question_arr[19]
    # ------------------------ initial table end ------------------------
    # ------------------------ initialize variables to be parsed start ------------------------
    parsed_question = i_question_actual_question
    parsed_option_a = None
    parsed_option_b = None
    parsed_option_c = None
    parsed_option_d = None
    parsed_option_e = None
    # ------------------------ initialize variables to be parsed end ------------------------
    # ------------------------ parsing start ------------------------
    k_arr = i_question_actual_question.split(' (A: ')
    parsed_question = k_arr[0]
    contains_selection_abcde = False
    k_answer_str = None
    try:
      k_answer_str = '(A: ' + k_arr[1]
      contains_selection_abcde = True
    except:
      contains_selection_abcde = False
      print(' ')
      print(i_question_uuid)
      print(' ')
    if contains_selection_abcde == True:
      k_answer_arr = k_answer_str.split(' | ')
      for k_i_string in k_answer_arr:
        current_parsing_str = k_i_string[4:-1]
        if '(A: ' in k_i_string:
          parsed_option_a = current_parsing_str
        if '(B: ' in k_i_string:
          parsed_option_b = current_parsing_str
        if '(C: ' in k_i_string:
          parsed_option_c = current_parsing_str
        if '(D: ' in k_i_string:
          parsed_option_d = current_parsing_str
        if '(E: ' in k_i_string:
          parsed_option_e = current_parsing_str
    # ------------------------ parsing end ------------------------
    # ------------------------ Final row assignment start ------------------------
    final_id = i_question_uuid
    final_created_timestamp = i_question_timestamp_created
    final_fk_user_id = None
    final_status = True
    final_categories = i_question_categories_list
    final_title = i_question_title
    final_difficulty = i_question_difficulty
    final_question = parsed_question
    final_option_a = parsed_option_a
    final_option_b = parsed_option_b
    final_option_c = parsed_option_c
    final_option_d = parsed_option_d
    final_option_e = parsed_option_e
    final_answer = i_question_answers_list
    final_aws_image_uuid = i_question_image_aws_uuid
    final_aws_image_url = i_question_image_aws_url
    # ------------------------ Final row assignment end ------------------------
    insert_migration_questions_function(postgres_connection, postgres_cursor, final_id,final_created_timestamp,final_fk_user_id,final_status,final_categories,final_title,final_difficulty,final_question,final_option_a,final_option_b,final_option_c,final_option_d,final_option_e,final_answer,final_aws_image_uuid,final_aws_image_url)
    # ------------------------ insert row to csv start ------------------------
    # ------------------------ insert row to csv end ------------------------
  # ------------------------ build export csv end ------------------------




  # ------------------------ DB Close Conection START ------------------------
  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ DB Close Conection END ------------------------

  localhost_print_function('=========================================== job_migrate_mcq_questions_function END ===========================================')
  return True



# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  job_migrate_mcq_questions_function()
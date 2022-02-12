# -------------------------------------------------------------- Imports
from datetime import date, timedelta
import os, time
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_team_channel_combos import select_triviafy_user_login_information_table_slack_all_team_channel_combos_function
from backend.db.queries.select_queries.select_queries_joined_tables.select_skipped_quizzes_company_team_level import select_skipped_quizzes_company_team_level_function
from backend.utils.latest_quiz_utils.supporting_make_company_latest_quiz_utils.convert_question_ids_from_string_to_arr import convert_question_ids_from_string_to_arr_function
from backend.db.queries.select_queries.select_queries_triviafy_skipped_quiz_count_slack_team_channel_table.select_if_skipped_quiz_count_already_exists import select_if_skipped_quiz_count_already_exists_function
from backend.db.queries.insert_queries.insert_queries_triviafy_skipped_quiz_count_slack_team_channel_table.insert_triviafy_skipped_quiz_count_slack_team_channel_table import insert_triviafy_skipped_quiz_count_slack_team_channel_table_function
from backend.db.queries.update_queries.update_queries_triviafy_skipped_quiz_count_slack_team_channel_table.update_skipped_quiz_count import update_skipped_quiz_count_function
from backend.db.queries.delete_queries.delete_queries_triviafy_quiz_master_table.delete_query_delete_skipped_quiz import delete_query_delete_skipped_quiz_function
from backend.db.queries.delete_queries.delete_queries_triviafy_quiz_questions_asked_to_company_slack_table.delete_query_delete_question_asked_on_skipped_quiz import delete_query_delete_question_asked_on_skipped_quiz_function

# -------------------------------------------------------------- Main Function
def job_post_quiz_skipped_quiz_check_function():
  localhost_print_function('=========================================== job_post_quiz_skipped_quiz_check_function START ===========================================')

  # ------------------------ Print Summary Variables START ------------------------
  summary_arr = []
  # ------------------------ Print Summary Variables END ------------------------
  
  
  # ------------------------ Get Today's Date Information START ------------------------
  # Today's date
  today_date = date.today()# - timedelta(days=1)
  today_date_str = str(today_date)
  # ------------------------ Get Today's Date Information END ------------------------


  # ------------------------ Connect to DB START ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ Connect to DB END ------------------------


  # ------------------------ Pull All Company Team Channel Combos START ------------------------
  all_current_slack_team_id_and_channel_id_combos_arr = select_triviafy_user_login_information_table_slack_all_team_channel_combos_function(postgres_connection, postgres_cursor)
  count_all_current_slack_team_id_and_channel_id_combos_arr = len(all_current_slack_team_id_and_channel_id_combos_arr)
  # ------------------------ Pull All Company Team Channel Combos END ------------------------


  # ------------------------ For Each Company Team Channel Combo START ------------------------
  count_so_far = 0
  for team_channel_combo in all_current_slack_team_id_and_channel_id_combos_arr:
    count_so_far += 1

    company_team_id = team_channel_combo[0]
    company_channel_id = team_channel_combo[1]
    # ------------------------ Pull Closed Quizzes with No Winner START ------------------------
    # Get the quiz info arr of skipped quizzes
    skipped_quizzes_arr = select_skipped_quizzes_company_team_level_function(postgres_connection, postgres_cursor, company_team_id, company_channel_id, today_date_str)

    if skipped_quizzes_arr == None:
      if count_so_far < count_all_current_slack_team_id_and_channel_id_combos_arr:
        localhost_print_function('move onto next team')
        continue
      else:
        localhost_print_function('Last team channel combo')
        localhost_print_function('did not run delete, likely because it is day of quiz end')
        # ------------------------ Job Summary Print START ------------------------
        len_summary_arr = len(summary_arr)
        localhost_print_function('- - - - - - -')
        localhost_print_function('- - - - - - -')
        localhost_print_function('deleted quiz count: {}'.format(len_summary_arr))
        localhost_print_function('- - - - - - -')
        localhost_print_function('- - - - - - -')
        # ------------------------ Job Summary Print END ------------------------
        localhost_print_function('=========================================== job_post_quiz_skipped_quiz_check_function END ===========================================')
        return True

    # Total number of skipped quizzes for company
    total_skipped_quizzes_int_for_company_team_channel_level = len(skipped_quizzes_arr)

    for skipped_quiz in skipped_quizzes_arr:
      uuid_quiz = skipped_quiz[0]                   # str
      # quiz_timestamp_created = skipped_quiz[1]    # datetime.datetime
      # quiz_slack_team_id = skipped_quiz[2]        # str
      # quiz_slack_channel_id = skipped_quiz[3]     # str
      # quiz_start_date = skipped_quiz[4]           # datetime.datetime
      # quiz_start_day_of_week = skipped_quiz[5]    # str
      # quiz_start_time = skipped_quiz[6]           # str
      # quiz_end_date = skipped_quiz[7]             # datetime.datetime
      # quiz_end_day_of_week = skipped_quiz[8]      # str
      # quiz_end_time = skipped_quiz[9]             # str
      # quiz_number_of_questions = skipped_quiz[10] # int
      # quiz_question_ids_str = skipped_quiz[11]    # * str
      # company_quiz_count = skipped_quiz[12]       # int
      # quiz_question_ids_arr = convert_question_ids_from_string_to_arr_function(quiz_question_ids_str)   # * list
      # ------------------------ Pull Closed Quizzes with No Winner END ------------------------


      # ------------------------ Delete Skipped Quiz And Questions Marked As Asked START ------------------------
      # Delete the quiz from master quiz table DB
      output_message = delete_query_delete_skipped_quiz_function(postgres_connection, postgres_cursor, uuid_quiz)
      # Delete the questions asked from the master questions asked to team channel table DB
      output_message = delete_query_delete_question_asked_on_skipped_quiz_function(postgres_connection, postgres_cursor, uuid_quiz)
      # Append to job summary
      summary_arr.append((company_team_id, company_channel_id, uuid_quiz))
      # ------------------------ Delete Skipped Quiz And Questions Marked As Asked END ------------------------


    # ------------------------ Insert/Update Total Quizzes Skipped Table START ------------------------
    # Get latest skipped quiz count
    current_db_skipped_quiz_count = select_if_skipped_quiz_count_already_exists_function(postgres_connection, postgres_cursor, company_team_id, company_channel_id)

    # If there is no latest skipped quiz count for company team channel level, insert to DB and make count 0 again
    if current_db_skipped_quiz_count == False:
      skipped_quiz_uuid = create_uuid_function('skipped_quiz_')
      skipped_quiz_timestamp = create_timestamp_function()
      output_message = insert_triviafy_skipped_quiz_count_slack_team_channel_table_function(postgres_connection, postgres_cursor, skipped_quiz_uuid, skipped_quiz_timestamp, company_team_id, company_channel_id, total_skipped_quizzes_int_for_company_team_channel_level)
      total_skipped_quizzes_int_for_company_team_channel_level = 0
    
    # If there is a latest skipped quiz count, update the number in DB
    if current_db_skipped_quiz_count != False:
      current_db_skipped_quiz_count_int = current_db_skipped_quiz_count[0]
      current_db_skipped_quiz_count_int_updated = current_db_skipped_quiz_count_int + total_skipped_quizzes_int_for_company_team_channel_level
      output_message = update_skipped_quiz_count_function(postgres_connection, postgres_cursor, current_db_skipped_quiz_count_int_updated, company_team_id, company_channel_id)
    # ------------------------ Insert/Update Total Quizzes Skipped Table START ------------------------
  # ------------------------ For Each Company Team Channel Combo END ------------------------


  # ------------------------ Clsoe DB START ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Clsoe DB END ------------------------


  # ------------------------ Job Summary Print START ------------------------
  len_summary_arr = len(summary_arr)
  localhost_print_function('- - - - - - -')
  localhost_print_function('- - - - - - -')
  localhost_print_function('deleted quiz count: {}'.format(len_summary_arr))
  localhost_print_function('- - - - - - -')
  localhost_print_function('- - - - - - -')
  # ------------------------ Job Summary Print END ------------------------


  localhost_print_function('=========================================== job_post_quiz_skipped_quiz_check_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  job_post_quiz_skipped_quiz_check_function()
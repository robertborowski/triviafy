import psycopg2
from psycopg2 import Error

def insert_triviafy_quiz_answers_master_table_function(postgres_connection, postgres_cursor, uuid_quiz_answer, quiz_answer_timestamp, slack_workspace_team_id, slack_channel_id, user_uuid, uuid_quiz, question_uuid_k, user_answer_v):
  """Returns: inserts into database"""
  
  # ------------------------ Query START ------------------------
  postgres_insert_query = """INSERT INTO triviafy_quiz_answers_master_table(uuid_quiz_answer,quiz_answer_timestamp,quiz_answer_slack_team_id,quiz_answer_slack_channel_id,quiz_answer_user_uuid_fk,quiz_answer_quiz_uuid_fk,quiz_answer_quiz_question_uuid_fk,quiz_answer_actual_user_answer) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
  # ------------------------ Query END ------------------------


  # ------------------------ Record row START ------------------------
  record_to_insert = (uuid_quiz_answer, quiz_answer_timestamp, slack_workspace_team_id, slack_channel_id, user_uuid, uuid_quiz, question_uuid_k, user_answer_v)
  # ------------------------ Record row END ------------------------


  # ------------------------ Insert attempt START ------------------------
  try:
    postgres_cursor.execute(postgres_insert_query, record_to_insert)
    postgres_connection.commit()
    output_message = 'Postgres Database Insert Successful!'
    return output_message
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      print("Status: ", error)
      output_message = 'Did not insert info database'
      return output_message
  # ------------------------ Insert attempt END ------------------------
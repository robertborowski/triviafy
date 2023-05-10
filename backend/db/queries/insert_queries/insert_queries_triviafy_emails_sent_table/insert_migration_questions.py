# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def insert_migration_questions_function(postgres_connection, postgres_cursor, final_id,final_created_timestamp,final_fk_user_id,final_status,final_categories,final_title,final_difficulty,final_question,final_option_a,final_option_b,final_option_c,final_option_d,final_option_e,final_answer,final_aws_image_uuid,final_aws_image_url):
  # localhost_print_function('=========================================== insert_migration_questions_function START ===========================================')
  
  # ------------------------ Query START ------------------------
  postgres_insert_query = """INSERT INTO activity_a_created_questions_obj(id,created_timestamp,fk_user_id,status,categories,title,difficulty,question,option_a,option_b,option_c,option_d,option_e,answer,aws_image_uuid,aws_image_url) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
  # ------------------------ Query END ------------------------
  


  # ------------------------ Record row START ------------------------
  record_to_insert = (final_id,final_created_timestamp,final_fk_user_id,final_status,final_categories,final_title,final_difficulty,final_question,final_option_a,final_option_b,final_option_c,final_option_d,final_option_e,final_answer,final_aws_image_uuid,final_aws_image_url)
  # ------------------------ Record row END ------------------------


  # ------------------------ Insert attempt START ------------------------
  try:
    postgres_cursor.execute(postgres_insert_query, record_to_insert)
    postgres_connection.commit()

    # localhost_print_function('=========================================== insert_migration_questions_function END ===========================================')
    return True
  
  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function(error)
      localhost_print_function('=========================================== insert_migration_questions_function END ===========================================')
      return None
  # ------------------------ Insert attempt END ------------------------
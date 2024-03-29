# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error, extras
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def select_company_quiz_questions_function(postgres_connection, postgres_cursor, quiz_question_ids_arr, quiz_number_of_questions):
  localhost_print_function('=========================================== select_company_quiz_questions_function START ===========================================')

  try:
    # ------------------------ Dict Cursor START ------------------------
    cursor = postgres_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # ------------------------ Dict Cursor END ------------------------

    # 10 questions
    if quiz_number_of_questions == 10:
      # ------------------------ Query START ------------------------
      cursor.execute("SELECT * FROM triviafy_all_questions_table WHERE question_uuid IN (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [quiz_question_ids_arr[0], quiz_question_ids_arr[1], quiz_question_ids_arr[2], quiz_question_ids_arr[3], quiz_question_ids_arr[4], quiz_question_ids_arr[5], quiz_question_ids_arr[6], quiz_question_ids_arr[7], quiz_question_ids_arr[8], quiz_question_ids_arr[9]])
      # ------------------------ Query END ------------------------
    
    # 5 questions
    elif quiz_number_of_questions == 5:
      # ------------------------ Query START ------------------------
      cursor.execute("SELECT * FROM triviafy_all_questions_table WHERE question_uuid IN (%s,%s,%s,%s,%s)", [quiz_question_ids_arr[0], quiz_question_ids_arr[1], quiz_question_ids_arr[2], quiz_question_ids_arr[3], quiz_question_ids_arr[4]])
      # ------------------------ Query END ------------------------


    # ------------------------ Query Result START ------------------------
    # Get the results arr
    result_arr = cursor.fetchall()
    
    # Put results arr into dict
    result_arr_dicts = []
    for row in result_arr:
      result_arr_dicts.append(dict(row))
    
    # Retunr results dict
    localhost_print_function('=========================================== select_company_quiz_questions_function END ===========================================')
    return result_arr_dicts
    # ------------------------ Query Result END ------------------------


  except (Exception, psycopg2.Error) as error:
    if(postgres_connection):
      localhost_print_function('Except error hit: ', error)
      localhost_print_function('=========================================== select_company_quiz_questions_function END ===========================================')
      return None
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def update_manual_function(postgres_connection, postgres_cursor, tag_query_to_use, additional_input_arr=None):
  if additional_input_arr != None:
    # ------------------------ generic pull start ------------------------
    input_0 = None
    input_1 = None
    input_2 = None
    input_3 = None
    input_4 = None
    input_5 = None
    input_6 = None
    input_7 = None
    input_8 = None
    input_9 = None
    input_10 = None
    input_11 = None
    input_12 = None
    input_13 = None
    input_14 = None
    input_15 = None
    input_16 = None
    input_17 = None
    input_18 = None
    try:
      input_0 = additional_input_arr[0]
      input_1 = additional_input_arr[1]
      input_2 = additional_input_arr[2]
      input_3 = additional_input_arr[3]
      input_4 = additional_input_arr[4]
      input_5 = additional_input_arr[5]
      input_6 = additional_input_arr[6]
      input_7 = additional_input_arr[7]
      input_8 = additional_input_arr[8]
      input_9 = additional_input_arr[9]
      input_10 = additional_input_arr[10]
      input_11 = additional_input_arr[11]
      input_12 = additional_input_arr[12]
      input_13 = additional_input_arr[13]
      input_14 = additional_input_arr[14]
      input_15 = additional_input_arr[15]
      input_16 = additional_input_arr[16]
      input_17 = additional_input_arr[17]
      input_18 = additional_input_arr[18]
    except:
      pass
    # ------------------------ generic pull end ------------------------
    # ------------------------ insert queries start ------------------------
    queries_dict = {
      'update_email_1': {
        'query': "UPDATE user_celebrate_obj \
                  SET status=True, fk_question_id=%s \
                  WHERE fk_user_id=%s AND event=%s;",
        'inject_criteria': (input_0, input_1, input_2)
      },
      'update_celebrations_1': {
        'query': "UPDATE user_celebrate_obj \
                  SET fk_test_id=%s \
                  WHERE fk_question_id=%s;",
        'inject_criteria': (input_0, input_1)
      }
    }
    # ------------------------ insert queries end ------------------------
    postgres_cursor.execute(queries_dict[tag_query_to_use]['query'], queries_dict[tag_query_to_use]['inject_criteria'])
    postgres_connection.commit()
    return True
# ------------------------ individual function end ------------------------
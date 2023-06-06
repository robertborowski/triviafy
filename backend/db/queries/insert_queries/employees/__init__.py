# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def insert_manual_function(postgres_connection, postgres_cursor, tag_query_to_use, additional_input_arr=None):
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
    except:
      pass
    # ------------------------ generic pull end ------------------------
    # ------------------------ insert queries start ------------------------
    insert_queries_dict = {
      'insert_email_1': {
        'query': "INSERT INTO email_sent_obj(id,created_timestamp,from_user_id_fk,to_email,subject,body) VALUES(%s,%s,%s,%s,%s,%s);",
        'new_row': (input_0, input_1, input_2, input_3, input_4, input_5)
      },
      'insert_celebrate_1': {
        'query': "INSERT INTO activity_a_created_questions_obj(id,created_timestamp,fk_user_id,status,categories,title,question,option_a,option_b,option_c,option_d,option_e,answer,aws_image_uuid,aws_image_url,submission,product,fk_group_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
        'new_row': (input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, input_11, input_12, input_13, input_14, input_15, input_16, input_17)
      },
      'insert_test_1': {
        'query': "INSERT INTO activity_a_test_obj(id,created_timestamp,fk_group_id,timezone,start_day,start_time,start_timestamp,end_day,end_time,end_timestamp,cadence,total_questions,question_type,categories,question_ids,question_types_order,status,product) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
        'new_row': (input_0, input_1, input_2, input_3, input_4, input_5, input_6, input_7, input_8, input_9, input_10, input_11, input_12, input_13, input_14, input_15, input_16, input_17)
      }
      ,
      'insert_used_1': {
        'query': "INSERT INTO activity_a_group_questions_used_obj(id,created_timestamp,fk_group_id,fk_question_id,fk_test_id,product) VALUES(%s,%s,%s,%s,%s,%s);",
        'new_row': (input_0, input_1, input_2, input_3, input_4, input_5)
      }
    }
    # ------------------------ insert queries end ------------------------
    postgres_cursor.execute(insert_queries_dict[tag_query_to_use]['query'], insert_queries_dict[tag_query_to_use]['new_row'])
    postgres_connection.commit()
    return True
# ------------------------ individual function end ------------------------
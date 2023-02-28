# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
# ------------------------ imports end ------------------------

localhost_print_function(' ------------------------ insert_queries employees __init__ start ------------------------ ')
# ------------------------ individual function start ------------------------
def insert_manual_function(postgres_connection, postgres_cursor, tag_query_to_use, additional_input_arr=None):
  if additional_input_arr != None:
    localhost_print_function(' ------------------------ insert_manual_function end ------------------------ ')
    # ------------------------ generic pull start ------------------------
    try:
      input_0 = additional_input_arr[0]
      input_1 = additional_input_arr[1]
      input_2 = additional_input_arr[2]
      input_3 = additional_input_arr[3]
      input_4 = additional_input_arr[4]
      input_5 = additional_input_arr[5]
    except:
      pass
    # ------------------------ generic pull end ------------------------
    # ------------------------ insert queries start ------------------------
    insert_queries_dict = {
      'insert_email_1': {
        'query': "INSERT INTO employees_email_sent_obj(id,created_timestamp,from_user_id_fk,to_email,subject,body) VALUES(%s,%s,%s,%s,%s,%s);",
        'new_row': (input_0, input_1, input_2, input_3, input_4, input_5)
      }
    }
    # ------------------------ insert queries end ------------------------
    postgres_cursor.execute(insert_queries_dict[tag_query_to_use]['query'], insert_queries_dict[tag_query_to_use]['new_row'])
    postgres_connection.commit()
    localhost_print_function(' ------------------------ insert_manual_function end ------------------------ ')
    return True
# ------------------------ individual function end ------------------------
localhost_print_function(' ------------------------ insert_queries employees __init__ end ------------------------ ')
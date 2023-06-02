# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.employees import select_manual_function
from backend.db.queries.insert_queries.employees import insert_manual_function
from backend.db.queries.update_queries.employees import update_manual_function
from datetime import datetime, timedelta, date
import os, time
import sendgrid
from sendgrid import SendGridAPIClient
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
# ------------------------ imports end ------------------------

# ------------------------ set timezone start ------------------------
# Set the timezone of the application when user creates account is will be in US/Easterm time
os.environ['TZ'] = 'US/Eastern'
time.tzset()
# ------------------------ set timezone end ------------------------

# ------------------------ individual function start ------------------------
def run_job_function():
  # ------------------------ get todays variables start ------------------------
  today = date.today()
  current_day = today.day
  current_month = today.month
  current_year = today.year
  # ------------------------ get todays variables end ------------------------
  # ------------------------ open connection start ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ open connection end ------------------------
  # ------------------------ lookup/celebrate birthday start ------------------------
  db_arr_of_dict_if_birthday_today = select_manual_function(postgres_connection, postgres_cursor, 'select_if_birthday_today', current_month, current_day)
  # ------------------------ if no birthday today start ------------------------
  if db_arr_of_dict_if_birthday_today == None or db_arr_of_dict_if_birthday_today == [] or len(db_arr_of_dict_if_birthday_today) == 0:
    print('no birthdays today')
    # ------------------------ close connection start ------------------------
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ close connection end ------------------------
    return True
  # ------------------------ if no birthday today end ------------------------
  # ------------------------ if yes birthday today start ------------------------
  else:
    for i_birthday_dict in db_arr_of_dict_if_birthday_today:
      # ------------------------ get question obj start ------------------------
      db_arr_of_dict_question = select_manual_function(postgres_connection, postgres_cursor, 'select_question_1', i_birthday_dict['fk_question_id'])
      db_question_dict = db_arr_of_dict_question[0]
      localhost_print_function(' ------------- 0 ------------- ')
      localhost_print_function(f"db_question_dict | type: {type(db_question_dict)} | {db_question_dict}")
      localhost_print_function(' ------------- 0 ------------- ')
      # ------------------------ get question obj end ------------------------
      # ------------------------ get user obj start ------------------------
      db_arr_of_dict_user = select_manual_function(postgres_connection, postgres_cursor, 'select_user_2', db_question_dict['fk_user_id'])
      db_user_dict = db_arr_of_dict_user[0]
      localhost_print_function(' ------------- 1 ------------- ')
      localhost_print_function(f"db_user_dict | type: {type(db_user_dict)} | {db_user_dict}")
      localhost_print_function(' ------------- 1 ------------- ')
      # ------------------------ get user obj end ------------------------
      # ------------------------ get teammates obj start ------------------------
      db_arr_of_dict_teammates = select_manual_function(postgres_connection, postgres_cursor, 'select_users_1', db_user_dict['group_id'])
      db_teammates_dict = db_arr_of_dict_teammates
      localhost_print_function(' ------------- 2 ------------- ')
      localhost_print_function(f"db_teammates_dict | type: {type(db_teammates_dict)} | {db_teammates_dict}")
      localhost_print_function(' ------------- 2 ------------- ')
      localhost_print_function(' ')
      localhost_print_function(' ')
      localhost_print_function(' ')
      # ------------------------ get teammates obj end ------------------------
  # ------------------------ if yes birthday today end ------------------------
  # ------------------------ lookup/celebrate birthday end ------------------------
  # ------------------------ close connection start ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ close connection end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ run function start ------------------------
if __name__ == "__main__":
  run_job_function()
# ------------------------ run function end ------------------------
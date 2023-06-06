# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.employees import select_manual_function
from backend.db.queries.insert_queries.employees import insert_manual_function
from backend.db.queries.update_queries.employees import update_manual_function
import os, time
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
import openai
import random
# ------------------------ imports end ------------------------

# ------------------------ set timezone start ------------------------
# Set the timezone of the application when user creates account is will be in US/Easterm time
os.environ['TZ'] = 'US/Eastern'
time.tzset()
# ------------------------ set timezone end ------------------------

# ------------------------ individual function start ------------------------
def openai_chat_gpt_prompt_result_function(message):
  openai.api_key = os.environ.get('OPENAI_API_KEY')
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": message}
    ]
  )
  # Retrieve and return the assistant's reply
  reply = response['choices'][0]['message']['content']
  return reply
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def openai_chat_gpt_parse_results_to_arr_function(chatgpt_response_str):
  chatgpt_start_index = chatgpt_response_str.find("[")
  chatgpt_end_index = chatgpt_response_str.find("]")
  chatgpt_response_substring = None
  if chatgpt_start_index != -1 and chatgpt_end_index != -1:
    chatgpt_response_substring = chatgpt_response_str[chatgpt_start_index + 1 : chatgpt_end_index].strip()  # Extract the substring
    chatgpt_response_substring = chatgpt_response_substring.replace('"','')
    chatgpt_response_substring = chatgpt_response_substring.replace("'","")
  chatgpt_response_arr = None
  if chatgpt_response_substring != None:
    chatgpt_response_arr = chatgpt_response_substring.split(', ')
  return chatgpt_response_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def run_job_function():
  # ------------------------ open connection start ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ open connection end ------------------------
  # ------------------------ get total count needed start ------------------------
  db_arr_of_dict_custom_questions_needed = select_manual_function(postgres_connection, postgres_cursor, 'select_openai_questions_needed')
  if db_arr_of_dict_custom_questions_needed == None or db_arr_of_dict_custom_questions_needed == [] or len(db_arr_of_dict_custom_questions_needed) == 0:
    print('no new rows')
    # ------------------------ close connection start ------------------------
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ close connection end ------------------------
    return True
  # ------------------------ get total count needed end ------------------------
  # ------------------------ get all tables start ------------------------
  db_arr_of_dict_custom_questions_created = select_manual_function(postgres_connection, postgres_cursor, 'select_celebrations_for_openai')
  db_arr_of_dict_users_to_create_questions_for = select_manual_function(postgres_connection, postgres_cursor, 'select_celebration_users')
  # ------------------------ get all tables end ------------------------
  # ------------------------ loop through logic start ------------------------
  try:
    # ------------------------ loop through celebrate rows start ------------------------
    for i_celebrate_dict in db_arr_of_dict_users_to_create_questions_for:
      # ------------------------ get total teammate count start ------------------------
      db_arr_of_dict_total_teammates = select_manual_function(postgres_connection, postgres_cursor, 'select_total_teammates', i_celebrate_dict['fk_group_id'])
      if db_arr_of_dict_total_teammates[0]['count'] == 1:
        localhost_print_function(f"group_id: {i_celebrate_dict['fk_group_id']} = 1 total user. No question created because no one else to celebrate.")
        continue
      # ------------------------ get total teammate count end ------------------------
      user_product_question_already_created = False
      # ------------------------ loop through questions already created rows start ------------------------
      found_question_id = None
      for i_question_dict in db_arr_of_dict_custom_questions_created:
        if i_celebrate_dict['fk_user_id'] == i_question_dict['fk_user_id'] and i_question_dict['product'] == i_celebrate_dict['event']:
          user_product_question_already_created = True
          found_question_id = i_question_dict['id']
      # ------------------------ loop through questions already created rows end ------------------------
      # ------------------------ if already created then update db start ------------------------
      if user_product_question_already_created == True:
        if i_celebrate_dict['status'] == True:
          pass
        elif i_celebrate_dict['status'] == False:
          update_input_arr = [found_question_id, i_celebrate_dict['fk_user_id'], i_celebrate_dict['event']]
          update_manual_function(postgres_connection, postgres_cursor, 'update_email_1', update_input_arr)
          print('updated db on 2nd run!')
      # ------------------------ if already created then update db end ------------------------
      if user_product_question_already_created == False:
        # ------------------------ openai start ------------------------
        print('waiting 20 seconds')
        time.sleep(20) # to not hit a rate limit on each run
        chatgpt_message = f"I am creating a multiple choice question that has only 1 correct answer. The question is 'what is your favorite {i_celebrate_dict['question'][:-1]}' and the only correct answer is '{i_celebrate_dict['answer']}'. Return a python array of 3 similar but incorrect answer choices. The python array returned should be given the name 'results_arr'."
        chatgpt_response_str = openai_chat_gpt_prompt_result_function(chatgpt_message)
        chatgpt_response_arr = openai_chat_gpt_parse_results_to_arr_function(chatgpt_response_str)
        answer_choices_arr = chatgpt_response_arr
        answer_choices_arr.append(i_celebrate_dict['answer'])
        random.shuffle(answer_choices_arr)
        # ------------------------ openai end ------------------------
        # ------------------------ determine correct answer choice start ------------------------
        correct_index = None
        correct_answer_choice = None
        for i in range(len(answer_choices_arr)):
          if answer_choices_arr[i] == i_celebrate_dict['answer']:
            correct_index = i
        if correct_index == 0:
          correct_answer_choice = 'A'
        elif correct_index == 1:
          correct_answer_choice = 'B'
        elif correct_index == 2:
          correct_answer_choice = 'C'
        elif correct_index == 3:
          correct_answer_choice = 'D'
        # ------------------------ determine correct answer choice end ------------------------
        # ------------------------ user info start ------------------------
        db_arr_of_dict_user = select_manual_function(postgres_connection, postgres_cursor, 'select_user_2', i_celebrate_dict['fk_user_id'])
        i_celebrate_dict['name'] = db_arr_of_dict_user[0]['name']
        i_celebrate_dict['group_id'] = db_arr_of_dict_user[0]['group_id']
        # ------------------------ user info end ------------------------
        # ------------------------ additional info start ------------------------
        question_id = create_uuid_function('questionid_')
        question_created_timestamp=create_timestamp_function()
        status = True
        categories = None
        title = None
        aws_image_uuid = None
        aws_image_uuid = None
        aws_image_url = None
        if i_celebrate_dict['event'] == 'birthday':
          title = 'Birthday celebration!'
          aws_image_uuid = 'celebrateBirthday'
          aws_image_url = 'https://triviafy-create-question-image-uploads.s3.us-east-2.amazonaws.com/celebrateBirthday.jpg'
        elif i_celebrate_dict['event'] == 'job_start_date':
          title = 'Anniversary celebration!'
          aws_image_uuid = 'celebrateAnniversary'
          aws_image_url = 'https://triviafy-create-question-image-uploads.s3.us-east-2.amazonaws.com/celebrateAnniversary.jpg'
        question = f"What is {i_celebrate_dict['name']}'s favorite {i_celebrate_dict['question']}"
        option_e = None
        submission = 'submitted'
        # ------------------------ additional info end ------------------------
        # ------------------------ create new question start ------------------------
        insert_inputs_arr = [question_id, question_created_timestamp, i_celebrate_dict['fk_user_id'], status, categories, title, question, answer_choices_arr[0].lower().capitalize(), answer_choices_arr[1].lower().capitalize(), answer_choices_arr[2].lower().capitalize(), answer_choices_arr[3].lower().capitalize(), option_e, correct_answer_choice, aws_image_uuid, aws_image_url, submission, i_celebrate_dict['event'], i_celebrate_dict['group_id']]
        insert_manual_function(postgres_connection, postgres_cursor, 'insert_celebrate_1', insert_inputs_arr)
        # ------------------------ create new question end ------------------------
        # ------------------------ update db start ------------------------
        update_input_arr = [question_id, i_celebrate_dict['fk_user_id'], i_celebrate_dict['event']]
        update_manual_function(postgres_connection, postgres_cursor, 'update_email_1', update_input_arr)
        print('updated db on 1st run!')
        # ------------------------ update db end ------------------------
    # ------------------------ loop through celebrate rows end ------------------------
  except Exception as e:
    print(f'Exception: {e}')
  # ------------------------ loop through logic end ------------------------
  # ------------------------ close connection start ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ close connection end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ run function start ------------------------
if __name__ == "__main__":
  run_job_function()
# ------------------------ run function end ------------------------
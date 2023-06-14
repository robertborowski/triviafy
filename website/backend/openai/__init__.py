
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
import openai
from website.models import UserCelebrateObj,ActivityACreatedQuestionsObj, UserObj
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
from sqlalchemy import and_, or_
from datetime import date
from website import db
import random
from website.backend.candidates.send_emails import send_email_template_function
# ------------------------ imports end ------------------------

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
def openai_chat_gpt_parse_results_to_arr_polling_function(chatgpt_response_str):
  result_arr_of_dict = None
  try:
    # ------------------------ remove line breaks from str start ------------------------
    chatgpt_response_str = chatgpt_response_str.replace('\n','')
    chatgpt_response_str = chatgpt_response_str.replace('~','')
    # ------------------------ remove line breaks from str end ------------------------
    # ------------------------ split the string into questions arr start ------------------------
    result_arr = chatgpt_response_str.split('polling_question_')
    # ------------------------ split the string into questions arr end ------------------------
    # ------------------------ remove any strings that are not part of the desired result start ------------------------
    result_arr_copy = result_arr[:]
    for i_str in result_arr_copy:
      if 'polling_answer_' not in i_str:
        result_arr.remove(i_str)
    # ------------------------ remove any strings that are not part of the desired result end ------------------------
    # ------------------------ manipulate to array of dicts start ------------------------
    result_arr_of_dict = []
    for i in result_arr:
      i_dict = {}
      # ------------------------ breakup question start ------------------------
      question_segments = i.split(":")
      question_pulled = question_segments[1].strip()
      question = question_pulled.replace('polling_answer_1','').strip()
      i_dict['question'] = question
      # ------------------------ breakup question end ------------------------
      # ------------------------ breakup answers start ------------------------
      answer_segments = i.split(":")[2:]
      answers_arr = []
      for i_answer in answer_segments:
        search_string = 'polling_answer'
        if search_string in i_answer:
          found_index = i_answer.find(search_string)
          i_answer = i_answer[:found_index]
        i_answer = i_answer.strip()
        answers_arr.append(i_answer)
      i_dict['answer_choices'] = answers_arr
      # ------------------------ breakup answers end ------------------------
      result_arr_of_dict.append(i_dict)
    # ------------------------ manipulate to array of dicts end ------------------------
  except:
    pass
  return result_arr_of_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_openai_starter_poll_questions_function(show_name):
  # ------------------------ openai start ------------------------
  chatgpt_message = f"I would like you to create 10 polling questions for me that follow the following rules. Rule #1: The polling questions should be aimed at the average listener of the podcast '{show_name}'. Rule #2: Please avoid general polling questions that could be asked about any other podcast. Rule #3: Each polling question should have at least 5 options as answer choices. Rule #4: Each question number should be preceded with the word 'polling_question_', for example question 1 should be titled 'polling_question_1' and so on until 'polling_question_10'. Rule #5: Each answer option should be preceded with the word 'polling_answer_', for example answer option 1 should be titled 'polling_answer_1' and so on until 'polling_answer_5'."
  chatgpt_response_str = openai_chat_gpt_prompt_result_function(chatgpt_message)
  chatgpt_response_arr_of_dicts = openai_chat_gpt_parse_results_to_arr_polling_function(chatgpt_response_str)
  # ------------------------ openai end ------------------------
  # ------------------------ sanitize/check results as expected start ------------------------
  if chatgpt_response_arr_of_dicts == None or chatgpt_response_arr_of_dicts == []:
    # ------------------------ email self start ------------------------
    try:
      output_to_email = os.environ.get('TRIVIAFY_NOTIFICATIONS_EMAIL')
      output_subject = f'Failure on ChatGPT parsing polls for {show_name}'
      output_body = f'Failure on ChatGPT parsing polls for {show_name}'
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
    # ------------------------ email self end ------------------------
  # ------------------------ sanitize/check results as expected end ------------------------
  return chatgpt_response_arr_of_dicts
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_openai_multiple_choice_question_function(current_user, input_db_obj_to_update):
  question_id_to_return = None
  # ------------------------ get todays variables start ------------------------
  today = date.today()    # <class 'datetime.date'> | 2023-06-03
  current_day = today.day
  current_month = today.month
  current_year = today.year
  # ------------------------ get todays variables end ------------------------
  # ------------------------ get total count needed start ------------------------
  db_celebrate_objs = UserCelebrateObj.query.filter_by(fk_group_id=current_user.group_id,status=False,celebrate_month=int(current_month),celebrate_day=int(current_day))
  db_arr_of_dict_custom_questions_needed = []
  for i_obj in db_celebrate_objs:
    if i_obj.fk_question_id == None or i_obj.fk_question_id == '':
      i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
      db_arr_of_dict_custom_questions_needed.append(i_dict)
  # ------------------------ get total count needed end ------------------------
  # ------------------------ get all tables start ------------------------
  # db_arr_of_dict_custom_questions_created = select_manual_function(postgres_connection, postgres_cursor, 'select_celebrations_for_openai')
  db_arr_of_dict_custom_questions_created = []
  db_custom_questions_obj = ActivityACreatedQuestionsObj.query.filter(or_(ActivityACreatedQuestionsObj.product=='birthday',ActivityACreatedQuestionsObj.product=='job_start_date'),ActivityACreatedQuestionsObj.fk_group_id==current_user.group_id)
  for i_obj in db_custom_questions_obj:
    i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
    db_arr_of_dict_custom_questions_created.append(i_dict)
  # ------------------------ get all tables end ------------------------
  # ------------------------ loop through logic start ------------------------
  chatgpt_response_str = None
  try:
    # ------------------------ loop through celebrate rows start ------------------------
    for i_celebrate_dict in db_arr_of_dict_custom_questions_needed:
      # ------------------------ get total teammate count start ------------------------
      db_teammates_objs = UserObj.query.filter_by(group_id=current_user.group_id)
      if db_teammates_objs.count() == 1:
        localhost_print_function(f"group_id: {i_celebrate_dict['fk_group_id']} = 1 total user. No question created because no one else to celebrate.")
        continue
      # ------------------------ get total teammate count end ------------------------
      # ------------------------ loop through questions already created rows start ------------------------
      user_product_question_already_created = False
      found_question_id = None
      db_custom_questions_obj = ActivityACreatedQuestionsObj.query.filter(or_(ActivityACreatedQuestionsObj.product=='birthday',ActivityACreatedQuestionsObj.product=='job_start_date'),ActivityACreatedQuestionsObj.fk_user_id==i_celebrate_dict['fk_user_id']).first()
      if db_custom_questions_obj != None and db_custom_questions_obj != []:
        if db_custom_questions_obj.count() != 0:
          user_product_question_already_created = True
          found_question_id = db_custom_questions_obj.id
      # ------------------------ loop through questions already created rows end ------------------------
      # ------------------------ if already created then update db start ------------------------
      if user_product_question_already_created == True:
        if i_celebrate_dict['status'] == True:
          pass
        elif i_celebrate_dict['status'] == False:
          input_db_obj_to_update.status = True
          input_db_obj_to_update.fk_question_id = found_question_id
          db.session.commit()
          question_id_to_return = found_question_id
          print('updated db on 2nd run!')
      # ------------------------ if already created then update db end ------------------------
      if user_product_question_already_created == False:
        # ------------------------ openai start ------------------------
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
        db_teammates_objs = UserObj.query.filter_by(id=i_celebrate_dict['fk_user_id']).first()
        i_celebrate_dict['name'] = db_teammates_objs.name
        i_celebrate_dict['group_id'] = db_teammates_objs.group_id
        # ------------------------ user info end ------------------------
        # ------------------------ additional info start ------------------------
        submitted_question_id = create_uuid_function('questionid_')
        question_created_timestamp=create_timestamp_function()
        submitted_status = True
        submitted_categories = None
        submitted_title = None
        aws_image_uuid = None
        aws_image_url = None
        if i_celebrate_dict['event'] == 'birthday':
          submitted_title = 'Birthday celebration!'
          aws_image_uuid = 'celebrateBirthday'
          aws_image_url = 'https://triviafy-create-question-image-uploads.s3.us-east-2.amazonaws.com/celebrateBirthday.jpg'
        elif i_celebrate_dict['event'] == 'job_start_date':
          submitted_title = 'Anniversary celebration!'
          aws_image_uuid = 'celebrateAnniversary'
          aws_image_url = 'https://triviafy-create-question-image-uploads.s3.us-east-2.amazonaws.com/celebrateAnniversary.jpg'
        submitted_question = f"What is {i_celebrate_dict['name']}'s favorite {i_celebrate_dict['question']}"
        submitted_option_e = None
        submitted_submission = 'submitted'
        # ------------------------ additional info end ------------------------
        # ------------------------ add to db start ------------------------
        try:
          # ------------------------ append answers end ------------------------
          new_row = ActivityACreatedQuestionsObj(
            id = submitted_question_id,
            created_timestamp = question_created_timestamp,
            fk_user_id = i_celebrate_dict['fk_user_id'],
            status = submitted_status,
            categories = submitted_categories,
            title = submitted_title,
            question = submitted_question,
            option_a = answer_choices_arr[0].lower().capitalize(),
            option_b = answer_choices_arr[1].lower().capitalize(),
            option_c = answer_choices_arr[2].lower().capitalize(),
            option_d = answer_choices_arr[3].lower().capitalize(),
            option_e = submitted_option_e,
            answer = correct_answer_choice,
            aws_image_uuid = aws_image_uuid,
            aws_image_url = aws_image_url,
            submission = submitted_submission,
            product = i_celebrate_dict['event'],
            fk_group_id = i_celebrate_dict['group_id']
          )
          db.session.add(new_row)
          db.session.commit()
        except:
          localhost_print_function('did not create question in db')
          pass
        # ------------------------ add to db end ------------------------
        # ------------------------ update db start ------------------------
        input_db_obj_to_update.status = True
        input_db_obj_to_update.fk_question_id = submitted_question_id
        db.session.commit()
        question_id_to_return = submitted_question_id
        print('updated db on 1st run!')
        # ------------------------ update db end ------------------------
    # ------------------------ loop through celebrate rows end ------------------------
  except Exception as e:
    print(f'Exception: {e} | chatgpt_response_str: {chatgpt_response_str}')
  # ------------------------ loop through logic end ------------------------
  return question_id_to_return
# ------------------------ individual function end ------------------------
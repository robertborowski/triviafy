# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website import db
from flask_login import current_user
# ------------------------ imports end ------------------------

localhost_print_function('=========================================== sql_statements_select __init__ START ===========================================')

# ------------------------ individual function start ------------------------
def select_general_function(tag_query_to_use, additional_input=None, additional_input2=None):
  localhost_print_function('=========================================== select_general_function START ===========================================')
  try:
    current_user_id_defined_var = current_user.id
  except:
    current_user_id_defined_var = None
  # ------------------------ select queries start ------------------------
  select_queries_dict = {
    'select_specific_assessment_questions': {
      'raw_query': f"SELECT \
                      question_uuid, question_categories_list, question_actual_question, question_difficulty, question_hint, question_title, question_image_aws_url, question_answers_list \
                    FROM \
                      triviafy_all_questions_table \
                    WHERE \
                      question_uuid IN ({additional_input}) \
                    ORDER BY \
                      question_timestamp_created;",
      'input_args': {}
    },
    'select_specific_assessment_questions_v2': {
      'raw_query': f"SELECT \
                      id, categories, question, title, aws_image_url, answer, option_a, option_b, option_c, option_d \
                    FROM \
                      created_questions_obj \
                    WHERE \
                      id IN ({additional_input}) \
                    ORDER BY \
                      created_timestamp;",
      'input_args': {}
    },
    'select_specific_assessment_questions_v3': {
      'raw_query': f"SELECT \
                      id, categories, question, title, aws_image_url, answer, option_a, option_b, option_c, option_d, option_e \
                    FROM \
                      created_questions_obj \
                    WHERE \
                      id = {additional_input};",
      'input_args': {}
    },
    'select_all_capacity_options': {
      'raw_query': 'SELECT id FROM candidates_capacity_options_obj',
      'input_args': {}
    },
    'select_if_desired_languages_captured': {
      'raw_query': 'SELECT desired_languages FROM candidates_desired_languages_obj WHERE user_id_fk = :val ORDER BY created_timestamp DESC',
      'input_args': {'val': current_user_id_defined_var}
    },
    'select_all_candidate_categories_chosen': {
      'raw_query': "SELECT DISTINCT q.question_categories_list FROM triviafy_all_questions_table AS q WHERE q.question_categories_list LIKE'%Candidates%' ORDER BY q.question_categories_list;",
      'input_args': {}
    },
    'select_all_candidate_categories_chosen_v2': {
      'raw_query': "SELECT DISTINCT q.categories FROM created_questions_obj AS q WHERE q.status=TRUE AND q.product='candidates' ORDER BY q.categories;",
      'input_args': {}
    },
    'select_all_questions_for_x_categories': {
      'raw_query': f"SELECT \
                      question_uuid, question_categories_list, question_actual_question, question_difficulty, question_hint, question_title, question_image_aws_url, question_answers_list \
                    FROM \
                      triviafy_all_questions_table \
                    WHERE \
                      (question_approved_for_release = TRUE AND question_status_for_creator = 'Approved') \
                      AND ({additional_input}) \
                    ORDER BY \
                      RANDOM();",
      'input_args': {}
    },
    'select_all_questions_for_x_categories_v2': {
      'raw_query': f"SELECT \
                      id, categories, question, title, aws_image_url, answer, option_a, option_b, option_c, option_d, option_e \
                    FROM \
                      created_questions_obj \
                    WHERE \
                      status = TRUE \
                      AND ({additional_input}) \
                    ORDER BY \
                      RANDOM();",
      'input_args': {}
    },
    'select_all_questions_for_x_categories_v3': {
      'raw_query': f"SELECT \
                      id \
                    FROM \
                      created_questions_obj \
                    WHERE \
                      status = TRUE AND product='candidates' \
                      AND ({additional_input}) \
                    ORDER BY \
                      RANDOM() \
                    LIMIT 10;",
      'input_args': {}
    },
    'select_one_question_for_x_categories_v1': {
      'raw_query': f"SELECT \
                      id \
                    FROM \
                      created_questions_obj \
                    WHERE \
                      status = TRUE \
                      AND ({additional_input}) \
                      AND id NOT IN ({additional_input2})\
                    ORDER BY \
                      RANDOM() \
                    LIMIT 1;",
      'input_args': {}
    },
    'select_question_id_actually_exists': {
      'raw_query': "SELECT question_uuid FROM triviafy_all_questions_table WHERE question_uuid=:val;",
      'input_args': {'val': additional_input}
    },
    'select_question_id_actually_exists_v2': {
      'raw_query': "SELECT id FROM created_questions_obj WHERE id=:val;",
      'input_args': {'val': additional_input}
    }
  }
  # ------------------------ select queries end ------------------------
  # ------------------------ general query start ------------------------
  # result_obj = db.session.execute('SELECT * FROM user_obj WHERE email = :val', {'val': 'a@a.com'})
  result_obj = db.session.execute(select_queries_dict[tag_query_to_use]['raw_query'], select_queries_dict[tag_query_to_use]['input_args'])
  # ------------------------ general query end ------------------------
  # ------------------------ default result start ------------------------
  result_arr_of_dicts = []
  # ------------------------ default result end ------------------------
  # ------------------------ existing result start ------------------------
  for i_row in result_obj:
    # result_dict = dict(i_row.items()) # convert to dict keyed by column names
    result_dict = dict(i_row) # convert to dict keyed by column names
    result_arr_of_dicts.append(result_dict)
  # ------------------------ existing result end ------------------------
  localhost_print_function('=========================================== select_general_function START ===========================================')
  return result_arr_of_dicts
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== sql_statements_select __init__ END ===========================================')
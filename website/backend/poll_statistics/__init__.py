# ------------------------ imports start ------------------------
from website.models import UserAttributesObj
from website.backend.sql_statements.select import select_general_function
from website.backend.get_create_obj import get_age_demographics_function
import pprint
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_percent_data_function(input_numerator, input_denominator):
  result = 0
  try:
    result = float(float(float(input_numerator)/float(input_denominator)) * float(100))
  except:
    pass
  return int(result)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_chart_data_function(chart_name, page_dict, total_answered_arr_of_dict):
  if chart_name == 'chart_answer_distribution':
    # ------------------------ loop answered count start ------------------------
    # ------------------------ set count to zero for options start ------------------------
    for k,v in page_dict['poll_dict']['answer_choices_dict'].items():
      page_dict['poll_statistics_dict']['vote_count_by_answer_choice_dict'][k] = 0
    # ------------------------ set count to zero for options end ------------------------
    for i_poll_answered_dict in total_answered_arr_of_dict:
      i_poll_answer_submitted = i_poll_answered_dict['poll_answer_submitted']
      for k,v in page_dict['poll_dict']['answer_choices_dict'].items():
        if i_poll_answer_submitted == v:
          try:
            page_dict['poll_statistics_dict']['vote_count_by_answer_choice_dict'][k] += 1
          except:
            pass
    # ------------------------ loop answered count end ------------------------
    # ------------------------ loop answered percent start ------------------------
    for k, v in page_dict['poll_statistics_dict']['vote_count_by_answer_choice_dict'].items():
      result = get_percent_data_function(v, page_dict['poll_statistics_dict']['total_latest_poll_answers'])
      page_dict['poll_statistics_dict']['vote_percent_by_answer_choice_dict'][k] = result
    # ------------------------ loop answered percent end ------------------------
    # ------------------------ chart variables for answered percent start ------------------------
    for k,v in page_dict['poll_statistics_dict']['vote_percent_by_answer_choice_dict'].items():
      page_dict['poll_statistics_dict']['chart_answer_distribution']['labels'].append(k)
      page_dict['poll_statistics_dict']['chart_answer_distribution']['values'].append(v)
    # ------------------------ chart variables for answered percent end ------------------------
  if chart_name == 'chart_generation_distribution':
    # ------------------------ get all user id's that voted start ------------------------
    for i_poll_answered_dict in total_answered_arr_of_dict:
      page_dict['poll_statistics_dict']['all_user_ids_participated'].append(i_poll_answered_dict['fk_user_id'])
    # ------------------------ get all user id's that voted end ------------------------
    # ------------------------ loop answered count start ------------------------
    year_generation_dict, generation_options_arr = get_age_demographics_function()
    # ------------------------ set count to zero for options start ------------------------
    for i in generation_options_arr:
      page_dict['poll_statistics_dict']['vote_count_by_generation_dict'][i] = 0
    # ------------------------ set count to zero for options end ------------------------
    for i_user in page_dict['poll_statistics_dict']['all_user_ids_participated']:
      try:
        db_user_obj = UserAttributesObj.query.filter_by(fk_user_id=i_user,attribute_code='attribute_birthday').first()
        user_generation = year_generation_dict[str(db_user_obj.attribute_year)]
        page_dict['poll_statistics_dict']['vote_count_by_generation_dict'][user_generation] += 1
      except:
        pass
    # ------------------------ loop answered count end ------------------------
    # ------------------------ loop answered percent start ------------------------
    for k, v in page_dict['poll_statistics_dict']['vote_count_by_generation_dict'].items():
      result = get_percent_data_function(v, page_dict['poll_statistics_dict']['total_latest_poll_answers'])
      page_dict['poll_statistics_dict']['vote_percent_by_generation_dict'][k] = result
    # ------------------------ loop answered percent end ------------------------
    # ------------------------ chart variables for answered percent start ------------------------
    for k,v in page_dict['poll_statistics_dict']['vote_percent_by_generation_dict'].items():
      if k == 'silent':
        continue
      fixed_word = k
      if k == 'boomers':
        fixed_word = 'Boomers'
      elif k == 'gen_x':
        fixed_word = 'Gen X'
      elif k == 'millenials':
        fixed_word = 'Millenials'
      elif k == 'gen_z':
        fixed_word = 'Gen Z'
      page_dict['poll_statistics_dict']['chart_generation_distribution']['labels'].append(fixed_word)
      page_dict['poll_statistics_dict']['chart_generation_distribution']['values'].append(v)
    # ------------------------ chart variables for answered percent end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------

# ------------------------ individual function start ------------------------
def get_poll_statistics_function(current_user, page_dict):
  # ------------------------ set variables start ------------------------
  page_dict['poll_statistics_dict'] = {}
  # total answered
  page_dict['poll_statistics_dict']['total_latest_poll_answers'] = 0
  # users participated
  page_dict['poll_statistics_dict']['all_user_ids_participated'] = []
  # chart answer choice
  page_dict['poll_statistics_dict']['vote_count_by_answer_choice_dict'] = {}
  page_dict['poll_statistics_dict']['vote_percent_by_answer_choice_dict'] = {}
  page_dict['poll_statistics_dict']['chart_answer_distribution'] = {}
  page_dict['poll_statistics_dict']['chart_answer_distribution']['labels'] = []
  page_dict['poll_statistics_dict']['chart_answer_distribution']['values'] = []
  # chart generations
  page_dict['poll_statistics_dict']['vote_count_by_generation_dict'] = {}
  page_dict['poll_statistics_dict']['vote_percent_by_generation_dict'] = {}
  page_dict['poll_statistics_dict']['chart_generation_distribution'] = {}
  page_dict['poll_statistics_dict']['chart_generation_distribution']['labels'] = []
  page_dict['poll_statistics_dict']['chart_generation_distribution']['values'] = []
  # ------------------------ set variables end ------------------------
  # ------------------------ pull variables start ------------------------
  poll_id = page_dict['url_poll_id']
  show_id = page_dict['url_show_id']
  # ------------------------ pull variables end ------------------------
  # ------------------------ get total answered start ------------------------
  total_answered_arr_of_dict = select_general_function('select_query_general_4', poll_id)
  try:
    page_dict['poll_statistics_dict']['total_latest_poll_answers'] = int(len(total_answered_arr_of_dict))
  except:
    pass
  # ------------------------ get total answered end ------------------------
  # ------------------------ get answer percent distribution start ------------------------
  page_dict = get_chart_data_function('chart_answer_distribution', page_dict, total_answered_arr_of_dict)
  # ------------------------ get answer percent distribution end ------------------------
  # ------------------------ get generational percent distribution start ------------------------
  page_dict = get_chart_data_function('chart_generation_distribution', page_dict, total_answered_arr_of_dict)
  # ------------------------ get generational percent distribution end ------------------------
  print(' ------------- 50 ------------- ')
  print(pprint.pformat(page_dict, indent=2))
  print(' ------------- 50 ------------- ')
  return page_dict
# ------------------------ individual function end ------------------------
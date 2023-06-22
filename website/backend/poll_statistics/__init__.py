# ------------------------ imports start ------------------------
from website.models import UserAttributesObj, PollsAnsweredObj
from website.backend.sql_statements.select import select_general_function
from website.backend.get_create_obj import get_age_demographics_function, get_age_group_function, get_gender_arr_function
import pprint
from website.backend.dates import user_years_old_at_timestamp_function
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
def get_chart_data_function(chart_name, page_dict, total_answered_arr_of_dict, current_user):
  # ------------------------ chart answer choices start ------------------------
  if chart_name == 'chart_answer_distribution':
    # ------------------------ set count to zero for options start ------------------------
    for k,v in page_dict['poll_dict']['answer_choices_dict'].items():
      page_dict['poll_statistics_dict']['vote_count_by_answer_choice_dict'][k] = 0
    # ------------------------ set count to zero for options end ------------------------
    # ------------------------ loop for count start ------------------------
    for i_poll_answered_dict in total_answered_arr_of_dict:
      i_poll_answer_submitted = i_poll_answered_dict['poll_answer_submitted']
      for k,v in page_dict['poll_dict']['answer_choices_dict'].items():
        if i_poll_answer_submitted == v:
          try:
            page_dict['poll_statistics_dict']['vote_count_by_answer_choice_dict'][k] += 1
          except:
            pass
    # ------------------------ loop for count end ------------------------
    # ------------------------ loop for percent start ------------------------
    for k, v in page_dict['poll_statistics_dict']['vote_count_by_answer_choice_dict'].items():
      result = get_percent_data_function(v, page_dict['poll_statistics_dict']['total_latest_poll_answers'])
      page_dict['poll_statistics_dict']['vote_percent_by_answer_choice_dict'][k] = result
    # ------------------------ loop for percent end ------------------------
    # ------------------------ chart variables start ------------------------
    for k,v in page_dict['poll_statistics_dict']['vote_percent_by_answer_choice_dict'].items():
      page_dict['poll_statistics_dict']['chart_answer_distribution']['labels'].append(k)
      page_dict['poll_statistics_dict']['chart_answer_distribution']['values'].append(v)
    # ------------------------ chart variables end ------------------------
  # ------------------------ chart answer choices end ------------------------
  # ------------------------ chart generations start ------------------------
  if chart_name == 'chart_generation_distribution':
    # ------------------------ set count to zero for options start ------------------------
    year_generation_dict, generation_options_arr = get_age_demographics_function()
    for i in generation_options_arr:
      page_dict['poll_statistics_dict']['vote_count_by_generation_dict'][i] = 0
    # ------------------------ set count to zero for options end ------------------------
    # ------------------------ loop for count start ------------------------
    for i_user in page_dict['poll_statistics_dict']['all_user_ids_participated']:
      try:
        db_user_obj = UserAttributesObj.query.filter_by(fk_user_id=i_user,attribute_code='attribute_birthday').first()
        user_generation = year_generation_dict[str(db_user_obj.attribute_year)]
        page_dict['poll_statistics_dict']['vote_count_by_generation_dict'][user_generation] += 1
      except:
        pass
    # ------------------------ loop for count end ------------------------
    # ------------------------ loop for percent start ------------------------
    for k, v in page_dict['poll_statistics_dict']['vote_count_by_generation_dict'].items():
      result = get_percent_data_function(v, page_dict['poll_statistics_dict']['total_latest_poll_answers'])
      page_dict['poll_statistics_dict']['vote_percent_by_generation_dict'][k] = result
    # ------------------------ loop for percent end ------------------------
    # ------------------------ chart variables start ------------------------
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
    # ------------------------ chart variables end ------------------------
  # ------------------------ chart generations end ------------------------
  # ------------------------ chart age groups start ------------------------
  if chart_name == 'chart_age_group_distribution':
    # ------------------------ set count to zero for options start ------------------------
    age_group_arr = get_age_group_function()
    for i in age_group_arr:
      page_dict['poll_statistics_dict']['vote_count_by_age_group_dict'][i] = 0
    # ------------------------ set count to zero for options end ------------------------
    # ------------------------ loop for count start ------------------------
    for i_poll_answered_dict in total_answered_arr_of_dict:
      i_poll_answer_submitted_timestamp = i_poll_answered_dict['created_timestamp']
      db_user_obj = UserAttributesObj.query.filter_by(fk_user_id=i_poll_answered_dict['fk_user_id'],attribute_code='attribute_birthday').first()
      age_at_submission = user_years_old_at_timestamp_function(i_poll_answer_submitted_timestamp, int(db_user_obj.attribute_year), int(db_user_obj.attribute_month), int(db_user_obj.attribute_day))
      if age_at_submission <= 29:
        page_dict['poll_statistics_dict']['vote_count_by_age_group_dict']["18-20's"] += 1
      elif age_at_submission >= 30 and age_at_submission <= 39:
        page_dict['poll_statistics_dict']['vote_count_by_age_group_dict']["30's"] += 1
      elif age_at_submission >= 40 and age_at_submission <= 49:
        page_dict['poll_statistics_dict']['vote_count_by_age_group_dict']["40's"] += 1
      elif age_at_submission >= 50 and age_at_submission <= 59:
        page_dict['poll_statistics_dict']['vote_count_by_age_group_dict']["50's"] += 1
      elif age_at_submission >= 60:
        page_dict['poll_statistics_dict']['vote_count_by_age_group_dict']["60's +"] += 1
    # ------------------------ loop for count end ------------------------
    # ------------------------ loop for percent start ------------------------
    for k, v in page_dict['poll_statistics_dict']['vote_count_by_age_group_dict'].items():
      result = get_percent_data_function(v, page_dict['poll_statistics_dict']['total_latest_poll_answers'])
      page_dict['poll_statistics_dict']['vote_percent_by_age_group_dict'][k] = result
    # ------------------------ loop for percent end ------------------------
    # ------------------------ chart variables start ------------------------
    for k,v in page_dict['poll_statistics_dict']['vote_percent_by_age_group_dict'].items():
      page_dict['poll_statistics_dict']['chart_age_group_distribution']['labels'].append(k)
      page_dict['poll_statistics_dict']['chart_age_group_distribution']['values'].append(v)
    # ------------------------ chart variables end ------------------------
    pass
  # ------------------------ chart age groups end ------------------------
  # ------------------------ chart gender start ------------------------
  if chart_name == 'chart_gender_distribution':
    # ------------------------ check if current user provided attribute poll response start ------------------------
    db_poll_answered_obj = PollsAnsweredObj.query.filter_by(fk_user_id=current_user.id,fk_show_id='show_user_attributes',fk_poll_id='poll_user_attribute_gender').order_by(PollsAnsweredObj.created_timestamp.desc()).first()
    if db_poll_answered_obj == None or db_poll_answered_obj == []:
      page_dict['poll_statistics_dict']['user_provided_attribute_gender'] = None
    else:
      page_dict['poll_statistics_dict']['user_provided_attribute_gender'] = True
    # ------------------------ check if current user provided attribute poll response end ------------------------
    # ------------------------ set count to zero for options start ------------------------
    gender_arr = get_gender_arr_function()
    for i in gender_arr:
      page_dict['poll_statistics_dict']['vote_count_by_gender_dict'][i] = 0
    # ------------------------ set count to zero for options end ------------------------
    # ------------------------ loop for count start ------------------------
    total_answered_arr_of_dict = select_general_function('select_query_general_4', 'poll_user_attribute_gender')
    for i_poll_answered_dict in total_answered_arr_of_dict:
      i_poll_answer_submitted = i_poll_answered_dict['poll_answer_submitted']
      if i_poll_answer_submitted == 'Male':
        page_dict['poll_statistics_dict']['vote_count_by_gender_dict']['male'] += 1
      elif i_poll_answer_submitted == 'Female':
        page_dict['poll_statistics_dict']['vote_count_by_gender_dict']['female'] += 1
      elif i_poll_answer_submitted == 'Ideology based':
        page_dict['poll_statistics_dict']['vote_count_by_gender_dict']['ideology'] += 1
    # ------------------------ loop for count end ------------------------
    # ------------------------ loop for percent start ------------------------
    for k, v in page_dict['poll_statistics_dict']['vote_count_by_gender_dict'].items():
      result = get_percent_data_function(v, page_dict['poll_statistics_dict']['total_latest_poll_answers'])
      page_dict['poll_statistics_dict']['vote_percent_by_gender_dict'][k] = result
    # ------------------------ loop for percent end ------------------------
    # ------------------------ chart variables start ------------------------
    for k,v in page_dict['poll_statistics_dict']['vote_percent_by_gender_dict'].items():
      page_dict['poll_statistics_dict']['chart_gender_distribution']['labels'].append(k)
      page_dict['poll_statistics_dict']['chart_gender_distribution']['values'].append(v)
    # ------------------------ chart variables end ------------------------
  # ------------------------ chart gender end ------------------------
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
  # chart age groups
  page_dict['poll_statistics_dict']['vote_count_by_age_group_dict'] = {}
  page_dict['poll_statistics_dict']['vote_percent_by_age_group_dict'] = {}
  page_dict['poll_statistics_dict']['chart_age_group_distribution'] = {}
  page_dict['poll_statistics_dict']['chart_age_group_distribution']['labels'] = []
  page_dict['poll_statistics_dict']['chart_age_group_distribution']['values'] = []
  # chart gender
  page_dict['poll_statistics_dict']['user_provided_attribute_gender'] = None
  page_dict['poll_statistics_dict']['vote_count_by_gender_dict'] = {}
  page_dict['poll_statistics_dict']['vote_percent_by_gender_dict'] = {}
  page_dict['poll_statistics_dict']['chart_gender_distribution'] = {}
  page_dict['poll_statistics_dict']['chart_gender_distribution']['labels'] = []
  page_dict['poll_statistics_dict']['chart_gender_distribution']['values'] = []
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
  # ------------------------ get all user id's that voted start ------------------------
  for i_poll_answered_dict in total_answered_arr_of_dict:
    page_dict['poll_statistics_dict']['all_user_ids_participated'].append(i_poll_answered_dict['fk_user_id'])
  # ------------------------ get all user id's that voted end ------------------------
  # ------------------------ get chart data start ------------------------
  page_dict = get_chart_data_function('chart_answer_distribution', page_dict, total_answered_arr_of_dict, current_user)
  page_dict = get_chart_data_function('chart_generation_distribution', page_dict, total_answered_arr_of_dict, current_user)
  page_dict = get_chart_data_function('chart_age_group_distribution', page_dict, total_answered_arr_of_dict, current_user)
  page_dict = get_chart_data_function('chart_gender_distribution', page_dict, total_answered_arr_of_dict, current_user)
  # ------------------------ get chart data end ------------------------
  print(' ------------- 50 ------------- ')
  print(pprint.pformat(page_dict, indent=2))
  print(' ------------- 50 ------------- ')
  return page_dict
# ------------------------ individual function end ------------------------
# ------------------------ imports start ------------------------
from website.models import PollsAnsweredObj
from website.backend.sql_statements.select import select_general_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_poll_statistics(current_user, page_dict):
  # ------------------------ pull variables start ------------------------
  poll_id = page_dict['url_poll_id']
  show_id = page_dict['url_show_id']
  # ------------------------ pull variables end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['poll_statistics_dict'] = {}
  page_dict['poll_statistics_dict']['total_latest_poll_answers'] = 0
  page_dict['poll_statistics_dict']['answer_choice_count_distribution_dict'] = {}
  page_dict['poll_statistics_dict']['answer_choice_percent_distribution_dict'] = {}
  page_dict['poll_statistics_dict']['chart_answer_distribution'] = {}
  page_dict['poll_statistics_dict']['chart_answer_distribution']['labels'] = []
  page_dict['poll_statistics_dict']['chart_answer_distribution']['values'] = []
  # ------------------------ set variables end ------------------------
  # ------------------------ get total answered start ------------------------
  total_answered_arr_of_dict = select_general_function('select_query_general_4', poll_id)
  try:
    page_dict['poll_statistics_dict']['total_latest_poll_answers'] = int(len(total_answered_arr_of_dict))
  except:
    pass
  # ------------------------ get total answered end ------------------------
  # ------------------------ loop answered count start ------------------------
  for k,v in page_dict['poll_dict']['answer_choices_dict'].items():
    page_dict['poll_statistics_dict']['answer_choice_count_distribution_dict'][k] = 0
  for i_poll_answered_dict in total_answered_arr_of_dict:
    i_poll_answer_submitted = i_poll_answered_dict['poll_answer_submitted']
    for k,v in page_dict['poll_dict']['answer_choices_dict'].items():
      if i_poll_answer_submitted == v:
        try:
          page_dict['poll_statistics_dict']['answer_choice_count_distribution_dict'][k] += 1
        except:
          pass
  # ------------------------ loop answered count start ------------------------
  # ------------------------ loop answered percent start ------------------------
  for k, v in page_dict['poll_statistics_dict']['answer_choice_count_distribution_dict'].items():
    result = 0
    try:
      result = float(float(float(v)/float(page_dict['poll_statistics_dict']['total_latest_poll_answers'])) * float(100))
    except:
      pass
    page_dict['poll_statistics_dict']['answer_choice_percent_distribution_dict'][k] = int(result)
  # ------------------------ loop answered percent end ------------------------
  # ------------------------ variables for chart start ------------------------
  for k,v in page_dict['poll_statistics_dict']['answer_choice_percent_distribution_dict'].items():
    page_dict['poll_statistics_dict']['chart_answer_distribution']['labels'].append(k)
    page_dict['poll_statistics_dict']['chart_answer_distribution']['values'].append(v)
  # ------------------------ variables for chart end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------
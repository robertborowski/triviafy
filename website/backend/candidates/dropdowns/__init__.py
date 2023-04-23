# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.candidates.datetime_manipulation import days_times_timezone_arr_function
from website.backend.candidates.autogeneration import question_choices_function
# ------------------------ imports end ------------------------

localhost_print_function('=========================================== dropdowns __init__ START ===========================================')
# ------------------------ individual function start ------------------------
def get_dropdowns_trivia_function():
  weekdays_arr, times_arr, timezone_arr = days_times_timezone_arr_function()
  quiz_cadence_arr, question_num_arr, question_type_arr = question_choices_function()
  dropdown_trivia_dict = {
    # ------------------------ individual dropdown start ------------------------
    'radio_start_day': {
      'id': 'id-radio_start_day',
      'name': 'radio_start_day',
      'title_short': 'Start day',
      'title_long': 'Team trivia should open on',
      'dropdown_arr': weekdays_arr
    }
    # ------------------------ individual dropdown end ------------------------
    # ------------------------ individual dropdown start ------------------------
    , 'radio_start_time': {
      'id': 'id-radio_start_time',
      'name': 'radio_start_time',
      'title_short': 'Start time',
      'title_long': 'Open at',
      'dropdown_arr': times_arr
    }
    # ------------------------ individual dropdown end ------------------------
    # ------------------------ individual dropdown start ------------------------
    , 'radio_end_day': {
      'id': 'id-radio_end_day',
      'name': 'radio_end_day',
      'title_short': 'End day',
      'title_long': 'Close at',
      'dropdown_arr': weekdays_arr
    }
    # ------------------------ individual dropdown end ------------------------
    # ------------------------ individual dropdown start ------------------------
    , 'radio_end_time': {
      'id': 'id-radio_end_time',
      'name': 'radio_end_time',
      'title_short': 'End time',
      'title_long': 'Closes time at',
      'dropdown_arr': times_arr
    }
    # ------------------------ individual dropdown end ------------------------
    # ------------------------ individual dropdown start ------------------------
    , 'radio_timezone': {
      'id': 'id-radio_timezone',
      'name': 'radio_timezone',
      'title_short': 'timezone',
      'title_long': 'timezoneeee',
      'dropdown_arr': timezone_arr
    }
    # ------------------------ individual dropdown end ------------------------
    # ------------------------ individual dropdown start ------------------------
    , 'radio_candence': {
      'id': 'id-radio_candence',
      'name': 'radio_candence',
      'title_short': 'candence',
      'title_long': 'cadenceeee',
      'dropdown_arr': quiz_cadence_arr
    }
    # ------------------------ individual dropdown end ------------------------
    # ------------------------ individual questions start ------------------------
    , 'radio_total_questions': {
      'id': 'id-radio_total_questions',
      'name': 'radio_total_questions',
      'title_short': 'total questions',
      'title_long': 'totttall questions',
      'dropdown_arr': question_num_arr
    }
    # ------------------------ individual questions end ------------------------
    # ------------------------ individual questions start ------------------------
    , 'radio_question_type': {
      'id': 'id-radio_question_type',
      'name': 'radio_question_type',
      'title_short': 'Question type',
      'title_long': 'question typee',
      'dropdown_arr': question_type_arr
    }
    # ------------------------ individual questions end ------------------------
  }
  return dropdown_trivia_dict
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== dropdowns __init__ END ===========================================')
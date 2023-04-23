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
    'radio_candence': {
      'id': 'id-radio_candence',
      'name': 'radio_candence',
      'title_short': 'Candence',
      'title_long': 'Candence',
      'dropdown_arr': quiz_cadence_arr,
      'type': 'secondary',
      'db_col_name': 'cadence'
    }
    # ------------------------ individual dropdown end ------------------------
    # ------------------------ individual questions start ------------------------
    , 'radio_total_questions': {
      'id': 'id-radio_total_questions',
      'name': 'radio_total_questions',
      'title_short': 'Questions per contest',
      'title_long': 'Questions per contest',
      'dropdown_arr': question_num_arr,
      'type': 'secondary',
      'db_col_name': 'total_questions'
    }
    # ------------------------ individual questions end ------------------------
    # ------------------------ individual questions start ------------------------
    , 'radio_question_type': {
      'id': 'id-radio_question_type',
      'name': 'radio_question_type',
      'title_short': 'Question type',
      'title_long': 'Question type',
      'dropdown_arr': question_type_arr,
      'type': 'secondary',
      'db_col_name': 'question_type'
    }
    # ------------------------ individual questions end ------------------------
    # ------------------------ individual dropdown start ------------------------
    , 'radio_start_day': {
      'id': 'id-radio_start_day',
      'name': 'radio_start_day',
      'title_short': 'Start day',
      'title_long': 'Start day',
      'dropdown_arr': weekdays_arr,
      'type': 'success',
      'db_col_name': 'start_day'
    }
    # ------------------------ individual dropdown end ------------------------
    # ------------------------ individual dropdown start ------------------------
    , 'radio_start_time': {
      'id': 'id-radio_start_time',
      'name': 'radio_start_time',
      'title_short': 'Start time',
      'title_long': 'Start time',
      'dropdown_arr': times_arr,
      'type': 'success',
      'db_col_name': 'start_time'
    }
    # ------------------------ individual dropdown end ------------------------
    # ------------------------ individual dropdown start ------------------------
    , 'radio_end_day': {
      'id': 'id-radio_end_day',
      'name': 'radio_end_day',
      'title_short': 'End day',
      'title_long': 'End day',
      'dropdown_arr': weekdays_arr,
      'type': 'danger',
      'db_col_name': 'end_day'
    }
    # ------------------------ individual dropdown end ------------------------
    # ------------------------ individual dropdown start ------------------------
    , 'radio_end_time': {
      'id': 'id-radio_end_time',
      'name': 'radio_end_time',
      'title_short': 'End time',
      'title_long': 'End time',
      'dropdown_arr': times_arr,
      'type': 'danger',
      'db_col_name': 'end_time'
    }
    # ------------------------ individual dropdown end ------------------------
    # ------------------------ individual dropdown start ------------------------
    , 'radio_timezone': {
      'id': 'id-radio_timezone',
      'name': 'radio_timezone',
      'title_short': 'Time zone',
      'title_long': 'Time zone',
      'dropdown_arr': timezone_arr,
      'type': 'secondary',
      'db_col_name': 'timezone'
    }
    # ------------------------ individual dropdown end ------------------------
  }
  return dropdown_trivia_dict
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== dropdowns __init__ END ===========================================')
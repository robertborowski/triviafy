# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
# ------------------------ imports end ------------------------

localhost_print_function('=========================================== lists __init__ START ===========================================')
# ------------------------ individual function start ------------------------
def get_arr_associated_index_function(input_arr):
  arr_index = []
  total_activities = len(input_arr)
  for i in range(total_activities):
    arr_index.append(i)
  return arr_index
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def make_arr_dict_function(arr, arr_index):
  dict_one = {
    'arr': arr,
    'arr_index': arr_index
  }
  return dict_one
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_team_building_activities_list_function():
  activities_list = [
    'Trivia',
    'Picture quizzes',
    'Icebreakers',
    'Employee surveys',
    'Personality tests',
    'Colleague birthday trivia',
    'Most likely to',
    'This or that',
    'Watercooler starters',
    'Word games',
    '2 player games',
    'Create custom questions'
  ]
  activities_list_index = get_arr_associated_index_function(activities_list)
  return activities_list, activities_list_index
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_marketing_list_function():
  temp_list = [
    'Google',
    'LinkedIn',
    'TikTok',
    'Twitter',
    'Facebook',
    'Instagram',
    'Word of mouth'
  ]
  temp_list_index = get_arr_associated_index_function(temp_list)
  return temp_list, temp_list_index
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_month_days_function():
  months_arr = [1,2,3,4,5,6,7,8,9,10,11,12]
  days_arr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
  month_day_dict = {
    '1': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    '2': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
    '3': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    '4': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    '5': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    '6': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    '7': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    '8': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    '9': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    '10': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    '11': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    '12': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
  }
  return months_arr, days_arr, month_day_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_favorite_questions_function():
  questions_arr = [
    "type of music or band?",
    "movie or TV show?",
    "type of food or cuisine?",
    "book or author?",
    "hobby or pastime?",
    "place to visit on vacation?",
    "season or time of year?",
    "sport or sports team?",
    "thing to do on weekends?",
    "memory from childhood?"
  ]
  questions_arr_index = get_arr_associated_index_function(questions_arr)
  return questions_arr, questions_arr_index
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_trivia_dropdowns_function():
  arr = [
    'radio_start_day',
    'radio_start_time',
    'radio_end_day',
    'radio_timezone',
    'radio_candence',
    'radio_total_questions',
    'radio_question_type'
  ]
  arr_index = get_arr_associated_index_function(arr)
  dict_one = make_arr_dict_function(arr, arr_index)
  return dict_one
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== lists __init__ END ===========================================')
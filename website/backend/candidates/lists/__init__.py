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
def get_month_days_function():
  months_arr = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  month_day_dict = {
    'January': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    'February': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
    'March': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    'April': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    'May': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    'June': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    'July': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    'August': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    'September': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    'October': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    'November': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    'December': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
  }
  return months_arr, month_day_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_favorite_questions_function():
  questions_arr = [
    "What is your favorite type of music or band?",
    "What is your favorite movie or TV show?",
    "What is your favorite type of food or cuisine?",
    "What is your favorite book or author?",
    "What is your favorite hobby or pastime?",
    "What is your favorite place to visit on vacation?",
    "What is your favorite season or time of year?",
    "What is your favorite sport or sports team?",
    "What is your favorite thing to do on weekends?",
    "What is your favorite memory from childhood?"
  ]
  questions_arr_index = get_arr_associated_index_function(questions_arr)
  return questions_arr, questions_arr_index
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== lists __init__ END ===========================================')
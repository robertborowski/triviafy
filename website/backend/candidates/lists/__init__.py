# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
# ------------------------ imports end ------------------------

localhost_print_function('=========================================== lists __init__ START ===========================================')
# ------------------------ individual function start ------------------------
def get_team_building_activities_list_function():
  activities_list = ['Trivia', 'Picture quizzes', 'Icebreakers', 'Employee surveys', 'Personality tests', 'Colleague birthday trivia', 'Most likely to', 'This or that', 'Watercooler starters', 'Word games', '2 player games', 'Create custom questions']
  # activities_list = sorted(activities_list)
  # ------------------------ get counter start ------------------------
  activities_list_index = []
  total_activities = len(activities_list)
  for i in range(total_activities):
    activities_list_index.append(i)
  # ------------------------ get counter end ------------------------
  return activities_list, activities_list_index
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== lists __init__ END ===========================================')
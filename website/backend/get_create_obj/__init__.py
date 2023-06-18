# ------------------------ imports start ------------------------
from website.models import UserObj, ShowsFollowingObj, PlatformsObj, ShowsObj, PollsObj, PollsAnsweredObj
from website.backend.sql_statements.select import select_general_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_all_shows_following_function(current_user):
  db_shows_following_obj = None
  try:
    db_shows_following_obj = ShowsFollowingObj.query.filter_by(fk_user_id=current_user.id).all()
    if db_shows_following_obj == None or db_shows_following_obj == []:
      return None
  except:
    pass
  return db_shows_following_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_all_platforms_function():
  db_objs = PlatformsObj.query.filter_by(status=True).order_by(PlatformsObj.name.asc()).all()
  if db_objs == None or db_objs == []:
    return None
  return db_objs
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_all_shows_for_platform_function(input_platform_id):
  db_objs = ShowsObj.query.filter_by(fk_platform_id=input_platform_id,status=True).order_by(ShowsObj.name.asc()).all()
  if db_objs == None or db_objs == []:
    return None
  return db_objs
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_show_based_on_name_function(input_platform_id, input_name):
  db_obj = ShowsObj.query.filter_by(fk_platform_id=input_platform_id,name=input_name,status=True).first()
  if db_obj == None or db_obj == []:
    return None
  return db_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_show_based_on_id_and_platform_id_function(input_show_id, input_platform_id):
  db_obj = ShowsObj.query.filter_by(id=input_show_id, fk_platform_id=input_platform_id, status=True).first()
  if db_obj == None or db_obj == []:
    return None
  return db_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_show_based_on_id_function(input_show_id):
  db_obj = ShowsObj.query.filter_by(id=input_show_id).first()
  if db_obj == None or db_obj == []:
    return None
  return db_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_show_percent_of_all_polls_answered_function(fk_user_id, fk_show_id):
  # ------------------------ variables start ------------------------
  user_percent_completed = int(0)
  show_polls_total = int(0)
  show_polls_answered_total = int(0)
  is_complete = False
  # ------------------------ variables end ------------------------
  # ------------------------ show polls total start ------------------------
  db_objs = PollsObj.query.filter_by(fk_show_id=fk_show_id,status_approved=True,status_removed=False).all()
  try:
    show_polls_total = len(db_objs)
  except:
    pass
  # ------------------------ show polls total end ------------------------
  # ------------------------ user answered show polls total start ------------------------
  db_arr_of_dicts = select_general_function('select_query_general_3', fk_show_id, fk_user_id)
  try:
    show_polls_answered_total = len(db_arr_of_dicts)
  except:
    pass
  # ------------------------ user answered show polls total end ------------------------
  # ------------------------ calculation start ------------------------
  try:
    user_percent_completed = float(int(show_polls_answered_total)/int(show_polls_total))
    user_percent_completed = str(int(float(user_percent_completed) * float(100)))
  except:
    pass
  # ------------------------ calculation end ------------------------
  # ------------------------ catch start ------------------------
  if int(user_percent_completed) == int(0):
    user_percent_completed = 1
  # ------------------------ catch end ------------------------
  # ------------------------ complete status start ------------------------
  if int(user_percent_completed) == int(100):
    is_complete = True
  # ------------------------ complete status end ------------------------
  return int(user_percent_completed), is_complete
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_poll_based_on_id_function(input_id):
  db_obj = PollsObj.query.filter_by(id=input_id,status_removed=False).first()
  if db_obj == None or db_obj == []:
    return None
  return db_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def check_if_currently_following_show_function(current_user, input_show_id, input_platform_id):
  db_obj = ShowsFollowingObj.query.filter_by(fk_user_id=current_user.id, fk_show_id=input_show_id, fk_platform_id=input_platform_id).first()
  if db_obj == None or db_obj == []:
    return None
  return db_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_platform_based_on_name_function(input_name):
  db_obj = PlatformsObj.query.filter_by(name=input_name,status=True).first()
  if db_obj == None or db_obj == []:
    return None
  return db_obj
# ------------------------ individual function end ------------------------
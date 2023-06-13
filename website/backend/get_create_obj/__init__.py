# ------------------------ imports start ------------------------
from website.models import UserObj, ShowsFollowingObj, PlatformsObj, ShowsObj
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
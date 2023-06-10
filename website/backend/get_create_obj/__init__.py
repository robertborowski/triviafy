# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website.models import UserObj, SourcesFollowingObj, PlatformsObj
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_all_sources_following_function(current_user):
  db_sources_following_obj = None
  try:
    db_sources_following_obj = SourcesFollowingObj.query.filter_by(fk_user_id=current_user.id).all()
    if db_sources_following_obj == None or db_sources_following_obj == []:
      return None
  except:
    pass
  return db_sources_following_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_all_platforms_function():
  db_objs = PlatformsObj.query.filter_by(status=True).order_by(PlatformsObj.name.asc()).all()
  if db_objs == None or db_objs == []:
    return None
  return db_objs
# ------------------------ individual function end ------------------------
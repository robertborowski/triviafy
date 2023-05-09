# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website.models import GroupObj, UserObj, ActivitySettingsAObj
from website.backend.candidates.autogeneration import generate_random_length_uuid_function
from website import db
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def pull_create_group_id_function(current_user):
  # ------------------------ if team member with group id exists start ------------------------
  db_all_users_obj = UserObj.query.filter_by(company_name=current_user.company_name).all()
  for i_user_obj in db_all_users_obj:
    if i_user_obj.group_id != None and i_user_obj.group_id != '':
      return i_user_obj.group_id
  # ------------------------ if team member with group id exists end ------------------------
  # ------------------------ if no group id exists start ------------------------
  company_group_id = generate_random_length_uuid_function(6)
  # ------------------------ while loop if generated group id already exists start ------------------------
  group_id_exists_check = GroupObj.query.filter_by(public_group_id=company_group_id).first()
  while group_id_exists_check != None:
    company_group_id = generate_random_length_uuid_function(6)
    group_id_exists_check = GroupObj.query.filter_by(public_group_id=company_group_id).first()
  # ------------------------ while loop if generated group id already exists end ------------------------
  # ------------------------ if no group id exists end ------------------------
  return company_group_id
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def pull_create_group_obj_function(current_user):
  db_group_obj = GroupObj.query.filter_by(public_group_id=current_user.group_id).first()
  if db_group_obj == None or db_group_obj == []:
    # ------------------------ insert to db start ------------------------
    try:
      new_row = GroupObj(
        id = create_uuid_function('group_'),
        created_timestamp = create_timestamp_function(),
        fk_company_name = current_user.company_name,
        fk_user_id = current_user.id,
        public_group_id = current_user.group_id,
        status = 'active',
        trivia = True,
        picture_quiz = False,
        birthday_questions = False,
        icebreakers = False,
        surveys = False,
        personality_test = False,
        this_or_that = False,
        most_likely_to = False,
        giftcard = False
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    db_group_obj = GroupObj.query.filter_by(public_group_id=current_user.group_id).first()
    # ------------------------ insert to db end ------------------------
  return db_group_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def pull_create_activity_settings_a_obj_function(current_user, activity_name):
  # ------------------------ pull/create group settings start ------------------------
  db_group_settings_obj = ActivitySettingsAObj.query.filter_by(fk_group_id=current_user.group_id,product=activity_name).first()
  if db_group_settings_obj == None or db_group_settings_obj == []:
    # ------------------------ insert to db start ------------------------
    try:
      new_row = ActivitySettingsAObj(
        id = create_uuid_function('gset_'),
        created_timestamp = create_timestamp_function(),
        fk_group_id = current_user.group_id,
        fk_user_id = current_user.id,
        timezone = 'EST',
        start_day = 'Monday',
        start_time = '12 PM',
        end_day = 'Thursday',
        end_time = '1 PM',
        cadence = 'Weekly',
        total_questions = 10,
        question_type = 'Mixed',
        categories = 'all_categories',
        product = activity_name
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    db_group_settings_obj = ActivitySettingsAObj.query.filter_by(fk_group_id=current_user.group_id,product=activity_name).first()
    # ------------------------ insert to db end ------------------------
  # ------------------------ pull/create group settings end ------------------------
  return db_group_settings_obj
# ------------------------ individual function end ------------------------
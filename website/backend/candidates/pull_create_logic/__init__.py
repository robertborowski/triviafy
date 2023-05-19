# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website.models import GroupObj, UserObj, ActivityASettingsObj, ActivityATestObj, ActivityATestGradedObj
from website.backend.candidates.autogeneration import generate_random_length_uuid_function
from website import db
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_all_users_company_name_function(current_user):
  db_all_users_obj = UserObj.query.filter_by(company_name=current_user.company_name).order_by(UserObj.created_timestamp.desc()).all()
  return db_all_users_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def user_must_have_group_id_function(current_user):
  if current_user.group_id == None or current_user.group_id == '':
    db_all_users_obj = get_all_users_company_name_function(current_user)
    for i_obj in db_all_users_obj:
      if i_obj.group_id != None and i_obj.group_id != '':
        latest_group_id = i_obj.group_id
        current_user.group_id = latest_group_id
        db.session.commit()
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def pull_create_group_id_function(current_user):
  # ------------------------ if team member with group id exists start ------------------------
  db_all_users_obj = get_all_users_company_name_function(current_user)
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
    if current_user.group_id != None and current_user.group_id != '':
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
def pull_group_obj_function(current_user):
  db_group_obj = GroupObj.query.filter_by(public_group_id=current_user.group_id).first()
  return db_group_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def pull_create_activity_a_settings_obj_function(current_user, activity_name):
  # ------------------------ pull/create group settings start ------------------------
  db_group_settings_obj = ActivityASettingsObj.query.filter_by(fk_group_id=current_user.group_id,product=activity_name).first()
  if db_group_settings_obj == None or db_group_settings_obj == []:
    # ------------------------ insert to db start ------------------------
    try:
      new_row = ActivityASettingsObj(
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
    db_group_settings_obj = ActivityASettingsObj.query.filter_by(fk_group_id=current_user.group_id,product=activity_name).first()
    # ------------------------ insert to db end ------------------------
  # ------------------------ pull/create group settings end ------------------------
  return db_group_settings_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def pull_latest_activity_a_test_obj_function(current_user, activity_name):
  db_tests_obj = ActivityATestObj.query.filter_by(fk_group_id=current_user.group_id,product=activity_name).order_by(ActivityATestObj.created_timestamp.desc()).first()
  if db_tests_obj == None or db_tests_obj == []:
    db_tests_obj = None
  return db_tests_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def pull_latest_activity_a_test_graded_obj_function(db_tests_obj, current_user, activity_name):
  db_test_grading_obj = ActivityATestGradedObj.query.filter_by(fk_test_id=db_tests_obj.id, fk_user_id=current_user.id,product=activity_name).first()
  if db_test_grading_obj == None or db_test_grading_obj == []:
    db_test_grading_obj = None
  return db_test_grading_obj
# ------------------------ individual function end ------------------------
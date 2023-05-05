
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website.models import EmployeesGroupsObj
from website.backend.candidates.autogeneration import generate_random_length_uuid_function
from website import db
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== pull_create_logic __init__ start ===========================================')
# ------------------------ individual function start ------------------------
def pull_create_group_obj_function(current_user):
  # ------------------------ pull/create group id start ------------------------
  company_group_id = None
  db_groups_obj = EmployeesGroupsObj.query.filter_by(fk_company_name=current_user.company_name).first()
  if db_groups_obj == None or db_groups_obj == []:
    company_group_id = generate_random_length_uuid_function(6)
    # ------------------------ while loop if generated group id already exists start ------------------------
    group_id_exists_check = EmployeesGroupsObj.query.filter_by(public_group_id=company_group_id).first()
    while group_id_exists_check != None:
      company_group_id = generate_random_length_uuid_function(6)
      group_id_exists_check = EmployeesGroupsObj.query.filter_by(public_group_id=company_group_id).first()
    # ------------------------ while loop if generated group id already exists end ------------------------
    # ------------------------ insert to db start ------------------------
    try:
      new_row = EmployeesGroupsObj(
        id = create_uuid_function('group_'),
        created_timestamp = create_timestamp_function(),
        fk_company_name = current_user.company_name,
        fk_user_id = current_user.id,
        public_group_id = company_group_id,
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
    # ------------------------ insert to db end ------------------------
  else:
    company_group_id = db_groups_obj.public_group_id
  # ------------------------ pull/create group id end ------------------------
  return company_group_id
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== pull_create_logic __init__ end ===========================================')
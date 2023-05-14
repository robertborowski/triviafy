# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from flask_login import login_required, current_user
from website.backend.candidates.autogeneration import question_choices_function
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
from website.backend.candidates.datetime_manipulation import days_times_timezone_arr_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.backend.candidates.string_manipulation import all_employee_question_categories_sorted_function
from website.backend.candidates.string_manipulation import capitalize_all_words_function
from website.backend.candidates.dropdowns import get_activity_a_dropdowns_function
from website.backend.candidates.pull_create_logic import pull_create_activity_a_settings_obj_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def activity_a_settings_prep_function(page_dict, url_activity_code, db_activity_settings_dict):
  # ------------------------ page title start ------------------------
  page_dict['title'] = capitalize_all_words_function(url_activity_code)
  page_dict['title'] = page_dict['title'] + ' Settings'
  # ------------------------ page title end ------------------------
  # ------------------------ get dropdowns start ------------------------
  page_dict['settings_dict'] = db_activity_settings_dict
  page_dict['dropdown_weekdays'], page_dict['dropdown_times'], page_dict['dropdown_timezones'] = days_times_timezone_arr_function()
  page_dict['dropdown_cadence_arr'], page_dict['dropdown_question_num_arr'], page_dict['dropdown_question_type_arr'] = question_choices_function()
  page_dict['dropdowns_dict'] = get_activity_a_dropdowns_function()
  # ------------------------ get dropdowns end ------------------------
  # ------------------------ get all categories start ------------------------
  query_result_arr_of_dicts = select_general_function('select_all_employees_categories_v1')
  page_dict['all_categories_arr'] = all_employee_question_categories_sorted_function(query_result_arr_of_dicts)
  # ------------------------ get all categories end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------
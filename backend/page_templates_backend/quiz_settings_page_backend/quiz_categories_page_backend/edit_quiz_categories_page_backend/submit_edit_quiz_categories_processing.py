# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.quiz_categories_utils.edit_quiz_categories_validate_user_inputs import edit_quiz_categories_validate_user_inputs_function
from backend.db.queries.update_queries.update_queries_triviafy_categories_selected_table.update_edit_quiz_categories import update_edit_quiz_categories_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function
from backend.db.queries.update_queries.update_queries_triviafy_categories_selected_table.update_account_categories_looked_at_complete import update_account_categories_looked_at_complete_function
from backend.utils.cached_login.create_nested_dict_from_uuid import create_nested_dict_from_uuid_function

# -------------------------------------------------------------- App Setup
submit_edit_quiz_categories_processing = Blueprint("submit_edit_quiz_categories_processing", __name__, static_folder="static", template_folder="templates")
@submit_edit_quiz_categories_processing.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@submit_edit_quiz_categories_processing.route("/categories/edit/processing", methods=['GET','POST'])
def submit_edit_quiz_categories_processing_function():
  localhost_print_function('=========================================== /categories/edit/processing Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/categories/edit/processing')
    # Redirects based on returned value - pre load checks
    if user_nested_dict == '/employees/subscription':
      return redirect('/employees/subscription', code=302)
    elif user_nested_dict == '/notifications/email/permission':
      return redirect('/notifications/email/permission', code=302)
    elif user_nested_dict == '/new/user/questionnaire':
      return redirect('/new/user/questionnaire', code=302)
    elif user_nested_dict == '/categories/edit':
      return redirect('/categories/edit', code=302)
    elif user_nested_dict == '/employees/logout':
      return redirect('/employees/logout', code=302)
    # ------------------------ Pre Load Page Checks END ------------------------

    # ------------------------ Page Company Info START ------------------------
    user_company_name = user_nested_dict['user_company_name']
    user_company_name = sanitize_page_output_company_name_function(user_company_name)
    user_channel_name = user_nested_dict['user_slack_channel_name']
    # ------------------------ Page Company Info END ------------------------
    
    # Get additional variables
    slack_workspace_team_id = user_nested_dict['user_slack_workspace_team_id']
    slack_channel_id = user_nested_dict['user_slack_channel_id']
    
    
    # ------------------------ Connect to Postgres DB START ------------------------
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()
    # ------------------------ Connect to Postgres DB END ------------------------


    # ------------------------ Update db for new user onboarding START ------------------------
    user_uuid = user_nested_dict['user_uuid']
    output_message = update_account_categories_looked_at_complete_function(postgres_connection, postgres_cursor, user_uuid)
    user_nested_dict = create_nested_dict_from_uuid_function(user_uuid)
    # ------------------------ Update db for new user onboarding END ------------------------


    # ------------------------ Get User Form Checkbox Values START ------------------------
    # Select All Category Check
    user_form_categories_selected_select_all_checkbox = request.form.get('select_all_category_checkbox_name')
    if user_form_categories_selected_select_all_checkbox != None and user_form_categories_selected_select_all_checkbox != 'select_all_categories':
      localhost_print_function('=========================================== /categories/edit/processing Page END ===========================================')
      return redirect('/dashboard', code=302)

    # Categories that are not Select All or Deselect All
    user_form_categories_selected_arr = request.form.getlist('category_checkbox_name')
    validate_user_form_categories_selected_arr = edit_quiz_categories_validate_user_inputs_function(user_form_categories_selected_arr)
    if validate_user_form_categories_selected_arr == False:
      localhost_print_function('=========================================== /categories/edit/processing Page END ===========================================')
      return redirect('/dashboard', code=302)
    # ------------------------ Get User Form Checkbox Values END ------------------------
    
    
    # ------------------------ Logic Selected Pre DB Update START ------------------------
    categories_to_push_to_db_str = ''
    caps_exceptions_set = {'sql', 'tv', 'uk'}
    
    # If other categories were checked
    if user_form_categories_selected_select_all_checkbox == None:
      if len(user_form_categories_selected_arr) >= 1:
        categories_to_push_to_db_arr = []
        for i_category in user_form_categories_selected_arr:
          i_category_with_space = i_category.replace('_',' ')
          if i_category_with_space in caps_exceptions_set:
            i_category_with_caps = i_category_with_space.upper()
            categories_to_push_to_db_arr.append(i_category_with_caps)
          else:
            i_category_with_title = i_category_with_space.title()
            categories_to_push_to_db_arr.append(i_category_with_title)
          categories_to_push_to_db_arr = sorted(categories_to_push_to_db_arr)
          categories_to_push_to_db_str = ",".join(categories_to_push_to_db_arr)

    # If select all was checked
    if user_form_categories_selected_select_all_checkbox == 'select_all_categories':
      categories_to_push_to_db_str = 'All Categories'
    # ------------------------ Logic Selected Pre DB Update END ------------------------

    
    # ------------------------ Update DB New Categories START ------------------------
    if categories_to_push_to_db_str != None and categories_to_push_to_db_str != '':
      output_message = update_edit_quiz_categories_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id, categories_to_push_to_db_str)
    # ------------------------ Update DB New Categories END ------------------------
    

    # ------------------------ Close Postgres DB START ------------------------
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Close Postgres DB END ------------------------
    
  except:
    localhost_print_function('page load except error hit - /categories/edit/processing Page')
    localhost_print_function('=========================================== /categories/edit/processing Page END ===========================================')
    return redirect('/employees/logout', code=302)
    # return redirect('/', code=302)

  
  localhost_print_function('=========================================== /categories/edit/processing Page END ===========================================')
  return redirect('/dashboard', code=302)
# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_categories_selected_table.select_current_categories_team_channel_combo import select_current_categories_team_channel_combo_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
quiz_categories_index_page_render_template = Blueprint("quiz_categories_index_page_render_template", __name__, static_folder="static", template_folder="templates")
@quiz_categories_index_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@quiz_categories_index_page_render_template.route("/categories", methods=['GET','POST'])
def quiz_categories_index_page_render_template_function():
  localhost_print_function('=========================================== /categories Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/categories')
    # Redirects based on returned value - pre load checks
    if user_nested_dict == '/subscription':
      return redirect('/subscription', code=302)
    elif user_nested_dict == '/notifications/email/permission':
      return redirect('/notifications/email/permission', code=302)
    elif user_nested_dict == '/new/user/questionnaire':
      return redirect('/new/user/questionnaire', code=302)
    elif user_nested_dict == '/categories/edit':
      return redirect('/categories/edit', code=302)
    elif user_nested_dict == '/logout':
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

    
    # ------------------------ Select/Pull All Current Categories START ------------------------
    company_current_categories_str = select_current_categories_team_channel_combo_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)
    company_current_categories_arr = company_current_categories_str.split(',')
    # ------------------------ Select/Pull All Current Categories END ------------------------


    # ------------------------ Close Postgres DB START ------------------------
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Close Postgres DB END ------------------------
    
  except:
    localhost_print_function('page load except error hit - /categories Page')
    localhost_print_function('=========================================== /categories Page END ===========================================')
    return redirect('/employees/logout', code=302)
    # return redirect('/', code=302)

  
  localhost_print_function('=========================================== /categories Page END ===========================================')
  return render_template('employee_engagement_page_templates/quiz_settings_page_templates/quiz_categories_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          free_trial_ends_info_to_html = free_trial_ends_info,
                          company_current_categories_arr_to_html = company_current_categories_arr,
                          page_title_to_html = 'Quiz Categories')
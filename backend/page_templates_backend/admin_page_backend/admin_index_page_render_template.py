# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
import os
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_slack_all_team_channel_combos_with_names_count import select_triviafy_user_login_information_table_slack_all_team_channel_combos_with_names_count_function
from backend.page_templates_backend.admin_page_backend.admin_supporting_backend.admin_supporting_remaining_category_count import admin_supporting_remaining_category_count_function
from backend.page_templates_backend.admin_page_backend.admin_supporting_backend.admin_supporting_winner_counts import admin_supporting_winner_counts_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_new_emails_for_dist_list import select_triviafy_user_login_information_table_new_emails_for_dist_list_function
from backend.db.queries.select_queries.select_queries_triviafy_user_login_information_table_slack.select_triviafy_user_login_information_table_new_sign_ups import select_triviafy_user_login_information_table_new_sign_ups_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
admin_index_page_render_template = Blueprint("admin_index_page_render_template", __name__, static_folder="static", template_folder="templates")
@admin_index_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@admin_index_page_render_template.route("/admin", methods=['GET','POST'])
def admin_index_page_render_template_function():
  localhost_print_function('=========================================== /admin Page START ===========================================')
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/admin')
    # Redirects based on returned value - pre load checks
    if user_nested_dict == '/subscription':
      return redirect('/subscription', code=302)
    elif user_nested_dict == '/notifications/email/permission':
      return redirect('/notifications/email/permission', code=302)
    elif user_nested_dict == '/new/user/questionnaire':
      return redirect('/new/user/questionnaire', code=302)
    elif user_nested_dict == '/logout':
      return redirect('/logout', code=302)
    # ------------------------ Pre Load Page Checks END ------------------------

    
    # ------------------------ Page Company Info START ------------------------
    user_company_name = user_nested_dict['user_company_name']
    user_company_name = sanitize_page_output_company_name_function(user_company_name)
    user_channel_name = user_nested_dict['slack_channel_name']
    # ------------------------ Page Company Info END ------------------------
    
    # Get additional variables
    user_email = user_nested_dict['user_email']

  except:
    localhost_print_function('page load except error hit - /admin Page')
    localhost_print_function('=========================================== /admin Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)
  

  # ------------------------ Check create question accesss START ------------------------
  # Get personal email
  personal_email = os.environ.get('PERSONAL_EMAIL')

  # If user does not have access to create questions then redirect to waitlist page
  if user_email != personal_email:
    localhost_print_function('redirecting to the index page!')
    localhost_print_function('=========================================== /admin Page END ===========================================')
    return redirect('/', code=302)
  # ------------------------ Check create question accesss END ------------------------


  # ------------------------ Connect to Postgres DB START ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ Connect to Postgres DB END ------------------------


  # ------------------------ New Sign Ups and New Emails START ------------------------
  new_emails_for_dist_list_int = select_triviafy_user_login_information_table_new_emails_for_dist_list_function(postgres_connection, postgres_cursor)
  new_sign_ups_int = select_triviafy_user_login_information_table_new_sign_ups_function(postgres_connection, postgres_cursor)
  # ------------------------ New Sign Ups and New Emails END ------------------------


  # ------------------------ Pull All Team Channel Combos START ------------------------
  all_team_channel_combos_arr = select_triviafy_user_login_information_table_slack_all_team_channel_combos_with_names_count_function(postgres_connection, postgres_cursor)
  # ------------------------ Pull All Team Channel Combos END ------------------------


  # ------------------------ Loop Through Each Team Channel Combo START ------------------------
  # Make the master arr of dicts before looping
  master_all_companies_remainder_arr_of_dicts = []
  master_all_companies_winner_counts_arr_of_dicts = []

  for i in all_team_channel_combos_arr:
    # declare variables
    pulled_team_id = i[0]       # str
    pulled_channel_id = i[1]    # str
    pulled_team_name = i[2]     # str
    pulled_channel_name = i[3]  # str
    pulled_user_count = i[4]    # int
    

    # Category remaining questions
    master_all_companies_remainder_arr_of_dicts = admin_supporting_remaining_category_count_function(postgres_connection, postgres_cursor, pulled_team_id, pulled_channel_id, pulled_team_name, pulled_channel_name, pulled_user_count, master_all_companies_remainder_arr_of_dicts)

    # Count users, count wins, count wins per user
    master_all_companies_winner_counts_arr_of_dicts = admin_supporting_winner_counts_function(postgres_connection, postgres_cursor, pulled_team_id, pulled_channel_id, pulled_team_name, pulled_channel_name, pulled_user_count, master_all_companies_winner_counts_arr_of_dicts)

  # ------------------------ Loop Through Each Team Channel Combo END ------------------------


  # ------------------------ Close Postgres DB START ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Close Postgres DB END ------------------------

  
  localhost_print_function('=========================================== /admin Page END ===========================================')
  return render_template('admin_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          new_emails_for_dist_list_int_to_html = new_emails_for_dist_list_int,
                          new_sign_ups_int_to_html = new_sign_ups_int,
                          master_all_companies_remainder_arr_of_dicts_to_html = master_all_companies_remainder_arr_of_dicts,
                          master_all_companies_winner_counts_arr_of_dicts_to_html = master_all_companies_winner_counts_arr_of_dicts,
                          page_title_to_html = 'Admin')
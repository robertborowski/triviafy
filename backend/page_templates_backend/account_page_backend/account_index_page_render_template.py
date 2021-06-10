# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.cached_login.check_if_user_login_through_cookies import check_if_user_login_through_cookies_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.select_triviafy_user_login_information_table_slack_all_payment_admins import select_triviafy_user_login_information_table_slack_all_payment_admins_function
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.db.queries.select_queries.select_triviafy_user_login_information_table_slack_all_company_user_uuids import select_triviafy_user_login_information_table_slack_all_company_user_uuids_function

# -------------------------------------------------------------- App Setup
account_index_page_render_template = Blueprint("account_index_page_render_template", __name__, static_folder="static", template_folder="templates")
@account_index_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@account_index_page_render_template.route("/account", methods=['GET','POST'])
def account_index_page_render_template_function():
  print('=========================================== /account Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------

  try:
    user_nested_dict = check_if_user_login_through_cookies_function()

    # Get user information from the nested dict
    user_company_name = user_nested_dict['user_company_name']
    user_channel_name = user_nested_dict['slack_channel_name']
    user_first_name = user_nested_dict['user_first_name']
    user_last_name = user_nested_dict['user_last_name']
    slack_workspace_team_id = user_nested_dict['slack_team_id']
    slack_channel_id = user_nested_dict['slack_channel_id']


    # ------------------------ Get All User Payment Admins START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()
    # Get all user payment admins from DB for company
    company_all_payment_admins_arr_raw = select_triviafy_user_login_information_table_slack_all_payment_admins_function(postgres_connection, postgres_cursor, slack_workspace_team_id, slack_channel_id)
    company_all_payment_admins_arr = []
    for user in company_all_payment_admins_arr_raw:
      # All Payment Admins - present on html page
      company_all_payment_admins_arr.append(user[0].replace("_"," "))

    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Get All User Payment Admins END ------------------------

  except:
    print('=========================================== /account Page END ===========================================')
    return redirect('/', code=302)
  
  print('=========================================== /account Page END ===========================================')
  return render_template('account_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          user_first_name_to_html = user_first_name,
                          user_last_name_to_html = user_last_name,
                          company_all_payment_admins_arr_to_html = company_all_payment_admins_arr)
# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
import os
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
admin_leaderboard_index_page_render_template = Blueprint("admin_leaderboard_index_page_render_template", __name__, static_folder="static", template_folder="templates")
@admin_leaderboard_index_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@admin_leaderboard_index_page_render_template.route("/employees/admin/leaderboard", methods=['GET','POST'])
def admin_leaderboard_index_page_render_template_function():
  localhost_print_function('=========================================== /employees/admin/leaderboard Page START ===========================================')
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/employees/admin/leaderboard')
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
    user_email = user_nested_dict['user_email']

  except:
    localhost_print_function('page load except error hit - /employees/admin/leaderboard Page')
    localhost_print_function('=========================================== /employees/admin/leaderboard Page END ===========================================')
    return redirect('/employees/logout', code=302)
    # return redirect('/', code=302)
  

  # ------------------------ Check create question accesss START ------------------------
  # Get personal email
  personal_email = os.environ.get('PERSONAL_EMAIL')

  # If user does not have access to create questions then redirect to waitlist page
  if user_email != personal_email:
    localhost_print_function('redirecting to the index page!')
    localhost_print_function('=========================================== /employees/admin/leaderboard Page END ===========================================')
    return redirect('/', code=302)
  # ------------------------ Check create question accesss END ------------------------

  
  localhost_print_function('=========================================== /employees/admin/leaderboard Page END ===========================================')
  return render_template('employee_engagement_page_templates/admin_page_templates/index_leaderboard.html',
                          css_cache_busting = cache_busting_output,
                          page_title_to_html = 'Leaderboard')
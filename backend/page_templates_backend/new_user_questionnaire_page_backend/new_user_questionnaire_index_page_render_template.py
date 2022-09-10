# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.sanitize_page_outputs.sanitize_page_output_company_name import sanitize_page_output_company_name_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
new_user_questionnaire_index_page_render_template = Blueprint("new_user_questionnaire_index_page_render_template", __name__, static_folder="static", template_folder="templates")
@new_user_questionnaire_index_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@new_user_questionnaire_index_page_render_template.route("/new/user/questionnaire", methods=['GET','POST'])
def new_user_questionnaire_index_page_render_template_function():
  localhost_print_function('=========================================== /new/user/questionnaire Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/new/user/questionnaire')
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
      return redirect('/logout', code=302)
    # ------------------------ Pre Load Page Checks END ------------------------


    # ------------------------ Page Pre Load Check - Redirect Check - New User Questionnaire Answered START ------------------------
    user_slack_new_user_questionnaire_answered = user_nested_dict['user_slack_new_user_questionnaire_answered']
    if user_slack_new_user_questionnaire_answered == True or user_slack_new_user_questionnaire_answered == 'True':
      return redirect('/dashboard', code=302)
    # ------------------------ Page Pre Load Check - Redirect Check - New User Questionnaire Answered END ------------------------


    # ------------------------ Page Company Info START ------------------------
    user_company_name = user_nested_dict['user_company_name']
    user_company_name = sanitize_page_output_company_name_function(user_company_name)
    user_channel_name = user_nested_dict['user_slack_channel_name']
    # ------------------------ Page Company Info END ------------------------

    user_full_name = user_nested_dict['user_display_name']

    
  except:
    localhost_print_function('page load except error hit - /new/user/questionnaire Page')
    localhost_print_function('=========================================== /new/user/questionnaire Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)

  
  localhost_print_function('=========================================== /new/user/questionnaire Page END ===========================================')
  return render_template('employee_engagement_page_templates/new_user_questionnaire_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          free_trial_ends_info_to_html = free_trial_ends_info,
                          user_full_name_to_html = user_full_name,
                          page_title_to_html = 'New User Questionnaire')
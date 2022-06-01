# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.pre_load_page_checks_utils.pre_load_page_checks import pre_load_page_checks_function

# -------------------------------------------------------------- App Setup
create_question_rate_limit_page_render_template = Blueprint("create_question_rate_limit_page_render_template", __name__, static_folder="static", template_folder="templates")
@create_question_rate_limit_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@create_question_rate_limit_page_render_template.route("/create/question/limit", methods=['GET','POST'])
def create_question_rate_limit_page_render_template_function():
  localhost_print_function('=========================================== /create/question/limit Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Pre Load Page Checks START ------------------------
    user_nested_dict, free_trial_ends_info = pre_load_page_checks_function('/create/question/limit')
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


    user_email = user_nested_dict['user_email']
    user_uuid = user_nested_dict['user_uuid']
    
    # This is a variable in TWO .py files
    limit_amount = 50

  except:
    localhost_print_function('page load except error hit - /create/question/limit Page')
    localhost_print_function('=========================================== /create/question/limit Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)

  
  localhost_print_function('=========================================== /create/question/limit Page END ===========================================')
  return render_template('create_question_page_templates/create_question_rate_limit_page_templates/index.html',
                          css_cache_busting = cache_busting_output,
                          user_email_html = user_email,
                          free_trial_ends_info_to_html = free_trial_ends_info,
                          limit_amount_to_html = limit_amount)
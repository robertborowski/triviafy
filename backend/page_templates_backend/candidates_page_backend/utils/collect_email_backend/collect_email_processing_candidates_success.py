# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- App Setup
collect_email_processing_candidates_success = Blueprint("collect_email_processing_candidates_success", __name__, static_folder="static", template_folder="templates")
@collect_email_processing_candidates_success.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@collect_email_processing_candidates_success.route("/candidates/email/success", methods=['GET','POST'])
def collect_email_processing_candidates_success_function():
  localhost_print_function('=========================================== /candidates/email/success Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------

  localhost_print_function('=========================================== /candidates/email/success Page END ===========================================')
  return render_template('employee_engagement_page_templates/candidates_page_templates/collect_email_page_templates/index.html', css_cache_busting = cache_busting_output)
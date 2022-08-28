# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- App Setup
login_page_render_template = Blueprint("login_page_render_template", __name__, static_folder="static", template_folder="templates")
@login_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@login_page_render_template.route("/candidates/login", methods=['GET','POST'])
def login_page_render_template_function():
  localhost_print_function('=========================================== /candidates/login Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------

  localhost_print_function('=========================================== /candidates/login Page END ===========================================')
  return render_template('candidates_page_templates/login_page_templates/index.html', css_cache_busting = cache_busting_output)
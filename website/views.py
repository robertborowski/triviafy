# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -Note: any pages related to authentication will not be in this file, they will be routed in the auth.py file.
# ------------------------ info about this file end ------------------------


# ------------------------ imports start ------------------------
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from flask import Blueprint, render_template
from flask_login import login_required, current_user
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
views = Blueprint('views', __name__)
# ------------------------ function end ------------------------

# ------------------------ before page variables start ------------------------
cache_busting_output = create_uuid_function('css_')
# ------------------------ before page variables end ------------------------

# ------------------------ routes start ------------------------
# ------------------------ individual route - aaaa youtube start ------------------------
@views.route('/')
@login_required   # this decorator says that url cannot be accessed unless the user is logged in.
def home_function():
  return render_template('home.html', user=current_user)
# ------------------------ individual route - aaaa youtube end ------------------------
# ------------------------ individual route - candidates about start ------------------------
@views.route('/candidates/about')
def candidates_about_page_function():
  return render_template('candidates_page_templates/about_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates about end ------------------------
# ------------------------ individual route - candidates collect email start ------------------------
@views.route('/candidates/email')
def candidates_email_page_function():
  return render_template('candidates_page_templates/collect_email_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates collect email end ------------------------
# ------------------------ individual route - candidates faq start ------------------------
@views.route('/candidates/faq')
def candidates_faq_page_function():
  return render_template('candidates_page_templates/faq_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates faq end ------------------------
# ------------------------ individual route - candidates index main start ------------------------
@views.route('/candidates')
def landing_index_page_function():
  return render_template('candidates_page_templates/index_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates index main end ------------------------
# ------------------------ individual route - candidates pricing start ------------------------
@views.route('/candidates/pricing')
def candidates_pricing_page_function():
  return render_template('candidates_page_templates/pricing_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates pricing end ------------------------
# ------------------------ individual route - candidates stand in start ------------------------
@views.route('/candidates/launch')
def candidates_stand_in_page_function():
  return render_template('candidates_page_templates/stand_in_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates stand in end ------------------------
# ------------------------ individual route - candidates test library start ------------------------
@views.route('/candidates/library')
def candidates_test_library_page_function():
  return render_template('candidates_page_templates/test_library_page_templates/index.html', user=current_user)
# ------------------------ individual route - candidates test library end ------------------------
# ------------------------ individual route - error 404 start ------------------------
@views.route('/404')
def error_page_function():
  return render_template('error_404_page_templates/index.html', user=current_user)
# ------------------------ individual route - error 404 end ------------------------
# ------------------------ individual route - privacy start ------------------------
@views.route('/privacy')
def privacy_page_function():
  return render_template('privacy_policy_page_templates/index.html', user=current_user)
# ------------------------ individual route - privacy end ------------------------
# ------------------------ individual route - privacy start ------------------------
@views.route('/tos')
def terms_of_service_page_function():
  return render_template('terms_of_service_page_templates/index.html', user=current_user)
# ------------------------ individual route - privacy end ------------------------
# ------------------------ routes end ------------------------
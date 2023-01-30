# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -Note: any pages related to authentication will not be in this file, they will be routed in the auth.py file.
# -@login_required   # this decorator says that url cannot be accessed unless the user is logged in. 
# -@login_required: <-- This decorator will bring a user to __init__ code: [login_manager.login_view = 'auth.candidates_login_page_function'] if they hit a page that requires login and they are not logged in.
# -use code: <methods=['GET', 'POST']> when you want the user to interact with the page through forms/checkbox/textbox/radio/etc.
# ------------------------ info about this file end ------------------------

# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from flask import Blueprint, render_template
from flask_login import current_user
from website.backend.candidates.redis import redis_connect_to_database_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
employees_views_exterior = Blueprint('employees_views_exterior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees')
@employees_views_exterior.route('/employees/')
def landing_page_function():
  localhost_print_function(' ------------------------ landing_page_function START ------------------------ ')
  localhost_print_function(' ------------------------ landing_page_function END ------------------------ ')
  return render_template('employees/exterior/landing/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees/about')
@employees_views_exterior.route('/employees/about/')
def employees_about_function():
  localhost_print_function(' ------------------------ employees_about_function START ------------------------ ')
  localhost_print_function(' ------------------------ employees_about_function END ------------------------ ')
  return render_template('employees/exterior/about/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees/faq')
@employees_views_exterior.route('/employees/faq/')
def employees_faq_function():
  localhost_print_function(' ------------------------ employees_faq_function start ------------------------ ')
  localhost_print_function(' ------------------------ employees_faq_function end ------------------------ ')
  return render_template('employees/exterior/faq/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@employees_views_exterior.route('/employees/pricing')
@employees_views_exterior.route('/employees/pricing/')
def employees_pricing_function():
  localhost_print_function(' ------------------------ employees_pricing_function start ------------------------ ')
  localhost_print_function(' ------------------------ employees_pricing_function end ------------------------ ')
  return render_template('employees/exterior/pricing/index.html')
# ------------------------ individual route end ------------------------
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
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from website import db
from website.backend.candidates.user_inputs import alert_message_default_function_v2
from website.models import EmployeesGroupsObj, EmployeesGroupSettingsObj, EmployeesTestsObj, EmployeesDesiredCategoriesObj, CreatedQuestionsObj, EmployeesTestsGradedObj, UserObj, EmployeesCapacityOptionsObj, EmployeesEmailSentObj, StripeCheckoutSessionObj
import os
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
admin_views_interior = Blueprint('admin_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@admin_views_interior.route('/admin', methods=['GET', 'POST'])
@admin_views_interior.route('/admin/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def admin_dashboard_page_function(url_redirect_code=None):
  localhost_print_function(' ------------------------ admin_dashboard_page_function start ------------------------ ')
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ ensure correct email start ------------------------
  if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
    return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e9'))
  # ------------------------ ensure correct email end ------------------------
  if request.method == 'POST':
    # ------------------------ ensure correct email on post to be safe start ------------------------
    try:
      if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
        return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e9'))
    except:
      return redirect(url_for('employees_views_interior.login_dashboard_page_function', url_redirect_code='e9'))
    # ------------------------ ensure correct email on post to be safe end ------------------------
    # ------------------------ DeleteOneUserAllEmployeesTable start ------------------------
    email_to_delete = request.form.get('DeleteOneUserAllEmployeesTables')
    if email_to_delete != None:
      localhost_print_function(' ------------- 0 ------------- ')
      localhost_print_function(f'USER email_to_delete | type: {type(email_to_delete)} | {email_to_delete}')
      localhost_print_function(' ------------- 0 ------------- ')
    # ------------------------ DeleteOneUserAllEmployeesTable end ------------------------
    pass
  localhost_print_function(' ------------------------ admin_dashboard_page_function end ------------------------ ')
  return render_template('admin_page/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------
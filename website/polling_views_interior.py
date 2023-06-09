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
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from website import db
from website.backend.candidates.user_inputs import alert_message_default_function_v2
from website.backend.candidates.browser import browser_response_set_cookie_function_v6
from website.models import GroupObj, ActivityASettingsObj, ActivityATestObj, UserDesiredCategoriesObj, ActivityACreatedQuestionsObj, ActivityATestGradedObj, UserObj, StripePaymentOptionsObj, EmailSentObj, StripeCheckoutSessionObj, ActivityAGroupQuestionsUsedObj, UserFeatureRequestObj, UserSignupFeedbackObj, UserCelebrateObj, ActivityBCreatedQuestionsObj, ActivityBGroupQuestionsUsedObj, ActivityBTestGradedObj, ActivityBTestObj
from website.backend.candidates.autogeneration import question_choices_function
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function, categories_tuple_function
from website.backend.candidates.datetime_manipulation import days_times_timezone_arr_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.backend.candidates.string_manipulation import all_employee_question_categories_sorted_function
from website.backend.candidates.user_inputs import sanitize_char_count_1_function, sanitize_create_question_options_function, sanitize_create_question_categories_function, sanitize_create_question_question_function, sanitize_create_question_option_e_function, sanitize_create_question_answer_function, get_special_characters_function
from website.backend.candidates.send_emails import send_email_template_function
import os
from website.backend.candidates.quiz import grade_quiz_function, pull_question_function, create_activity_function, compare_candence_vs_previous_quiz_function_v2
import json
from datetime import datetime
from website.backend.candidates.stripe import check_stripe_subscription_status_function_v2, convert_current_period_end_function
import stripe
from website.backend.candidates.datatype_conversion_manipulation import one_col_dict_to_arr_function
from website.backend.candidates.test_backend import get_test_winner
from website.backend.candidates.aws_manipulation import candidates_change_uploaded_image_filename_function, candidates_user_upload_image_checks_aws_s3_function
from website.backend.candidates.string_manipulation import breakup_email_function, capitalize_all_words_function
from website.backend.candidates.lists import get_team_building_activities_list_function, get_month_days_years_function, get_favorite_questions_function, get_marketing_list_function, get_dashboard_accordian_function, get_activity_a_products_function, get_activity_b_products_function
from website.backend.candidates.pull_create_logic import pull_create_group_obj_function, pull_latest_activity_test_obj_function, user_must_have_group_id_function, pull_create_activity_settings_obj_function, pull_group_obj_function, get_total_activity_closed_count_function
from website.backend.candidates.activity_supporting import activity_dashboard_function, activity_live_function, turn_activity_auto_on_function, dashboard_celebrations_function, get_all_teammate_ids_function
from website.backend.candidates.emailing import email_share_with_team_function
from website.backend.candidates.onboarding import onboarding_checks_function
from website.backend.candidates.settings_supporting import activity_settings_prep_function, activity_settings_post_function
from website.backend.login_checks import product_login_checks_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
polling_views_interior = Blueprint('polling_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/polling/dashboard', methods=['GET', 'POST'])
@polling_views_interior.route('/polling/dashboard/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def polling_dashboard_function(url_redirect_code=None):
  # ------------------------ product login check start ------------------------
  is_match = product_login_checks_function(current_user,'polling')
  if is_match == False:
    logout_user()
    localhost_print_function('user logged out and redirecting to landing page of product')
    return redirect(url_for('polling_views_exterior.polling_landing_function'))
  # ------------------------ product login check end ------------------------
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'polling/interior/dashboard/index.html'
  # ------------------------ for setting cookie end ------------------------
  localhost_print_function(' ------------- 100-dashboard start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-dashboard end ------------- ')
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, page_dict_to_html=page_dict)
  else:
    browser_response = browser_response_set_cookie_function_v6(current_user, template_location_url, page_dict)
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------
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
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user, login_user
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from website.models import CandidatesUserObj, CandidatesDesiredLanguagesObj, CandidatesUploadedCandidatesObj, CandidatesAssessmentsCreatedObj, CandidatesRequestLanguageObj, CandidatesScheduleObj, CandidatesEmailSentObj, CandidatesAssessmentGradedObj, CandidatesCapacityOptionsObj, CandidatesStripeCheckoutSessionObj, CandidatesCreatedQuestionsObj
from website.backend.candidates.browser import browser_response_set_cookie_function, browser_response_set_cookie_function_v2
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.backend.candidates.datatype_conversion_manipulation import one_col_dict_to_arr_function
from website import db
from website.backend.candidates.user_inputs import sanitize_email_function, sanitize_password_function, sanitize_create_account_text_inputs_function, sanitize_create_account_text_inputs_large_function, validate_upload_candidate_function, sanitize_loop_check_if_exists_within_arr_function, sanitize_check_if_str_exists_within_arr_function, check_if_question_id_arr_exists_function, sanitize_candidate_ui_answer_text_function, sanitize_candidate_ui_answer_radio_function, sanitize_create_question_categories_function, sanitize_create_question_question_function, sanitize_create_question_options_function, sanitize_create_question_answer_function, sanitize_create_question_difficulty_function, sanitize_create_question_option_e_function, sanitize_desired_langs_text_inputs_function
from website.backend.candidates.send_emails import send_email_template_function
from werkzeug.security import generate_password_hash
import pandas as pd
from website.backend.candidates.string_manipulation import all_question_candidate_categories_sorted_function, create_assessment_name_function
from website.backend.candidates.sqlalchemy_manipulation import pull_desired_languages_arr_function
from website.backend.candidates.dict_manipulation import question_arr_of_dicts_manipulations_function, create_assessment_info_dict_function, map_user_answers_to_questions_dict_function, backend_store_question_answers_dict_function, grade_assessment_answers_dict_function, check_two_phrase_similarity_score_function
from website.backend.candidates.datetime_manipulation import next_x_days_function, times_arr_function, expired_assessment_check_function
import datetime
import json
import stripe
import os
from website.backend.candidates.aws_manipulation import candidates_change_uploaded_image_filename_function, candidates_user_upload_image_checks_aws_s3_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
views_exterior = Blueprint('views_exterior', __name__)
# ------------------------ function end ------------------------
# ------------------------ before page variables start ------------------------
cache_busting_output = create_uuid_function('css_')
# ------------------------ before page variables end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ routes not logged in start ------------------------
# ------------------------ individual route start ------------------------
@views_exterior.route('/')
def landing_index_page_function():
  localhost_print_function('=========================================== landing_index_page_function START ===========================================')
  localhost_print_function('=========================================== landing_index_page_function END ===========================================')
  return render_template('candidates/exterior/landing/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/candidates/about')
def candidates_about_page_function():
  localhost_print_function('=========================================== candidates_about_page_function START ===========================================')  
  localhost_print_function('=========================================== candidates_about_page_function END ===========================================')
  return render_template('candidates/exterior/about/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/candidates/faq')
def candidates_faq_page_function():
  localhost_print_function('=========================================== candidates_faq_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_faq_page_function END ===========================================')
  return render_template('candidates/exterior/faq/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/candidates')
def landing_index_page_function_archive_v01():
  localhost_print_function('=========================================== landing_index_page_function_archive_v01 START ===========================================')
  localhost_print_function('=========================================== landing_index_page_function_archive_v01 END ===========================================')
  return render_template('candidates/exterior/landing/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/candidates/library')
def candidates_test_library_page_function():
  localhost_print_function('=========================================== candidates_test_library_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_test_library_page_function END ===========================================')
  return render_template('candidates/exterior/test_library/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/candidates/pricing')
def candidates_pricing_page_function():
  localhost_print_function('=========================================== candidates_pricing_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_pricing_page_function END ===========================================')
  return render_template('candidates/exterior/pricing/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/candidates/email')
def candidates_email_page_function():
  localhost_print_function('=========================================== candidates_email_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_email_page_function END ===========================================')
  return render_template('candidates/exterior/collect_email_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/404')
def error_page_function():
  localhost_print_function('=========================================== error_page_function START ===========================================')
  localhost_print_function('=========================================== error_page_function END ===========================================')
  return render_template('candidates/exterior/error_404/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/privacy')
def privacy_page_function():
  localhost_print_function('=========================================== privacy_page_function START ===========================================')
  localhost_print_function('=========================================== privacy_page_function END ===========================================')
  return render_template('candidates/exterior/privacy_policy_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/tos')
def terms_of_service_page_function():
  localhost_print_function('=========================================== terms_of_service_page_function START ===========================================')
  localhost_print_function('=========================================== terms_of_service_page_function END ===========================================')
  return render_template('candidates/exterior/terms_of_service_page_templates/index.html', user=current_user)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/candidates/reset', methods=['GET', 'POST'])
def candidates_forgot_password_page_function():
  localhost_print_function('=========================================== candidates_forgot_password_page_function START ===========================================')  
  forgot_password_error_statement = ''
  if request.method == 'POST':
    # ------------------------ post request sent start ------------------------
    ui_email = request.form.get('forgot_password_page_ui_email')
    # ------------------------ post request sent end ------------------------
    # ------------------------ sanitize/check user input email start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email)
    if ui_email_cleaned == False:
      forgot_password_error_statement = 'Please enter a valid work email.'
    # ------------------------ sanitize/check user input email end ------------------------
    # ------------------------ check if user email exists in db start ------------------------
    user_exists = CandidatesUserObj.query.filter_by(email=ui_email).first()
    if user_exists:
      forgot_password_error_statement = 'Password reset link sent to email.'
      # ------------------------ send email with token url start ------------------------
      serializer_token_obj = CandidatesUserObj.get_reset_token_function(self=user_exists)
      output_email = ui_email
      output_subject_line = 'Password Reset - Triviafy'
      output_message_content = f"To reset your password, visit the following link: https://triviafy.com/candidates/reset/{serializer_token_obj} \n\nThis link will expire after 30 minutes.\nIf you did not make this request then simply ignore this email and no changes will be made."
      send_email_template_function(output_email, output_subject_line, output_message_content)
      # ------------------------ send email with token url end ------------------------
    else:
      forgot_password_error_statement = 'Password reset link sent to email.'
      pass
    # ------------------------ check if user email exists in db end ------------------------
  localhost_print_function('=========================================== candidates_forgot_password_page_function END ===========================================')
  return render_template('candidates/exterior/forgot_password/index.html', user=current_user, error_message_to_html = forgot_password_error_statement)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/candidates/reset/<token>', methods=['GET', 'POST'])
def candidates_reset_forgot_password_page_function(token):
  localhost_print_function('=========================================== candidates_reset_forgot_password_page_function START ===========================================')
  # if current_user.is_authenticated == False:
  #   return redirect(url_for('views_interior.login_dashboard_page_function'))
  reset_password_error_statement = ''
  user_obj_from_token = CandidatesUserObj.verify_reset_token_function(token)
  if user_obj_from_token is None:
    reset_password_error_statement = 'That is an invalid or expired token'
    localhost_print_function('=========================================== candidates_reset_forgot_password_page_function END ===========================================')
    return render_template('candidates/exterior/forgot_password/index.html', user=current_user, error_message_to_html = reset_password_error_statement)
  if request.method == 'POST':
    reset_password_error_statement = ''
    # ------------------------ get inputs from form start ------------------------
    ui_password = request.form.get('reset_forgot_password_page_ui_password')
    ui_password_confirmed = request.form.get('reset_forgot_password_page_ui_password_confirmed')
    # ------------------------ get inputs from form end ------------------------
    # ------------------------ check match start ------------------------
    if ui_password != ui_password_confirmed:
      reset_password_error_statement = 'Passwords do not match.'
    # ------------------------ check match end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_cleaned = sanitize_password_function(ui_password)
    if ui_password_cleaned == False:
      reset_password_error_statement = 'Password is not valid.'
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_confirmed_cleaned = sanitize_password_function(ui_password_confirmed)
    if ui_password_confirmed_cleaned == False:
      reset_password_error_statement = 'Password is not valid.'
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ update db start ------------------------
    if reset_password_error_statement == '':
      user_obj_from_token.password = generate_password_hash(ui_password, method="sha256")
      db.session.commit()
      return redirect(url_for('views_interior.login_dashboard_page_function'))
    # ------------------------ update db end ------------------------
  localhost_print_function('=========================================== candidates_reset_forgot_password_page_function END ===========================================')
  return render_template('candidates/exterior/forgot_password/reset_forgot_password/index.html', user=current_user, error_message_to_html = reset_password_error_statement)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/candidates/blog', methods=['GET', 'POST'])
def candidates_blog_page_function():
  localhost_print_function('=========================================== candidates_blog_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_blog_page_function END ===========================================')
  return render_template('candidates/exterior/blog/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@views_exterior.route('/candidates/blog/<i_blog_post_number>', methods=['GET', 'POST'])
def candidates_i_blog_page_function(i_blog_post_number):
  localhost_print_function('=========================================== candidates_i_blog_page_function START ===========================================')
  current_blog_post_num = i_blog_post_number
  current_blog_post_num_full_string = f'candidates/exterior/blog/i_blog/i_{current_blog_post_num}.html'
  localhost_print_function('=========================================== candidates_i_blog_page_function END ===========================================')
  return render_template(current_blog_post_num_full_string)
# ------------------------ individual route end ------------------------
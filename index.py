# -------------------------------------------------------------- Imports
import os, time
import datetime
from flask import Flask, session, render_template

# ------------------------ Pages START ------------------------
# Index page
from backend.page_templates_backend.index_page_backend.index_page_render_template import index_page_render_template
# Admin page
from backend.page_templates_backend.admin_page_backend.admin_index_page_render_template import admin_index_page_render_template
from backend.page_templates_backend.admin_page_backend.admin_leaderboard_index_page_render_template import admin_leaderboard_index_page_render_template
# About page
from backend.page_templates_backend.about_page_backend.about_index_page_render_template import about_index_page_render_template
# Demo page
from backend.page_templates_backend.demo_page_backend.demo_page_render_template import demo_page_render_template
# Privacy page
from backend.page_templates_backend.privacy_policy_page_backend.privacy_policy_index_page_render_template import privacy_policy_index_page_render_template
# TOS page
from backend.page_templates_backend.terms_of_service_page_backend.terms_of_service_index_page_render_template import terms_of_service_index_page_render_template
# FAQ page
from backend.page_templates_backend.faq_page_backend.faq_index_page_render_template import faq_index_page_render_template
# Slack authentication pages
from backend.page_templates_backend.slack_confirm_oauth_redirect_dashboard_backend.slack_confirm_oauth_redirect_dashboard_index import slack_confirm_oauth_redirect_dashboard_index
from backend.page_templates_backend.slack_sign_in_with_slack_page_backend.slack_oauth_redirect_page_index import slack_oauth_redirect_page_index
from backend.page_templates_backend.slack_sign_in_with_before_add_to_slack_page_backend.slack_sign_in_with_before_add_to_slack_page_render_template import slack_sign_in_with_before_add_to_slack_page_render_template
# Email Notifications Confirm pages
from backend.page_templates_backend.email_permission_notification_page_backend.email_permission_notification_page_render_template import email_permission_notification_page_render_template
from backend.page_templates_backend.email_permission_notification_page_backend.email_permission_notification_consent_processing import email_permission_notification_consent_processing
# New User Questionnaire
from backend.page_templates_backend.new_user_questionnaire_page_backend.new_user_questionnaire_index_page_render_template import new_user_questionnaire_index_page_render_template
from backend.page_templates_backend.new_user_questionnaire_page_backend.new_user_questionnaire_submit_processing import new_user_questionnaire_submit_processing
# Slack dashboard pages
from backend.page_templates_backend.dashboard_page_backend.dashboard_index_page_render_template import dashboard_index_page_render_template
from backend.page_templates_backend.submit_quiz_backend.submit_quiz_backend import submit_quiz_backend
from backend.page_templates_backend.dashboard_page_backend.quiz_past_due_page_backend.quiz_past_due_page_render_template import quiz_past_due_page_render_template
from backend.page_templates_backend.dashboard_page_backend.quiz_graded_end_of_week_view_page_backend.quiz_graded_end_of_week_view_page_render_template import quiz_graded_end_of_week_view_page_render_template
from backend.page_templates_backend.dashboard_page_backend.quiz_no_latest_quiz_yet_page_backend.quiz_no_latest_quiz_yet_page_render_template import quiz_no_latest_quiz_yet_page_render_template
from backend.page_templates_backend.dashboard_page_backend.quiz_pre_open_page_backend.quiz_pre_open_page_render_template import quiz_pre_open_page_render_template
# Download PDF
from backend.page_templates_backend.download_example_quiz_pdf_backend.download_example_quiz_pdf_redirect import download_example_quiz_pdf_redirect
from backend.page_templates_backend.download_example_quiz_pdf_backend.download_engineering_example_quiz_pdf_backend.download_engineering_example_quiz_pdf_redirect import download_engineering_example_quiz_pdf_redirect
from backend.page_templates_backend.download_example_quiz_pdf_backend.download_hr_example_quiz_pdf_backend.download_hr_example_quiz_pdf_redirect import download_hr_example_quiz_pdf_redirect
from backend.page_templates_backend.download_example_quiz_pdf_backend.download_marketing_example_quiz_pdf_backend.download_marketing_example_quiz_pdf_redirect import download_marketing_example_quiz_pdf_redirect
from backend.page_templates_backend.download_example_quiz_pdf_backend.download_finance_example_quiz_pdf_backend.download_finance_example_quiz_pdf_redirect import download_finance_example_quiz_pdf_redirect
from backend.page_templates_backend.download_example_quiz_pdf_backend.download_javascript_example_quiz_pdf_backend.download_javascript_example_quiz_pdf_redirect import download_javascript_example_quiz_pdf_redirect
from backend.page_templates_backend.download_example_quiz_pdf_backend.download_excel_example_quiz_pdf_backend.download_excel_example_quiz_pdf_redirect import download_excel_example_quiz_pdf_redirect
from backend.page_templates_backend.download_example_quiz_pdf_backend.download_sql_example_quiz_pdf_backend.download_sql_example_quiz_pdf_redirect import download_sql_example_quiz_pdf_redirect
from backend.page_templates_backend.download_example_quiz_pdf_backend.download_tableau_example_quiz_pdf_backend.download_tableau_example_quiz_pdf_redirect import download_tableau_example_quiz_pdf_redirect
from backend.page_templates_backend.download_triviafy_setup_steps_slack_backend.download_triviafy_setup_slack_pdf_redirect import download_triviafy_setup_slack_pdf_redirect
from backend.page_templates_backend.download_example_quiz_pdf_backend.download_mixed_categories_example_quiz_pdf_backend.download_mixed_categories_example_quiz_pdf_redirect import download_mixed_categories_example_quiz_pdf_redirect
# Setup Slack Pages
from backend.page_templates_backend.setup_slack_page_backend.setup_slack_index_page_render_template import setup_slack_index_page_render_template
# Example Quiz Pages
from backend.page_templates_backend.example_quizzes_not_signed_in_page_backend.example_quiz_excel_render_template import example_quiz_excel_render_template
from backend.page_templates_backend.example_quizzes_not_signed_in_page_backend.example_quiz_javascript_render_template import example_quiz_javascript_render_template
from backend.page_templates_backend.example_quizzes_not_signed_in_page_backend.example_quiz_sql_render_template import example_quiz_sql_render_template
from backend.page_templates_backend.example_quizzes_not_signed_in_page_backend.example_quiz_tableau_render_template import example_quiz_tableau_render_template
from backend.page_templates_backend.example_quizzes_not_signed_in_page_backend.example_quiz_team_analytics_render_template import example_quiz_team_analytics_render_template
from backend.page_templates_backend.example_quizzes_not_signed_in_page_backend.example_quiz_engineering_render_template import example_quiz_engineering_render_template
from backend.page_templates_backend.example_quizzes_not_signed_in_page_backend.example_quiz_hr_render_template import example_quiz_hr_render_template
from backend.page_templates_backend.example_quizzes_not_signed_in_page_backend.example_quiz_marketing_render_template import example_quiz_marketing_render_template
from backend.page_templates_backend.example_quizzes_not_signed_in_page_backend.example_quiz_finance_render_template import example_quiz_finance_render_template
from backend.page_templates_backend.example_quizzes_not_signed_in_page_backend.example_quiz_mixed_categories_render_template import example_quiz_mixed_categories_render_template
# Slack account pages
from backend.page_templates_backend.account_page_backend.account_index_page_render_template import account_index_page_render_template
from backend.page_templates_backend.account_page_backend.account_edit_settings_page_backend.account_edit_settings_page_render_template import account_edit_settings_page_render_template
from backend.page_templates_backend.account_page_backend.account_edit_settings_page_backend.account_edit_settings_processing_changes_page_render_template import account_edit_settings_processing_changes_page_render_template
from backend.page_templates_backend.account_page_backend.logout import logout
# Create question pages
from backend.page_templates_backend.waitlist_page_backend.waitlist_create_question_page_backend.waitlist_create_question_page_render_template import waitlist_create_question_page_render_template
from backend.page_templates_backend.waitlist_page_backend.waitlist_create_question_page_backend.waitlist_create_question_add_to_database_processing import waitlist_create_question_add_to_database_processing
from backend.page_templates_backend.waitlist_page_backend.waitlist_create_question_page_backend.waitlist_create_question_confirm_on_waitlist_page_render_template import waitlist_create_question_confirm_on_waitlist_page_render_template
from backend.page_templates_backend.create_question_page_backend.create_question_index_page_render_template import create_question_index_page_render_template
from backend.page_templates_backend.create_question_page_backend.create_question_submission_page_backend.create_question_submission_processing import create_question_submission_processing
from backend.page_templates_backend.create_question_page_backend.create_question_submission_page_backend.create_question_submission_success_page_render_template import create_question_submission_success_page_render_template
from backend.page_templates_backend.create_question_page_backend.create_question_rate_limit_backend.create_question_rate_limit_page_render_template import create_question_rate_limit_page_render_template
# Quiz Settings pages
from backend.page_templates_backend.quiz_settings_page_backend.quiz_settings_index_page_render_template import quiz_settings_index_page_render_template
from backend.page_templates_backend.quiz_settings_page_backend.edit_quiz_settings_page_backend.edit_quiz_settings_index_page_render_template import edit_quiz_settings_index_page_render_template
from backend.page_templates_backend.quiz_settings_page_backend.edit_quiz_settings_page_backend.edit_quiz_settings_submit_new_quiz_settings import edit_quiz_settings_submit_new_quiz_settings
# Quiz Categories pages
from backend.page_templates_backend.quiz_settings_page_backend.quiz_categories_page_backend.quiz_categories_index_page_render_template import quiz_categories_index_page_render_template
from backend.page_templates_backend.quiz_settings_page_backend.quiz_categories_page_backend.edit_quiz_categories_page_backend.edit_quiz_categories_index_page_render_template import edit_quiz_categories_index_page_render_template
from backend.page_templates_backend.quiz_settings_page_backend.quiz_categories_page_backend.edit_quiz_categories_page_backend.submit_edit_quiz_categories_processing import submit_edit_quiz_categories_processing
# Quiz Feedback pages
from backend.page_templates_backend.quiz_feedback_page_backend.quiz_feedback_index_page_render_template import quiz_feedback_index_page_render_template
from backend.page_templates_backend.quiz_feedback_page_backend.quiz_feedback_submission_page_backend.quiz_feedback_processing import quiz_feedback_processing
from backend.page_templates_backend.quiz_feedback_page_backend.quiz_feedback_submission_page_backend.quiz_feedback_success_page_render_template import quiz_feedback_success_page_render_template
# Quiz Archive pages
from backend.page_templates_backend.quiz_archive_page_backend.quiz_archive_none_yet_page_backend.quiz_archive_none_yet_page_render_template import quiz_archive_none_yet_page_render_template
from backend.page_templates_backend.quiz_archive_page_backend.quiz_archive_page_render_template import quiz_archive_page_render_template
from backend.page_templates_backend.quiz_archive_page_backend.quiz_archive_specific_quiz_number import quiz_archive_specific_quiz_number
# Leaderboard pages
from backend.page_templates_backend.leaderboard_page_backend.leaderboard_page_render_template import leaderboard_page_render_template
# Sample Quiz pages
from backend.page_templates_backend.sample_quiz_page_backend.sample_quiz_index_page_render_template import sample_quiz_index_page_render_template
from backend.page_templates_backend.sample_quiz_page_backend.grade_sample_quiz_page_backend.sample_quiz_graded_index_page_render_template import sample_quiz_graded_index_page_render_template
# Subscription pages
from backend.page_templates_backend.subscription_page_backend.subscription_index_page_render_template import subscription_index_page_render_template
# Claim Prize pages
from backend.page_templates_backend.claim_prize_page_backend.claim_prize_index_page_render_template import claim_prize_index_page_render_template
# Blog page
from backend.page_templates_backend.blog_page_backend.blog_index_page_render_template import blog_index_page_render_template
# Collect User Email Page
from backend.page_templates_backend.collect_email_page_backend.collect_email_processing import collect_email_processing
from backend.page_templates_backend.collect_email_page_backend.collect_email_confirm_page_backend.collect_email_confirm_page_render_template import collect_email_confirm_page_render_template
from backend.page_templates_backend.candidates_page_backend.utils.collect_email_backend.collect_email_processing_candidates import collect_email_processing_candidates
from backend.page_templates_backend.candidates_page_backend.utils.collect_email_backend.collect_email_processing_candidates_success import collect_email_processing_candidates_success
# Blog Single Post page
from backend.page_templates_backend.blog_page_backend.blog_single_post_page_backend.blog_single_post_0001_index_page_render_template import blog_single_post_0001_index_page_render_template
from backend.page_templates_backend.blog_page_backend.blog_single_post_page_backend.blog_single_post_0002_index_page_render_template import blog_single_post_0002_index_page_render_template
from backend.page_templates_backend.blog_page_backend.blog_single_post_page_backend.blog_single_post_0003_index_page_render_template import blog_single_post_0003_index_page_render_template
from backend.page_templates_backend.blog_page_backend.blog_single_post_page_backend.blog_single_post_0004_index_page_render_template import blog_single_post_0004_index_page_render_template
from backend.page_templates_backend.blog_page_backend.blog_single_post_page_backend.blog_single_post_0005_index_page_render_template import blog_single_post_0005_index_page_render_template
from backend.page_templates_backend.blog_page_backend.blog_single_post_page_backend.blog_single_post_0006_index_page_render_template import blog_single_post_0006_index_page_render_template
# Candidates - index page
from backend.page_templates_backend.candidates_page_backend.index_page_backend.candidates_page_render_template import candidates_page_render_template
# Candidates - about page
from backend.page_templates_backend.candidates_page_backend.about_page_backend.candidates_about_page_render_template import candidates_about_page_render_template
# Candidates - faq page
from backend.page_templates_backend.candidates_page_backend.faq_page_backend.candidates_faq_page_render_template import candidates_faq_page_render_template
# Candidates - pricing page
from backend.page_templates_backend.candidates_page_backend.pricing_page_backend.candidates_pricing_page_render_template import candidates_pricing_page_render_template
# Candidates - test library page
from backend.page_templates_backend.candidates_page_backend.test_library_page_backend.candidates_test_library_page_render_template import candidates_test_library_page_render_template
# Candidates - launch page
from backend.page_templates_backend.candidates_page_backend.stand_in_page_backend.login_stand_in_page_backend.launch_page_render_template import launch_page_render_template
# Candidates - login page
from backend.page_templates_backend.candidates_page_backend.login_page_backend.login_page_render_template import login_page_render_template
# ------------------------ Pages END ------------------------


# ------------------------ App setup START ------------------------
# Set the timezone of the application when user creates account is will be in US/Easterm time
os.environ['TZ'] = 'US/Eastern'
time.tzset()
# Flask constructor
app = Flask(__name__)
#app = Flask(__name__, static_folder="static", template_folder="templates")

# To use a session, there has to be a secret key. The string should be something difficult to guess
app.secret_key = os.urandom(64)
# Set session variables to perm so that user can remain signed in for x days
app.permanent_session_lifetime = datetime.timedelta(days=30)

# For removing cache from images for quiz questions. The URL was auto caching and not updating
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

  # ------------------------ Handleing Error Messages START ------------------------
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
  return render_template("error_404_page_templates/index.html")
  # ------------------------ Handleing Error Messages END ------------------------
# ------------------------ App setup END ------------------------


# ------------------------ Pages - Register START ------------------------
# Index page
app.register_blueprint(index_page_render_template, url_prefix="")
# Admin page
app.register_blueprint(admin_index_page_render_template, url_prefix="")
app.register_blueprint(admin_leaderboard_index_page_render_template, url_prefix="")
# About page
app.register_blueprint(about_index_page_render_template, url_prefix="")
# Demo page
app.register_blueprint(demo_page_render_template, url_prefix="")
# Privacy page
app.register_blueprint(privacy_policy_index_page_render_template, url_prefix="")
# Terms of Service page
app.register_blueprint(terms_of_service_index_page_render_template, url_prefix="")
# FAQ page
app.register_blueprint(faq_index_page_render_template, url_prefix="")
# Slack authentication pages
app.register_blueprint(slack_confirm_oauth_redirect_dashboard_index, url_prefix="")
app.register_blueprint(slack_oauth_redirect_page_index, url_prefix="")
app.register_blueprint(slack_sign_in_with_before_add_to_slack_page_render_template, url_prefix="")
# Email Notifications Confirm pages
app.register_blueprint(email_permission_notification_page_render_template, url_prefix="")
app.register_blueprint(email_permission_notification_consent_processing, url_prefix="")
# New User Questionnaire
app.register_blueprint(new_user_questionnaire_index_page_render_template, url_prefix="")
app.register_blueprint(new_user_questionnaire_submit_processing, url_prefix="")
# Slack dashboard pages
app.register_blueprint(dashboard_index_page_render_template, url_prefix="")
app.register_blueprint(submit_quiz_backend, url_prefix="")
app.register_blueprint(quiz_past_due_page_render_template, url_prefix="")
app.register_blueprint(quiz_graded_end_of_week_view_page_render_template, url_prefix="")
app.register_blueprint(quiz_no_latest_quiz_yet_page_render_template, url_prefix="")
app.register_blueprint(quiz_pre_open_page_render_template, url_prefix="")
# Download PDF
app.register_blueprint(download_example_quiz_pdf_redirect, url_prefix="")
app.register_blueprint(download_engineering_example_quiz_pdf_redirect, url_prefix="")
app.register_blueprint(download_hr_example_quiz_pdf_redirect, url_prefix="")
app.register_blueprint(download_marketing_example_quiz_pdf_redirect, url_prefix="")
app.register_blueprint(download_finance_example_quiz_pdf_redirect, url_prefix="")
app.register_blueprint(download_javascript_example_quiz_pdf_redirect, url_prefix="")
app.register_blueprint(download_excel_example_quiz_pdf_redirect, url_prefix="")
app.register_blueprint(download_sql_example_quiz_pdf_redirect, url_prefix="")
app.register_blueprint(download_tableau_example_quiz_pdf_redirect, url_prefix="")
app.register_blueprint(download_triviafy_setup_slack_pdf_redirect, url_prefix="")
app.register_blueprint(download_mixed_categories_example_quiz_pdf_redirect, url_prefix="")
# Setup Slack Pages
app.register_blueprint(setup_slack_index_page_render_template, url_prefix="")
# Example Quiz Pages
app.register_blueprint(example_quiz_excel_render_template, url_prefix="")
app.register_blueprint(example_quiz_javascript_render_template, url_prefix="")
app.register_blueprint(example_quiz_sql_render_template, url_prefix="")
app.register_blueprint(example_quiz_tableau_render_template, url_prefix="")
app.register_blueprint(example_quiz_team_analytics_render_template, url_prefix="")
app.register_blueprint(example_quiz_engineering_render_template, url_prefix="")
app.register_blueprint(example_quiz_hr_render_template, url_prefix="")
app.register_blueprint(example_quiz_marketing_render_template, url_prefix="")
app.register_blueprint(example_quiz_finance_render_template, url_prefix="")
app.register_blueprint(example_quiz_mixed_categories_render_template, url_prefix="")
# Slack account pages
app.register_blueprint(account_index_page_render_template, url_prefix="")
app.register_blueprint(account_edit_settings_page_render_template, url_prefix="")
app.register_blueprint(account_edit_settings_processing_changes_page_render_template, url_prefix="")
app.register_blueprint(logout, url_prefix="")
# Create question pages
app.register_blueprint(waitlist_create_question_page_render_template, url_prefix="")
app.register_blueprint(waitlist_create_question_add_to_database_processing, url_prefix="")
app.register_blueprint(waitlist_create_question_confirm_on_waitlist_page_render_template, url_prefix="")
app.register_blueprint(create_question_index_page_render_template, url_prefix="")
app.register_blueprint(create_question_submission_processing, url_prefix="")
app.register_blueprint(create_question_submission_success_page_render_template, url_prefix="")
app.register_blueprint(create_question_rate_limit_page_render_template, url_prefix="")
# Quiz Settings pages
app.register_blueprint(quiz_settings_index_page_render_template, url_prefix="")
app.register_blueprint(edit_quiz_settings_index_page_render_template, url_prefix="")
app.register_blueprint(edit_quiz_settings_submit_new_quiz_settings, url_prefix="")
# Quiz Categories pages
app.register_blueprint(quiz_categories_index_page_render_template, url_prefix="")
app.register_blueprint(edit_quiz_categories_index_page_render_template, url_prefix="")
app.register_blueprint(submit_edit_quiz_categories_processing, url_prefix="")
# Quiz Feedback pages
app.register_blueprint(quiz_feedback_index_page_render_template, url_prefix="")
app.register_blueprint(quiz_feedback_processing, url_prefix="")
app.register_blueprint(quiz_feedback_success_page_render_template, url_prefix="")
# Quiz Archive pages
app.register_blueprint(quiz_archive_none_yet_page_render_template, url_prefix="")
app.register_blueprint(quiz_archive_page_render_template, url_prefix="")
app.register_blueprint(quiz_archive_specific_quiz_number, url_prefix="")
# Leaderboard pages
app.register_blueprint(leaderboard_page_render_template, url_prefix="")
# Sample Quiz pages
app.register_blueprint(sample_quiz_index_page_render_template, url_prefix="")
app.register_blueprint(sample_quiz_graded_index_page_render_template, url_prefix="")
# Subscription pages
app.register_blueprint(subscription_index_page_render_template, url_prefix="")
# Claim Prize pages
app.register_blueprint(claim_prize_index_page_render_template, url_prefix="")
# Blog page
app.register_blueprint(blog_index_page_render_template, url_prefix="")
# Collect User Email Page
app.register_blueprint(collect_email_processing, url_prefix="")
app.register_blueprint(collect_email_confirm_page_render_template, url_prefix="")
app.register_blueprint(collect_email_processing_candidates, url_prefix="")
app.register_blueprint(collect_email_processing_candidates_success, url_prefix="")
# Blog Single Post page
app.register_blueprint(blog_single_post_0001_index_page_render_template, url_prefix="")
app.register_blueprint(blog_single_post_0002_index_page_render_template, url_prefix="")
app.register_blueprint(blog_single_post_0003_index_page_render_template, url_prefix="")
app.register_blueprint(blog_single_post_0004_index_page_render_template, url_prefix="")
app.register_blueprint(blog_single_post_0005_index_page_render_template, url_prefix="")
app.register_blueprint(blog_single_post_0006_index_page_render_template, url_prefix="")
# Candidates page
app.register_blueprint(candidates_page_render_template, url_prefix="")
# Candidates about page
app.register_blueprint(candidates_about_page_render_template, url_prefix="")
# Candidates faq page
app.register_blueprint(candidates_faq_page_render_template, url_prefix="")
# Candidates pricing page
app.register_blueprint(candidates_pricing_page_render_template, url_prefix="")
# Candidates test library page
app.register_blueprint(candidates_test_library_page_render_template, url_prefix="")
# Candidates launch  page
app.register_blueprint(launch_page_render_template, url_prefix="")
# Candidates login  page
app.register_blueprint(login_page_render_template, url_prefix="")
# ------------------------ Pages - Register END ------------------------





# =========================================================================================================== Run app
# Run the main program
if __name__ == "__main__":

  # Check environment variable that was passed in from user on the command line
  server_env = os.environ.get('TESTING', 'false')
  # ------------------------ Running on localhost START ------------------------
  if server_env and server_env == 'true':
    print('RUNNING ON LOCALHOST')
    app.run(debug = True, host='0.0.0.0', port=80, use_reloader=False)
  # ------------------------ Running on localhost END ------------------------


  # ------------------------ Running on heroku server START ------------------------
  else:
    # port and run for Heroku
    print('RUNNING ON PRODUCTION')
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)
  # ------------------------ Running on heroku server END ------------------------
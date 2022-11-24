# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -note: any pages related to authentication will be in this auth.py file
# -@login_required   # this decorator says that url cannot be accessed unless the user is logged in. 
# -@login_required: <-- This decorator will bring a user to __init__ code: [login_manager.login_view = 'auth.candidates_login_page_function'] if they hit a page that requires login and they are not logged in.
# -use code: <methods=['GET', 'POST']> when you want the user to interact with the page through forms/checkbox/textbox/radio/etc.
# ------------------------ info about this file end ------------------------


# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import CandidatesUserObj, CandidatesCollectEmailObj
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from website.backend.candidates.user_inputs import sanitize_email_function, sanitize_password_function, sanitize_create_account_text_inputs_function
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
import os
# ------------------------ imports end ------------------------


# ------------------------ function start ------------------------
blog = Blueprint('blog', __name__)
# ------------------------ function end ------------------------
# ------------------------ before page variables start ------------------------
cache_busting_output = create_uuid_function('css_')
# ------------------------ before page variables end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------


# ------------------------ individual route start ------------------------
@blog.route('/candidates/blog', methods=['GET', 'POST'])
def candidates_blog_page_function():
  localhost_print_function('=========================================== candidates_blog_page_function START ===========================================')
  localhost_print_function('=========================================== candidates_blog_page_function END ===========================================')
  return render_template('candidates_page_templates/not_logged_in_page_templates/blog_page_templates/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@blog.route('/candidates/blog/<i_blog_post_number>', methods=['GET', 'POST'])
def candidates_i_blog_page_function(i_blog_post_number):
  localhost_print_function('=========================================== candidates_i_blog_page_function START ===========================================')
  current_blog_post_num = i_blog_post_number
  current_blog_post_num_full_string = f'candidates_page_templates/not_logged_in_page_templates/blog_page_templates/individual_blog_page_templates/i_blog_post_{current_blog_post_num}.html'
  localhost_print_function('=========================================== candidates_i_blog_page_function END ===========================================')
  return render_template(current_blog_post_num_full_string)
# ------------------------ individual route end ------------------------
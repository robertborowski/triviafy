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
from flask_login import current_user
from website.backend.candidates.redis import redis_connect_to_database_function
from website.models import UserObj, BlogPollingObj, ShowsObj, PollsObj, ShowsQueueObj
# from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
from website import db
from website.backend.candidates.user_inputs import sanitize_email_function, sanitize_password_function
from werkzeug.security import generate_password_hash
from website.backend.candidates.send_emails import send_email_template_function
from website.backend.candidates.user_inputs import alert_message_default_function_v2
import datetime
from website.backend.sql_statements.select import select_general_function
from website.backend.user_inputs import sanitize_letters_numbers_spaces_specials_only_function
from website.backend.spotify import spotify_search_show_function
from website.backend.get_create_obj import get_show_based_on_name_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
import json
from website.backend.dict_manipulation import arr_of_dict_all_columns_single_item_function, prep_poll_dict_function
import os
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
polling_views_exterior = Blueprint('polling_views_exterior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_exterior.route('/polling/details')
@polling_views_exterior.route('/polling/details/')
def polling_landing_details_function():
  # ------------------------ set variables start ------------------------
  page_dict = {}
  # ------------------------ set variables end ------------------------
  # ------------------------ get random podcast show info start ------------------------
  show_arr_of_dict = select_general_function('select_query_general_7')
  page_dict['show_dict'] = show_arr_of_dict[0]
  # ------------------------ get random podcast show info end ------------------------
  return render_template('polling/exterior/landing/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_exterior.route('/polling', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/<url_step_code>', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/<url_step_code>/', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/<url_step_code>/<url_platform_id>', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/<url_step_code>/<url_platform_id>/', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/<url_step_code>/<url_platform_id>/<url_redis_key>', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/<url_step_code>/<url_platform_id>/<url_redis_key>/', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/<url_step_code>/<url_platform_id>/<url_redis_key>/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/<url_step_code>/<url_platform_id>/<url_redis_key>/<url_redirect_code>/', methods=['GET', 'POST'])
def polling_landing_function(url_redirect_code=None, url_step_code=None, url_platform_id=None, url_redis_key=None):
  # ------------------------ page dict start ------------------------
  if url_redirect_code == None:
    try:
      url_redirect_code = request.args.get('url_redirect_code')
    except:
      pass
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ remove from redis check start ------------------------
  try:
    wip_key = request.args.get('wip_key')
    if wip_key != None and wip_key != '':
      redis_connection.delete(wip_key)
  except:
    pass
  # ------------------------ remove from redis check end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['url_step_code'] = url_step_code
  page_dict['url_platform_id'] = url_platform_id
  page_dict['url_redis_key'] = url_redis_key
  page_dict['url_next_step_code'] = ''
  page_dict['url_previous_step_code'] = ''
  page_dict['platforms_arr'] = []
  page_dict['shows_arr_of_dicts'] = []
  page_dict['url_step_title'] = ''
  page_dict['url_back_str'] = ''
  page_dict['spotify_pulled_arr_of_dict'] = None
  spotify_pulled_arr_of_dict = []
  # ------------------------ set variables end ------------------------
  # ------------------------ step code defaults/checks start ------------------------
  if url_step_code == None:
    url_step_code = '1'
  page_dict['url_step_code'] = url_step_code
  if url_step_code == '1':
    page_dict['url_next_step_code'] = '2'
    page_dict['url_previous_step_code'] = '1'
  if url_step_code == '2':
    page_dict['url_next_step_code'] = '3'
    page_dict['url_previous_step_code'] = '2'
    page_dict['url_step_title'] = 'Confirm show'
  if url_platform_id == None:
    url_platform_id = 'platform001'
  page_dict['url_platform_id'] = url_platform_id
  # ------------------------ step code doesnt exist start ------------------------
  try:
    if int(url_step_code) < int(1) or int(url_step_code) < int(3):
      pass
  except:
    return redirect(url_for('polling_views_exterior.polling_landing_function', url_step_code='1', url_platform_id=page_dict['url_platform_id']))
  # ------------------------ step code doesnt exist end ------------------------
  # ------------------------ step code defaults/checks end ------------------------
  if page_dict['url_step_code'] == '2' and page_dict['url_redis_key'] != None:
    try:
      redis_pulled_value = redis_connection.get(url_redis_key).decode('utf-8')
      spotify_pulled_arr_of_dict = json.loads(redis_pulled_value)
      page_dict['spotify_pulled_arr_of_dict'] = spotify_pulled_arr_of_dict
      # ------------------------ spotify exists already check start ------------------------
      page_dict['spotify_dict_exists_in_db'] = False
      page_dict['spotify_dict_exists_show_id'] = False
      try:
        db_obj = ShowsObj.query.filter_by(name=page_dict['spotify_pulled_arr_of_dict'][0]['name']).first()
        if db_obj != None and db_obj != []:
          page_dict['spotify_dict_exists_in_db'] = True
          page_dict['spotify_dict_exists_show_id'] = db_obj.id
        pass
      except:
        pass
      # ------------------------ spotify exists already check end ------------------------
    except:
      pass
  # ------------------------ pull from redis if exists end ------------------------
  # ------------------------ get all podcasts start ------------------------
  if url_step_code == '1':
    show_arr_of_dict = select_general_function('select_query_general_8')
    for i in show_arr_of_dict:
      page_dict['shows_arr_of_dicts'].append(i)
  # ------------------------ get all podcasts end ------------------------
  if request.method == 'POST':
    if page_dict['url_step_code'] == '1':
      # ------------------------ get user inputs start ------------------------
      ui_search_show_name = request.form.get('ui_search_show_name')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ sanitize ui start ------------------------
      ui_search_show_name_check = sanitize_letters_numbers_spaces_specials_only_function(ui_search_show_name)
      if ui_search_show_name_check == False:
        return redirect(url_for('polling_views_exterior.polling_landing_function', url_step_code=url_step_code, url_platform_id=url_platform_id, url_redirect_code='e6'))
      # ------------------------ sanitize ui end ------------------------
      # ------------------------ search spotify start ------------------------
      spotify_pulled_arr_of_dict = spotify_search_show_function(ui_search_show_name)
      if spotify_pulled_arr_of_dict == None:
        return redirect(url_for('polling_views_exterior.polling_landing_function', url_step_code=url_step_code, url_platform_id=url_platform_id, url_redirect_code='e32'))
      # ------------------------ search spotify end ------------------------
      # ------------------------ check if show already in db start ------------------------
      show_already_exists_check = get_show_based_on_name_function(url_platform_id, spotify_pulled_arr_of_dict[0]['name'])
      if show_already_exists_check != None:
        page_dict['spotify_dict_exists_show_id'] = show_already_exists_check.id
      # ------------------------ check if show already in db end ------------------------
      # ------------------------ add spotify result to redis start ------------------------
      url_redis_key = create_uuid_function('spotify_temp_')
      redis_connection.set(url_redis_key, json.dumps(spotify_pulled_arr_of_dict[0]).encode('utf-8'))
      # ------------------------ add spotify result to redis end ------------------------
      return redirect(url_for('polling_views_exterior.polling_landing_function', url_step_code=page_dict['url_next_step_code'], url_platform_id=url_platform_id, url_redis_key=url_redis_key))
    localhost_print_function(' ------------- 100-preview start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-preview end ------------- ')
  return render_template('polling/exterior/landing_interactive/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_exterior.route('/polling/preview/show/<url_show_id>', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/preview/show/<url_show_id>/', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/preview/show/<url_show_id>/<url_poll_id>', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/preview/show/<url_show_id>/<url_poll_id>/', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/preview/show/<url_show_id>/<url_poll_id>/<url_redis_key>', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/preview/show/<url_show_id>/<url_poll_id>/<url_redis_key>/', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/preview/show/<url_show_id>/<url_poll_id>/<url_redis_key>/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/preview/show/<url_show_id>/<url_poll_id>/<url_redis_key>/<url_redirect_code>/', methods=['GET', 'POST'])
def polling_exterior_show_function(url_redirect_code=None, url_show_id=None, url_poll_id=None, url_redis_key=None):
  # ------------------------ page dict start ------------------------
  if url_redirect_code == None:
    try:
      url_redirect_code = request.args.get('url_redirect_code')
    except:
      pass
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['url_show_id'] = url_show_id
  page_dict['url_poll_id'] = url_poll_id
  page_dict['url_redis_key'] = url_redis_key
  page_dict['poll_dict'] = None
  page_dict['db_show_dict'] = None
  # ------------------------ set variables end ------------------------
  # ------------------------ redis key start ------------------------
  if page_dict['url_redis_key'] == None:
    try:
      page_dict['url_redis_key'] = request.args.get('url_redis_key')
    except:
      pass
  # ------------------------ redis key end ------------------------
  # ------------------------ delete redis key start ------------------------
  try:
    redis_connection.delete(page_dict['url_redis_key'])
  except:
    pass
  # ------------------------ delete redis key end ------------------------
  # ------------------------ check show id exists start ------------------------
  if page_dict['url_show_id'] == None:
    return redirect(url_for('polling_views_exterior.polling_landing_function'))
  db_obj = ShowsObj.query.filter_by(id=page_dict['url_show_id']).first()
  if db_obj == None or db_obj == []:
    return redirect(url_for('polling_views_exterior.polling_landing_function'))
  # ------------------------ check show id exists end ------------------------
  # ------------------------ get show info start ------------------------
  page_dict['db_show_dict'] = arr_of_dict_all_columns_single_item_function(db_obj)
  title_limit = 15
  if len(page_dict['db_show_dict']['name']) > title_limit:
    page_dict['db_show_dict']['name_title'] = page_dict['db_show_dict']['name'][0:title_limit] + '...'
  else:
    page_dict['db_show_dict']['name_title'] = page_dict['db_show_dict']['name']
  # ------------------------ get show info end ------------------------
  # ------------------------ if poll id blank get latest episode start ------------------------
  if page_dict['url_poll_id'] == None:
    try:
      db_obj = PollsObj.query.filter_by(fk_show_id=page_dict['url_show_id'],status_approved=True,status_removed=False).order_by(PollsObj.created_timestamp.desc()).first()
      page_dict['url_poll_id'] = db_obj.id
      return redirect(url_for('polling_views_exterior.polling_exterior_show_function', url_show_id=page_dict['url_show_id'], url_poll_id=page_dict['url_poll_id']))
    except:
      pass
  # ------------------------ if poll id blank get latest episode end ------------------------
  # ------------------------ get poll info start ------------------------
  try:
    db_obj = PollsObj.query.filter_by(id=page_dict['url_poll_id']).first()
    db_dict = arr_of_dict_all_columns_single_item_function(db_obj)
    page_dict['poll_dict'] = prep_poll_dict_function(db_dict)
  except:
    pass
  # ------------------------ get poll info end ------------------------
  localhost_print_function(' ------------- 100-poll exterior start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-poll exterior end ------------- ')
  return render_template('polling/exterior/poll/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_exterior.route('/polling/preview/show/add/<url_redis_key>', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/preview/show/add/<url_redis_key>/', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/preview/show/add/<url_redis_key>/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/preview/show/add/<url_redis_key>/<url_redirect_code>/', methods=['GET', 'POST'])
def polling_exterior_add_show_function(url_redirect_code=None, url_redis_key=None):
  # ------------------------ page dict start ------------------------
  if url_redirect_code == None:
    try:
      url_redirect_code = request.args.get('url_redirect_code')
    except:
      pass
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['url_redis_key'] = url_redis_key
  page_dict['spotify_pulled_arr_of_dict'] = None
  # ------------------------ set variables end ------------------------
  # ------------------------ get redis key value start ------------------------
  try:
    redis_pulled_value = redis_connection.get(url_redis_key).decode('utf-8')
    spotify_pulled_arr_of_dict = json.loads(redis_pulled_value)
    page_dict['spotify_pulled_arr_of_dict'] = spotify_pulled_arr_of_dict
  except:
    page_dict['url_redis_key'] = None
    pass
  # ------------------------ get redis key value end ------------------------
  # ------------------------ if redis key null start ------------------------
  if page_dict['url_redis_key'] == None:
    return redirect(url_for('polling_views_exterior.polling_landing_function'))
  # ------------------------ if redis key null end ------------------------
  # ------------------------ add to queue start ------------------------
  # ------------------------ check show does not exist start ------------------------
  db_obj = ShowsObj.query.filter_by(name=page_dict['spotify_pulled_arr_of_dict']['name']).first()
  if db_obj != None and db_obj != []:
    return redirect(url_for('polling_views_exterior.polling_exterior_show_function', url_show_id=db_obj.id))
  # ------------------------ check show does not exist end ------------------------  
  # ------------------------ check if already in queue start ------------------------
  db_queue_obj = ShowsQueueObj.query.filter_by(name=page_dict['spotify_pulled_arr_of_dict']['name']).first()
  # ------------------------ check if already in queue end ------------------------
  if db_queue_obj == None:
    # ------------------------ add to live job queue start ------------------------
    new_row = ShowsQueueObj(
      id=create_uuid_function('queue_'),
      created_timestamp=create_timestamp_function(),
      fk_platform_id = 'platform001',
      platform_reference_id = page_dict['spotify_pulled_arr_of_dict']['id'],
      name=page_dict['spotify_pulled_arr_of_dict']['name'],
      description=page_dict['spotify_pulled_arr_of_dict']['description'],
      img_large=page_dict['spotify_pulled_arr_of_dict']['img_large'],
      img_medium=page_dict['spotify_pulled_arr_of_dict']['img_medium'],
      img_small=page_dict['spotify_pulled_arr_of_dict']['img_small'],
      show_url=page_dict['spotify_pulled_arr_of_dict']['show_url']
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ add to live job queue end ------------------------
    # ------------------------ email self start ------------------------
    try:
      output_to_email = os.environ.get('TRIVIAFY_NOTIFICATIONS_EMAIL')
      output_subject = f"Exterior landing - User added show to queue"
      output_body = f"Exterior landing - User added show to queue: '{page_dict['spotify_pulled_arr_of_dict']['name']}'"
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
    # ------------------------ email self end ------------------------
    # ------------------------ delete redis key start ------------------------
    try:
      redis_connection.delete(page_dict['url_redis_key'])
    except:
      pass
    # ------------------------ delete redis key end ------------------------
  # ------------------------ add to queue end ------------------------
  localhost_print_function(' ------------- 100-show add to queue exterior start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-show add to queue exterior end ------------- ')
  return redirect(url_for('polling_auth.polling_signup_function'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_exterior.route('/polling/reset', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/reset/<url_redirect_code>', methods=['GET', 'POST'])
def polling_forgot_password_function(url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
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
    user_exists = UserObj.query.filter_by(email=ui_email,signup_product='polling').first()
    if user_exists:
      forgot_password_error_statement = 'Password reset link sent to email.'
      # ------------------------ send email with token url start ------------------------
      serializer_token_obj = UserObj.get_reset_token_function(self=user_exists)
      output_email = ui_email
      output_subject_line = 'Password Reset - Triviafy'
      output_message_content = f"To reset your password, visit the following link: https://triviafy.com/polling/reset/{serializer_token_obj}/ \
                                This link will expire after 30 minutes.\nIf you did not make this request then simply ignore this email and no changes will be made."
      send_email_template_function(output_email, output_subject_line, output_message_content)
      # ------------------------ send email with token url end ------------------------
    else:
      forgot_password_error_statement = 'Password reset link sent to email.'
      pass
    # ------------------------ check if user email exists in db end ------------------------
    # ------------------------ success code start ------------------------
    alert_message_dict = alert_message_default_function_v2('s13')
    page_dict['alert_message_dict'] = alert_message_dict
    # ------------------------ success code end ------------------------
  return render_template('polling/exterior/forgot_password/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_exterior.route('/polling/reset/<token>', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/reset/<token>/', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/reset/<token>/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_exterior.route('/polling/reset/<token>/<url_redirect_code>/', methods=['GET', 'POST'])
def polling_reset_forgot_password_function(token, url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  user_obj_from_token = UserObj.verify_reset_token_function(token)
  if user_obj_from_token is None:
    return redirect(url_for('polling_views_exterior.polling_reset_forgot_password_function', token=token, url_redirect_code='e28'))
  if request.method == 'POST':
    # ------------------------ get inputs from form start ------------------------
    ui_password = request.form.get('reset_forgot_password_page_ui_password')
    ui_password_confirmed = request.form.get('reset_forgot_password_page_ui_password_confirmed')
    # ------------------------ get inputs from form end ------------------------
    # ------------------------ check match start ------------------------
    if ui_password != ui_password_confirmed:
      return redirect(url_for('polling_views_exterior.polling_reset_forgot_password_function', token=token, url_redirect_code='e29'))
    # ------------------------ check match end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_cleaned = sanitize_password_function(ui_password)
    if ui_password_cleaned == False:
      return redirect(url_for('polling_views_exterior.polling_reset_forgot_password_function', token=token, url_redirect_code='e6'))
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_confirmed_cleaned = sanitize_password_function(ui_password_confirmed)
    if ui_password_confirmed_cleaned == False:
      return redirect(url_for('polling_views_exterior.polling_reset_forgot_password_function', token=token, url_redirect_code='e6'))
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ update db start ------------------------
    user_obj_from_token.password = generate_password_hash(ui_password, method="sha256")
    db.session.commit()
    return redirect(url_for('polling_auth.polling_login_function', url_redirect_code='s6'))
    # ------------------------ update db end ------------------------
  return render_template('polling/exterior/forgot_password/reset_forgot_password/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_exterior.route('/polling/blog')
@polling_views_exterior.route('/polling/blog/')
def polling_all_blogs_function():
  # ------------------------ page dict start ------------------------
  page_dict = {}
  # ------------------------ page dict end ------------------------
  # ------------------------ get all blogs start ------------------------
  master_arr_of_dicts = []
  blog_obj = BlogPollingObj.query.filter_by(status=True).order_by(BlogPollingObj.created_timestamp.desc()).all()
  for i_obj in blog_obj:
    i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
    i_dict['title_url'] = i_dict['title'].replace(' ','-')
    i_dict['title'] = i_dict['title'][:50] + '...'
    i_dict['details'] = i_dict['details'][:100] + '...'
    master_arr_of_dicts.append(i_dict)
  page_dict['master_arr_of_dicts'] = master_arr_of_dicts
  # ------------------------ get all blogs end ------------------------
  return render_template('polling/exterior/blog/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_exterior.route('/polling/blog/<i_blog_post_title>')
@polling_views_exterior.route('/polling/blog/<i_blog_post_title>/')
def polling_i_blog_page_function(i_blog_post_title=None):
  # ------------------------ page dict start ------------------------
  page_dict = {}
  # ------------------------ page dict end ------------------------
  if i_blog_post_title == None or i_blog_post_title == '':
    return redirect(url_for('polling_views_exterior.polling_all_blogs_function'))
  try:
    # ------------------------ replace hyphen start ------------------------
    i_blog_post_title = i_blog_post_title.replace('-',' ')
    # ------------------------ replace hyphen end ------------------------
    blog_obj = BlogPollingObj.query.filter_by(title=i_blog_post_title).first()
    if blog_obj == None or blog_obj == '':
      return redirect(url_for('polling_views_exterior.polling_all_blogs_function'))
    else:
      page_dict['blog_dict'] = arr_of_dict_all_columns_single_item_function(blog_obj)
      page_dict['blog_dict']['created_timestamp_date'] = page_dict['blog_dict']['created_timestamp'].date()
  except:
    return redirect(url_for('polling_views_exterior.polling_all_blogs_function'))
  current_blog_post_num_full_string = f'polling/exterior/blog/blogs_by_id/{blog_obj.id}.html'
  return render_template(current_blog_post_num_full_string, page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_exterior.route('/polling/privacy')
@polling_views_exterior.route('/polling/privacy/')
def polling_privacy_function():
  return render_template('polling/exterior/privacy/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_exterior.route('/polling/terms')
@polling_views_exterior.route('/polling/terms/')
def polling_terms_function():
  return render_template('polling/exterior/tos/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_exterior.route('/polling/about')
@polling_views_exterior.route('/polling/about/')
def polling_about_function():
  return render_template('polling/exterior/about/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_exterior.route('/polling/faq')
@polling_views_exterior.route('/polling/faq/')
def polling_faq_function():
  return render_template('polling/exterior/faq/index.html')
# ------------------------ individual route end ------------------------
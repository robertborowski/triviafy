# ------------------------ imports start ------------------------
import os, time
import datetime
from flask import Flask, session, render_template
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
# ------------------------ imports end ------------------------


# ------------------------ __init__ function start ------------------------
def create_app_function():
  localhost_print_function('=========================================== create_app_function START ===========================================')
  # ------------------------ app setup start ------------------------
  # ------------------------ set timezone start ------------------------
  # Set the timezone of the application when user creates account is will be in US/Easterm time
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  # ------------------------ set timezone end ------------------------
  # ------------------------ create flask app start ------------------------
  # Flask constructor
  app = Flask(__name__)
  # To use a session, there has to be a secret key. The string should be something difficult to guess
  app.secret_key = os.urandom(64)
  # Set session variables to perm so that user can remain signed in for x days
  app.permanent_session_lifetime = datetime.timedelta(days=30)
  # ------------------------ create flask app end ------------------------
  # ------------------------ additional flask app configurations start ------------------------
  # For removing cache from images for quiz questions. The URL was auto caching and not updating
  app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
  # ------------------------ additional flask app configurations end ------------------------
  # ------------------------ Handleing Error Messages START ------------------------
  @app.errorhandler(404)
  # inbuilt function which takes error as parameter
  def not_found(e):
    localhost_print_function('exception hit create_app_function')
    localhost_print_function('=========================================== create_app_function END ===========================================')
    return render_template("error_404_page_templates/index.html")
    # ------------------------ Handleing Error Messages END ------------------------
  # ------------------------ app setup end ------------------------
  localhost_print_function('=========================================== create_app_function END ===========================================')
  return app
# ------------------------ __init__ function end ------------------------
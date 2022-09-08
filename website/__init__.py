# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os, time
from os import path
import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== website __init__ START ===========================================')
# ------------------------ define/initialize a new db sql_alchemy function start ------------------------
# what is SQLAlchemy: https://www.youtube.com/watch?v=6k6NxFyKKQo&ab_channel=Treehouse
# transfers data stored in a SQL database into python objects. (models.py file)
# Use python code to the read, create, delete, update the objects as well as the SQL database at the same time. 
# Instead of writing SQL scripts every step of the way.
# Result: No SQL is needed to create, maintain, and query the db! ORM: Object Relational Mapping 
# and you can connect it directly to Postgres
db = SQLAlchemy()
# DB_NAME = 'triviafy_candidates_sqlalchemy_database.db'
DB_NAME = os.environ.get('DATABASE_URL')
# ------------------------ define/initialize a new db sql_alchemy function end ------------------------


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
  # use sqlalchemy to point to the correct db (postgres)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
  db.init_app(app)
  # ------------------------ create flask app end ------------------------
  # ------------------------ additional flask app configurations start ------------------------
  # Set session variables to perm so that user can remain signed in for x days
  app.permanent_session_lifetime = datetime.timedelta(days=30)
  # For removing cache from images for quiz questions. The URL was auto caching and not updating
  app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
  # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  # ------------------------ additional flask app configurations end ------------------------
  # ------------------------ Handleing Error Messages START ------------------------
  @app.errorhandler(404)
  # inbuilt function which takes error as parameter
  def not_found(e):
    # localhost_print_function('exception hit create_app_function')
    # localhost_print_function('=========================================== create_app_function END ===========================================')
    return render_template("candidates_page_templates/not_logged_in_page_templates/error_404_page_templates/index.html")
  # ------------------------ Handleing Error Messages END ------------------------
  # ------------------------ views/auths/routes imports start ------------------------
  from .views import views
  from .auth import auth
  # ------------------------ views/auths/routes imports end ------------------------
  # ------------------------ views/auths/routes register blueprints start ------------------------
  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  # ------------------------ views/auths/routes register blueprints end ------------------------
  # ------------------------ import models before creating db for first time start ------------------------
  from .models import CandidatesUserObj
  create_database_function(app)
  # ------------------------ import models before creating db for first time end ------------------------
  # ------------------------ login manager start ------------------------
  login_manager = LoginManager()
  login_manager.login_view = 'auth.candidates_login_page_function'   # where does the person go if they are not logged in -> auth.login route
  login_manager.init_app(app)
  # ------------------------ function start ------------------------
  @login_manager.user_loader
  def load_user(id):
    localhost_print_function('def load_user function hit')
    # ------------------------ list user dict directly from postgres start ------------------------
    # logged_in_user_dict = CandidatesUserObj.query.get(id).__dict__
    # print(logged_in_user_dict['first_name'])
    # ------------------------ list user dict directly from postgres end ------------------------
    localhost_print_function('=========================================== create_app_function END ===========================================')
    return CandidatesUserObj.query.get(id)  # when you write query.get -> .get: automatically knows it is looking through the primary key in sqlite
  # ------------------------ function end ------------------------
  # ------------------------ login manager end ------------------------
  # ------------------------ app setup end ------------------------
  localhost_print_function('returning app')
  localhost_print_function('=========================================== create_app_function END ===========================================')
  return app
# ------------------------ __init__ function end ------------------------


# ------------------------ create_db_function start ------------------------
def create_database_function(app):
  localhost_print_function('=========================================== create_database_function START ===========================================')
  if not path.exists('website/' + DB_NAME):
    db.create_all(app=app)
    print('Created database!')
  else:
    print('Database already exists!')
    pass
  localhost_print_function('=========================================== create_database_function END ===========================================')
# ------------------------ create_db_function end ------------------------
localhost_print_function('=========================================== website __init__ END ===========================================')
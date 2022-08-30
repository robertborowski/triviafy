# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -Note: any pages related to authentication will not be in this file, they will be routed in the auth.py file.
# ------------------------ info about this file end ------------------------


# ------------------------ imports start ------------------------
from flask import Blueprint
# ------------------------ imports end ------------------------


# ------------------------ function start ------------------------
auth = Blueprint('auth', __name__)
# ------------------------ function end ------------------------


# ------------------------ individual route start ------------------------
@auth.route('/login')
def login_function():
  return "<h1>Login</h1>"
# ------------------------ individual route end ------------------------


# ------------------------ individual route start ------------------------
@auth.route('/logout')
def logout_function():
  return "<h1>Logout</h1>"
# ------------------------ individual route end ------------------------


# ------------------------ individual route start ------------------------
@auth.route('/sign-up')
def sign_up_function():
  return "<h1>Sign Up</h1>"
# ------------------------ individual route end ------------------------
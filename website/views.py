# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -Note: any pages related to authentication will not be in this file, they will be routed in the auth.py file.
# ------------------------ info about this file end ------------------------


# ------------------------ imports start ------------------------
from flask import Blueprint, render_template
from flask_login import login_required, current_user
# ------------------------ imports end ------------------------


# ------------------------ function start ------------------------
views = Blueprint('views', __name__)
# ------------------------ function end ------------------------


# ------------------------ individual route start ------------------------
@views.route('/')
@login_required   # this decorator says that url cannot be accessed unless the user is logged in.
def home_function():
  return render_template('home.html', user=current_user)
# ------------------------ individual route end ------------------------
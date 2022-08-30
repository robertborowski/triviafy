# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -Note: any pages related to authentication will not be in this file, they will be routed in the auth.py file.
# ------------------------ info about this file end ------------------------


# ------------------------ imports start ------------------------
from flask import Blueprint
# ------------------------ imports end ------------------------


# ------------------------ function start ------------------------
views = Blueprint('views', __name__)

@views.route('/')
def home():
  return "<h1>Test</h1>"
# ------------------------ function end ------------------------
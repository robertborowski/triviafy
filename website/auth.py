# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -Note: any pages related to authentication will not be in this file, they will be routed in the auth.py file.
# ------------------------ info about this file end ------------------------


# ------------------------ imports start ------------------------
from flask import Blueprint, render_template, request, flash
# ------------------------ imports end ------------------------


# ------------------------ function start ------------------------
auth = Blueprint('auth', __name__)
# ------------------------ function end ------------------------


# ------------------------ individual route start ------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login_function():
  return render_template('login.html')
# ------------------------ individual route end ------------------------


# ------------------------ individual route start ------------------------
@auth.route('/logout')
def logout_function():
  return "<h1>Logout</h1>"
# ------------------------ individual route end ------------------------


# ------------------------ individual route start ------------------------
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up_function():
  if request.method == 'POST':
    email = request.form.get('email')
    firstName = request.form.get('firstName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if len(email) < 4:
      flash('Email must be greater than 3 characters.', category='error')
    elif len(firstName) < 2:
      flash('First name must be greater than 1 character.', category='error')
    elif password1 != password2:
      flash('Passwords don\'t match.', category='error')
    elif len(password1) < 7:
      flash('Password must be at least 7 characters.', category='error')
    else:
      flash('Account created!', category='success')
      pass

  return render_template('sign_up.html')
# ------------------------ individual route end ------------------------
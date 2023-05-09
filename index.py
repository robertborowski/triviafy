# ------------------------ imports start ------------------------
# ------------------------ TRIVIAFY CANDIDATES START ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website import create_app_function
import os
# ------------------------ TRIVIAFY CANDIDATES END ------------------------
# ------------------------ imports end ------------------------

# ------------------------ app start ------------------------
# ------------------------ TRIVIAFY CANDIDATES START ------------------------
app = create_app_function()
# ------------------------ TRIVIAFY CANDIDATES END ------------------------
# ------------------------ app end ------------------------

# =========================================================================================================== Run app
# ------------------------ call app directly start ------------------------
if __name__ == '__main__':
  """
  # ------------------------ youtube app configs start ------------------------
  # debug = True means that each time we make a change to our python code it will automatically rerun the webserver.
  localhost_print_function(' --- about to run app --- ')
  localhost_print_function('=========================================== if __name__ == "__main__": END ===========================================')
  app.run(debug=True)
  # ------------------------ youtube app configs emd ------------------------
  """
  # ------------------------ additional configs start ------------------------
  # Check environment variable that was passed in from user on the command line, assume false
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
  # ------------------------ additional configs end ------------------------
# ------------------------ call app directly end ------------------------
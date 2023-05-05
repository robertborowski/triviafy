# -------------------------------------------------------------- Imports
from datetime import datetime
import os, time
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main
def create_timestamp_function():
  # localhost_print_function('=========================================== create_timestamp_function START ===========================================')
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  # localhost_print_function('=========================================== create_timestamp_function END ===========================================')
  return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
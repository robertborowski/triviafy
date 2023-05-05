# -------------------------------------------------------------- Imports
import uuid
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main
def create_uuid_function(table_prefix):
  # localhost_print_function('=========================================== create_uuid_function START ===========================================')
  # localhost_print_function('=========================================== create_uuid_function END ===========================================')
  return table_prefix + str(uuid.uuid4())
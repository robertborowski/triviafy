# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def postgres_close_connection_to_database_function(postgres_connection, postgres_cursor):
  localhost_print_function(' ------------------------ postgres_close_connection_to_database_function START ------------------------ ')

  postgres_cursor.close()
  postgres_connection.close()
  
  localhost_print_function(' ------------------------ postgres_close_connection_to_database_function END ------------------------ ')
# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
import os
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def postgres_connect_to_database_function():
  localhost_print_function('=========================================== postgres_connect_to_database_function START ===========================================')

  # Heroku Postgres connection
  DATABASE_URL = os.environ.get('HEROKU_POSTGRESQL_PURPLE_URL')
  postgres_connection = psycopg2.connect(DATABASE_URL, sslmode='require')
  postgres_cursor = postgres_connection.cursor()

  localhost_print_function('=========================================== postgres_connect_to_database_function END ===========================================')
  return postgres_connection, postgres_cursor
  
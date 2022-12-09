# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from jobs.candidates.db_cleanup_jobs import job_candidates_remove_unsub_user_all_tables_function, job_candidates_clean_out_redis_function
from jobs.candidates.email_jobs import job_candidates_email_all_collected_emails_function, job_candidates_email_all_users_function, job_candidates_send_article_to_all_users_function
# ------------------------ imports end ------------------------

# ------------------------ main start ------------------------
def job_caller_function():
  localhost_print_function('=========================================== job_caller_function START ===========================================')
  # ------------------------ Connect to Postgres DB START ------------------------
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ Connect to Postgres DB END ------------------------

  # ------------------------ remove users start ------------------------
  # job_candidates_remove_unsub_user_all_tables_function(postgres_connection, postgres_cursor)
  # job_candidates_clean_out_redis_function(postgres_connection, postgres_cursor)
  # ------------------------ remove users end ------------------------

  # ------------------------ send emails start ------------------------
  # job_candidates_email_all_collected_emails_function(postgres_connection, postgres_cursor)
  # job_candidates_email_all_users_function(postgres_connection, postgres_cursor)
  # job_candidates_send_article_to_all_users_function(postgres_connection, postgres_cursor)
  # ------------------------ send emails end ------------------------

  # ------------------------ Close Postgres DB START ------------------------
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ Close Postgres DB END ------------------------
  localhost_print_function('=========================================== job_caller_function END ===========================================')
  return True
# ------------------------ main end ------------------------

# ------------------------ run main start ------------------------
if __name__ == "__main__":
  job_caller_function()
# ------------------------ run main end ------------------------
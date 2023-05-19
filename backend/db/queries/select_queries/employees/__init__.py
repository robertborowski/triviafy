# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import psycopg2
from psycopg2 import Error, extras
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def select_manual_function(postgres_connection, postgres_cursor, tag_query_to_use, additional_input=None, additional_input2=None, additional_input3=None):
  # localhost_print_function(' ------------------------ select_manual_function start ------------------------ ')
  # ------------------------ select queries start ------------------------
  select_queries_dict = {
    'select_groups_1':
      f"SELECT \
          fk_company_name, \
          public_group_id \
        FROM \
          group_obj;",
    'select_groups_2':
      f"SELECT \
          DISTINCT company_name, \
          group_id \
        FROM \
          user_obj \
        ORDER BY \
          company_name;",
    'select_groups_3':
      f"SELECT \
          * \
        FROM \
          group_obj;",
    'select_group_settings_1':
      f"SELECT \
          * \
        FROM \
          activity_a_settings_obj \
        WHERE \
          product='trivia' AND \
          fk_group_id='{additional_input}';",
    'select_group_settings_2':
      f"SELECT \
          * \
        FROM \
          activity_a_settings_obj \
        WHERE \
          product='{additional_input2}' AND \
          fk_group_id='{additional_input}';",
    'select_latest_test_1':
      f"SELECT \
          * \
        FROM \
          activity_a_test_obj \
        WHERE \
          fk_group_id='{additional_input}' \
        ORDER BY \
          created_timestamp DESC \
        LIMIT 1;",
    'select_latest_test_2':
      f"SELECT \
          * \
        FROM \
          activity_a_test_obj \
        WHERE \
          fk_group_id='{additional_input}' \
          AND product='{additional_input2}' \
        ORDER BY \
          created_timestamp DESC \
        LIMIT 1;",
    'select_user_emails_1':
      f"SELECT \
          id, \
          email \
        FROM \
          user_obj \
        WHERE \
          company_name='{additional_input}';",
    'select_user_emails_2':
      f"SELECT \
          id, \
          email \
        FROM \
          user_obj \
        WHERE \
          group_id='{additional_input}';",
    'select_test_graded_1':
      f"SELECT \
          created_timestamp, fk_group_id, fk_user_id, fk_test_id, total_questions, correct_count, final_score, status, graded_count \
        FROM \
          activity_a_test_graded_obj \
        WHERE \
          fk_user_id='{additional_input}' AND \
          fk_test_id='{additional_input2}' AND \
          status='complete';",
    'select_check_email_sent_1':
      f"SELECT \
          * \
        FROM \
          email_sent_obj \
        WHERE \
          to_email='{additional_input}' AND \
          subject='{additional_input2}';",
    'select_latest_test_winner_1':
      f"SELECT \
          MAX(final_score) AS max_score, \
          fk_user_id, \
          created_timestamp \
        FROM \
          activity_a_test_graded_obj \
        WHERE \
          fk_test_id='{additional_input}' AND \
          status='complete' \
        GROUP BY \
          fk_user_id, \
          created_timestamp \
        ORDER BY \
          MAX(final_score) DESC, \
          created_timestamp \
        LIMIT 1;",
    'select_user_1':
      f"SELECT \
          email, \
          company_name \
        FROM \
          user_obj \
        WHERE \
          id='{additional_input}';",
    'select_categories_v1':
      f"SELECT \
          categories \
        FROM \
          activity_a_created_questions_obj \
        WHERE \
          product='employees';",
    'select_letter_count_v1':
      f"SELECT 'A' AS letter, COUNT(*) AS total_count FROM activity_a_created_questions_obj WHERE product = 'employees' AND answer LIKE 'A,%' \
        UNION \
        SELECT 'B' AS letter, COUNT(*) AS total_count FROM activity_a_created_questions_obj WHERE product = 'employees' AND answer LIKE 'B,%' \
        UNION \
        SELECT 'C' AS letter, COUNT(*) AS total_count FROM activity_a_created_questions_obj WHERE product = 'employees' AND answer LIKE 'C,%' \
        UNION \
        SELECT 'D' AS letter, COUNT(*) AS total_count FROM activity_a_created_questions_obj WHERE product = 'employees' AND answer LIKE 'D,%';"
  }
  # ------------------------ select queries end ------------------------
  # ------------------------ cursor start ------------------------
  cursor = postgres_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cursor.execute(select_queries_dict[tag_query_to_use])
  # ------------------------ cursor end ------------------------
  # ------------------------ results start ------------------------
  results_arr = cursor.fetchall()
  result_arr_dicts = []
  for row in results_arr:
    result_arr_dicts.append(dict(row))
  # ------------------------ results end ------------------------
  # localhost_print_function(' ------------------------ select_manual_function end ------------------------ ')
  return result_arr_dicts
# ------------------------ individual function end ------------------------
# -------------------------------------------------------------- Imports
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.db.queries.select_queries.select_queries_triviafy_all_questions_table.select_triviafy_category_count_totals import select_triviafy_category_count_totals_function
import pandas as pd

# -------------------------------------------------------------- Main Function
def job_check_category_count_totals_function():
  localhost_print_function('=========================================== job_check_category_count_totals_function START ===========================================')

  # ------------------------ DB Conection START ------------------------
  # Connect to Postgres database
  postgres_connection, postgres_cursor = postgres_connect_to_database_function()
  # ------------------------ DB Conection End ------------------------


  # ------------------------ Get Data START ------------------------
  category_count_totals_arr = select_triviafy_category_count_totals_function(postgres_connection, postgres_cursor)
  # ------------------------ Get Data END ------------------------


  # ------------------------ Sort Data START ------------------------
  category_count_dict = {}
  for i in category_count_totals_arr:
    categories_string = i[0]
    category_count = i[1]

    categories_list = categories_string.split(', ')
    for category in categories_list:
      if category not in category_count_dict:
        category_count_dict[category] = category_count
      else:
        category_count_dict[category] += category_count

  df = pd.DataFrame.from_dict(category_count_dict, orient='index', columns=['count_col'])
  df.index.name = 'category'
  df = df.reset_index()
  # df.rename(columns={0: 'count_col'}, inplace=True)
  df = df.sort_values(by='count_col', ascending=False)
  print(df)

  # ------------------------ Sort Data END ------------------------


  # ------------------------ DB Close Conection START ------------------------
  # Close postgres db connection
  postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
  # ------------------------ DB Close Conection END ------------------------

  localhost_print_function('=========================================== job_check_category_count_totals_function END ===========================================')
  return True


# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  job_check_category_count_totals_function()
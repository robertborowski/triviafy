# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website import db
# ------------------------ imports end ------------------------


localhost_print_function('=========================================== sql_statements_select __init__ START ===========================================')
# ------------------------ select queries start ------------------------
select_queries_dict = {
  'select_if_capacity_chosen': {
    'raw_query': 'SELECT * FROM candidates_user_obj WHERE email >= :val',
    'input_args': {'val': 'a@a.com'}
  }
}
# ------------------------ select queries end ------------------------

# ------------------------ individual function start ------------------------
def select_general_function():
  localhost_print_function('=========================================== select_general_function START ===========================================')
  # ------------------------ actual query start ------------------------
  # result_obj = db.session.execute('SELECT * FROM candidates_user_obj WHERE email = :val', {'val': 'a@a.com'})
  result_obj = db.session.execute(select_queries_dict['select_if_capacity_chosen']['raw_query'], select_queries_dict['select_if_capacity_chosen']['input_args'])
  # ------------------------ actual query end ------------------------
  # ------------------------ default result start ------------------------
  result_arr_of_dicts = []
  # ------------------------ default result end ------------------------
  # ------------------------ existing result start ------------------------
  for i_row in result_obj:
    result_dict = dict(i_row.items()) # convert to dict keyed by column names
    result_arr_of_dicts.append(result_dict)
  # ------------------------ existing result end ------------------------
  localhost_print_function('=========================================== select_general_function START ===========================================')
  return result_arr_of_dicts
# ------------------------ individual function end ------------------------
localhost_print_function('=========================================== sql_statements_select __init__ END ===========================================')
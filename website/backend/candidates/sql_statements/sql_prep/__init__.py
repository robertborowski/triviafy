# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def prepare_where_clause_function(desired_langs_str):
  where_clause_arr = []
  desired_langs_arr = desired_langs_str.split(',')
  master_where_statement = ''
  for i in range(len(desired_langs_arr)):
    if i == (len(desired_langs_arr) - 1):
      master_where_statement += f"(categories LIKE '%{desired_langs_arr[i]}%')"
    else:
      master_where_statement += f"(categories LIKE '%{desired_langs_arr[i]}%') OR "
  where_clause_arr.append(master_where_statement)
  return where_clause_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def prepare_question_ids_where_clause_function(db_assessment_obj):
  # ------------------------ where clause start ------------------------
  question_ids_str =  db_assessment_obj.question_ids_arr
  question_ids_arr = question_ids_str.split(',')
  question_ids_str = "','".join(question_ids_arr)
  question_ids_str = "'" + question_ids_str + "'"
  # ------------------------ where clause end ------------------------
  return question_ids_str
# ------------------------ individual function end ------------------------
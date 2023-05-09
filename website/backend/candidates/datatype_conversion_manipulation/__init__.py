# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def one_col_dict_to_arr_function(input_arr_of_dicts):
  """
  This function is for only for the results of ONE column. Example: "SELECT id FROM table" this will return arr of dicts, one dict for each row. So this function converts that into an array.
  """
  output_arr = []
  for i in input_arr_of_dicts:
    for k, v in i.items():
      output_arr.append(v)
  return output_arr
# ------------------------ individual function end ------------------------
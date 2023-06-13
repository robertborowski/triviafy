# ------------------------ imports start ------------------------
from datetime import datetime
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def arr_of_dict_all_columns_single_item_function(sql_obj, for_json_dumps=False):
  current_dict = {}
  for c in sql_obj.__table__.columns:
    current_value = getattr(sql_obj, c.name)
    if for_json_dumps == True:
      if isinstance(current_value, datetime):
        current_value = str(current_value)
    current_dict[c.name] = current_value
  return current_dict
# ------------------------ individual function end ------------------------
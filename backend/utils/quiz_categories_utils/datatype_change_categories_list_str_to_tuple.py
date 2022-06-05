# -------------------------------------------------------------- Imports
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def datatype_change_categories_list_str_to_tuple_function(categories_str):
  localhost_print_function('=========================================== datatype_change_categories_list_str_to_tuple_function START ===========================================')

  try:
    # Words for user html tuple Start
    # Assign variables
    categories_str_fixed = categories_str.replace(', ',',')
    categories_arr = categories_str_fixed.split(',')
    
    # Loop and separate
    categories_arr_to_html = []
    for category in categories_arr:
      category_lower = category.lower()
      category_replace_space = category_lower.replace(' ','_')
      categories_arr_to_html.append((category, category_replace_space))
  
  except:
    print('Error here: datatype_change_categories_list_str_to_tuple_function except statement...')
    return False
  
  localhost_print_function('=========================================== datatype_change_categories_list_str_to_tuple_function END ===========================================')
  return categories_arr_to_html
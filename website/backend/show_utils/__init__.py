# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.get_create_obj import get_show_based_on_id_function
from website.backend.dict_manipulation import arr_of_dict_all_columns_single_item_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def shows_following_arr_of_dict_function(page_dict):
  if page_dict['shows_following_arr_of_dict'] != None:
    shows_arr_of_dict = []
    for i_obj in page_dict['shows_following_arr_of_dict']:
      show_obj = get_show_based_on_id_function(i_obj.fk_show_id)
      # ------------------------ if following show that has been deleted start ------------------------
      if show_obj == None:
        continue
      # ------------------------ if following show that has been deleted end ------------------------
      show_dict = arr_of_dict_all_columns_single_item_function(show_obj)
      show_dict['description'] = show_dict['description'][0:150] + '...'
      shows_arr_of_dict.append(show_dict)
    sorted_shows_arr_of_dict = sorted(shows_arr_of_dict, key=lambda x: x['name'])
    page_dict['shows_following_arr_of_dict'] = sorted_shows_arr_of_dict
  return page_dict
# ------------------------ individual function end ------------------------
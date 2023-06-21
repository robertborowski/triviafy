# ------------------------ imports start ------------------------
from website.models import UserSignupFeedbackObj, UserAttributesObj
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_poll_statistics(page_dict):
  print(' ------------- 20 ------------- ')
  print(f"page_dict | type: {type(page_dict)} | {page_dict}")
  print(' ------------- 20 ------------- ')
  page_dict['testing_value'] = 'hello thank you!'
  return page_dict
# ------------------------ individual function end ------------------------
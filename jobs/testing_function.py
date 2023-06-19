# ------------------------ imports start ------------------------
import os, time
# ------------------------ imports end ------------------------

# ------------------------ set timezone start ------------------------
# Set the timezone of the application when user creates account is will be in US/Easterm time
os.environ['TZ'] = 'US/Eastern'
time.tzset()
# ------------------------ set timezone end ------------------------

# ------------------------ individual function start ------------------------
def run_function():
  print(' -------------------------- 000 start -------------------------- ')
  counter = 0
  while counter < 10:
    counter += 1
    print(f'status counter: {counter}')
    time.sleep(10)
  print(' -------------------------- 000 end -------------------------- ')
  
  try:
    print(' -------------------------- 001 -------------------------- ')
    print('starting to wait')
    time.sleep(60)
    print('done waiting 60 seconds')
    print(' -------------------------- 002 -------------------------- ')
  except:
    print(' -------------------------- error -------------------------- ')
  return True
# ------------------------ individual function end ------------------------

# ------------------------ run function start ------------------------
if __name__ == "__main__":
  run_function()
# ------------------------ run function end ------------------------
# -------------------------------------------------------------- Imports
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
# def send_team_channel_message_quiz_open_function(slack_bot_token, user_channel, quiz_end_day_of_week, quiz_end_time, user_slack_authed_incoming_webhook_url):
def send_team_channel_message_quiz_open_function(quiz_end_day_of_week, quiz_end_time, user_slack_authed_incoming_webhook_url, quiz_channel_name):
  
  """
  # ------------------------ Old Method START ------------------------
  localhost_print_function('=========================================== send_team_channel_message_quiz_open_function START ===========================================')

  output_text = f":tada: Hi <!here>, your team's weekly Triviafy quiz is now OPEN!\n:hourglass_flowing_sand: Quiz closes on {quiz_end_day_of_week}, {quiz_end_time}.\n:white_check_mark: Login and submit your answers at: https://triviafy.com/employees"

  # Set up client with the USER's Bot Access Token. NOT your's from the environment variable
  client = WebClient(token=slack_bot_token)
  # Have the bot send a test message to the channel
  try:
    response = client.chat_postMessage(
      channel=user_channel,
      text=output_text
    )
    localhost_print_function('sent slack message')
  except SlackApiError as e:
    localhost_print_function('did not send message to slack channel')
    print(e.response['error'])

  localhost_print_function('=========================================== send_team_channel_message_quiz_open_function END ===========================================')
  return True, output_text
  # ------------------------ Old Method END ------------------------
  """


  # ------------------------ Incoming Webhook Method START ------------------------
  localhost_print_function('=========================================== send_team_channel_message_quiz_open_function START ===========================================')
  from slack_sdk.webhook import WebhookClient
  url = user_slack_authed_incoming_webhook_url
  webhook = WebhookClient(url)

  output_text = f":tada: Hi <!here>, your team's weekly Triviafy quiz is now OPEN!\n:hourglass_flowing_sand: Quiz closes on {quiz_end_day_of_week}, {quiz_end_time}.\n:white_check_mark: Login and submit your answers at: https://triviafy.com/employees\n:woman-raising-hand: New to Triviafy? In order to participate in the weekly Triviafy quiz each team member go to https://triviafy.com/employees > Create Account > Add To Slack > Select Channel: '{quiz_channel_name}'"

  response = webhook.send(text=output_text)
  #assert response.status_code == 200
  #assert response.body == "ok"

  localhost_print_function('=========================================== send_team_channel_message_quiz_open_function END ===========================================')
  return output_text
  # ------------------------ Incoming Webhook Method END ------------------------
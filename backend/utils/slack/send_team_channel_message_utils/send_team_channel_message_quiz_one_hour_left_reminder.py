# -------------------------------------------------------------- Imports
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def send_team_channel_message_quiz_one_hour_left_reminder_function(quiz_channel_name, quiz_end_time, user_slack_authed_incoming_webhook_url):

  # ------------------------ Incoming Webhook Method START ------------------------
  localhost_print_function('=========================================== send_team_channel_message_quiz_one_hour_left_reminder_function START ===========================================')
  from slack_sdk.webhook import WebhookClient
  url = user_slack_authed_incoming_webhook_url
  webhook = WebhookClient(url)

  output_text = f":hourglass_flowing_sand: Hi <!here>, your team's weekly Triviafy quiz closes TODAY at {quiz_end_time} (less than 1 hour)!\n:pencil2: Login and submit your answers at: https://triviafy.com/employees\n:woman-raising-hand: New to Triviafy? In order to participate in the weekly Triviafy quiz each team member go to https://triviafy.com/employees > Create Account > Add To Slack > Select Channel: '{quiz_channel_name}'"

  response = webhook.send(text=output_text)
  #assert response.status_code == 200
  #assert response.body == "ok"

  localhost_print_function('=========================================== send_team_channel_message_quiz_one_hour_left_reminder_function END ===========================================')
  return output_text
  # ------------------------ Incoming Webhook Method END ------------------------
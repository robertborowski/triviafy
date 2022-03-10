# -------------------------------------------------------------- Imports
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def send_team_channel_message_skipped_quiz_feedback_function(quiz_channel_name, skipped_quiz_count_int, user_slack_authed_incoming_webhook_url):

  # ------------------------ Incoming Webhook Method START ------------------------
  localhost_print_function('=========================================== send_team_channel_message_skipped_quiz_feedback_function START ===========================================')
  from slack_sdk.webhook import WebhookClient
  url = user_slack_authed_incoming_webhook_url
  webhook = WebhookClient(url)

  output_text = f"\n:red_circle:     :red_circle:     :red_circle:     :red_circle:     :red_circle:\n.\n.\n.\n*Cancel Free Trial Period:* If you want to stop receiving emails/Slack messages from Triviafy (end your team's free trial period early), then please email 'robert@triviafy.com' with word 'cancel'.\n.\n.\nHi <!here>\nYour team's Slack channel '{quiz_channel_name}' has skipped {skipped_quiz_count_int} Triviafy quizzes.\nWhy is no one on your team participating? *See Latest Quiz:* triviafy.com > Login > Sign in With Slack.\nAny feedback about our product would be greatly appreciated (email: 'robert@triviafy.com').\n.\n.\n*Cancel Free Trial Period:* If you want to stop receiving emails/Slack messages from Triviafy (end your team's free trial period early), then please email 'robert@triviafy.com' with word 'cancel'.\n.\n.\n.\n:red_circle:     :red_circle:     :red_circle:     :red_circle:     :red_circle:"

  response = webhook.send(text=output_text)
  #assert response.status_code == 200
  #assert response.body == "ok"

  localhost_print_function('=========================================== send_team_channel_message_skipped_quiz_feedback_function END ===========================================')
  return output_text
  # ------------------------ Incoming Webhook Method END ------------------------
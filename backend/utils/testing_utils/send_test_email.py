# -------------------------------------------------------------- Imports
import os
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def send_test_email_function():
  localhost_print_function('=========================================== send_test_email_function START ===========================================')
  
  # ------------------------ Test 1 START ------------------------
  # message = Mail(
  #   from_email='support@triviafy.com',
  #   name='Triviafy',
  #   to_emails='rborowski141@gmail.com',
  #   subject='Testing Send Grid2',
  #   html_content='Hello World!')
  # try:
  #   sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY_TRIVIAFY'))
  #   response = sg.send(message)
  #   localhost_print_function(response.status_code)
  #   localhost_print_function(response.body)
  #   localhost_print_function(response.headers)
  # except Exception as e:
  #   localhost_print_function(e.message)
  # ------------------------ Test 1 END ------------------------



  # ------------------------ Test 2 START ------------------------
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY_TRIVIAFY'))
  from_email = Email(email = "support@triviafy.com", name = "TRIVIAFY")  # Change to your verified sender
  to_email = To('rborowski141@gmail.com')  # Change to your recipient
  subject = "Test Email 2"
  content = Content("text/plain","Hi this is a test/n/nHow are you doing on this fine day?")
  mail = Mail(from_email, to_email, subject, content)

  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()

  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)
  try:
    sg.client.mail.send.post(request_body=mail_json)
    localhost_print_function('email sent successfully!')
  except:
    localhost_print_function('email did not send successfully...')
  # ------------------------ Test 2 END ------------------------

  localhost_print_function('=========================================== send_test_email_function END ===========================================')
  return True

# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  send_test_email_function()
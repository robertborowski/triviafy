# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# ------------------------ main start ------------------------
def send_email_test_function():
    message = Mail(
        from_email='support@triviafy.com',
        to_emails='robjborowski@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY_TRIVIAFY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)



# ------------------------ run main start ------------------------
if __name__ == "__main__":
    send_email_test_function()
# ------------------------ run main end ------------------------
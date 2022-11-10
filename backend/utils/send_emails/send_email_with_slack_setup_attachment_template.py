# -------------------------------------------------------------- Imports
import os
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition, ContentId
import base64
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def send_email_with_slack_setup_attachment_template_function(output_email, output_subject_line, output_message_content):
  localhost_print_function('=========================================== send_email_with_slack_setup_attachment_template_function START ===========================================')
 
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY_TRIVIAFY'))
  from_email = Email(email = os.environ.get('TRIVIAFY_SUPPORT_EMAIL'), name = "Triviafy")  # Change to your verified sender
  to_email = To(output_email)  # Change to your recipient
  subject = output_subject_line
  content = Content("text/plain", output_message_content)
  mail = Mail(from_email, to_email, subject, content)

  file_path = 'website/static/images/employee_engagement/pdfs/PDFTriviafySlackSetupGuide.pdf'
  with open(file_path, 'rb') as f:
      data = f.read()
      f.close()
  encoded = base64.b64encode(data).decode()
  attachment = Attachment()
  attachment.file_content = FileContent(encoded)
  attachment.file_type = FileType('application/pdf')
  attachment.file_name = FileName('PDFTriviafySlackSetupGuide.pdf')
  attachment.disposition = Disposition('attachment')
  attachment.content_id = ContentId('PDFTriviafySlackSetupGuide Content ID')
  mail.attachment = attachment

  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()


  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)
  try:
    sg.client.mail.send.post(request_body=mail_json)
    localhost_print_function('email sent successfully! ' + output_subject_line + " - To: " + output_email)
  except:
    localhost_print_function('email did not send successfully...' + output_subject_line)
    localhost_print_function('=========================================== send_email_with_slack_setup_attachment_template_function END ===========================================')
    return False

  localhost_print_function('=========================================== send_email_with_slack_setup_attachment_template_function END ===========================================')
  return True
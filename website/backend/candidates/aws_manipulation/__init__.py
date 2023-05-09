
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os
import boto3
from botocore.exceptions import NoCredentialsError
# ------------------------ imports end ------------------------


# ------------------------ individual function start ------------------------
def candidates_change_uploaded_image_filename_function(image, create_question_uploaded_image_uuid):
  # Get the filename
  filename = image.filename

  # Split the filename by '.'
  filename_parts_arr = filename.split('.')

  # Replace the first part of the filename
  filename_parts_arr[0] = create_question_uploaded_image_uuid

  # Join it back together
  filename = ".".join(filename_parts_arr)

  # Assign to the image filename
  image.filename = filename

  return image
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def candidates_allowed_image_filesize_function(filesize, max_image_filesize_value):
  
  if int(filesize) <= max_image_filesize_value:
    return True
  
  else:
    return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def candidates_allowed_images_function(filename, allowed_image_extensions_arr):
  # We only want files with a . in the filename
  if not "." in filename:
    return False

  # Split the extension from the filename
  ext = filename.rsplit(".", 1)[1]

  # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
  if ext.upper() in allowed_image_extensions_arr:
    return True
  
  else:
    return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def candidates_create_question_upload_image_aws_s3_function(image_obj):
  # Env variables
  aws_s3_bucket = os.environ.get('AWS_TRIVIAFY_BUCKET_NAME')
  aws_s3_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
  aws_s3_key_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
  
  s3 = boto3.client("s3",
                    aws_access_key_id = aws_s3_key_id,
                    aws_secret_access_key = aws_s3_key_secret)

  # Try the upload to AWS s3 bucket
  try:
    s3.upload_fileobj(image_obj, aws_s3_bucket, image_obj.filename, ExtraArgs={"ContentType": image_obj.content_type})
    print('image stored in aws s3!')
  except Exception as e:
    # This is a catch all exception, edit this part to fit your needs.
    print('Something Happened: ', e)
    return e
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def candidates_user_upload_image_checks_aws_s3_function(image, file_size):
  # Set the parameters for accepting image upload
  allowed_image_extensions_arr = ["JPEG", "JPG", "PNG", "GIF"]
  max_image_filesize_value = 50 * 1024 * 1024

  # Ensuring the filesize is allowed
  if not candidates_allowed_image_filesize_function(file_size, max_image_filesize_value):
    localhost_print_function('Filesize exceeded maximum limit (50 MB)')
    return False

  # Ensuring the file has a name
  if image.filename == "":
    localhost_print_function('No filename')
    return False

  # Ensuring the file type is allowed
  if candidates_allowed_images_function(image.filename, allowed_image_extensions_arr):
    # werkzeug.secure_filename not working when uploading to AWS
    # filename = secure_filename(image.filename)

    # Put the image object in aws s3
    aws_upload = candidates_create_question_upload_image_aws_s3_function(image)
    return True
  
  else:
    localhost_print_function('That file extension is not allowed')
    return False
# ------------------------ individual function end ------------------------
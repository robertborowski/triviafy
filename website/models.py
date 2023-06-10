# ------------------------ imports start ------------------------
from email.policy import default
from website import db
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from website import secret_key_ref
# ------------------------ imports end ------------------------


# ------------------------ all product models start ------------------------
# ------------------------ individual model start ------------------------
# Note: models vs tables: https://stackoverflow.com/questions/45044926/db-model-vs-db-table-in-flask-sqlalchemy
class UserObj(db.Model, UserMixin):   # Only the users object inherits UserMixin, other models do NOT!
  # ------------------------ general start ------------------------
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150))
  password = db.Column(db.String(150))
  name = db.Column(db.String(150))
  company_name = db.Column(db.String(150))
  group_id = db.Column(db.String(150))
  fk_stripe_customer_id = db.Column(db.String(150))
  # ------------------------ general start ------------------------
  # ------------------------ candidates start ------------------------
  fk_stripe_subscription_id = db.Column(db.String(150))
  # ------------------------ candidates end ------------------------
  # ------------------------ employees start ------------------------
  employees_fk_stripe_subscription_id = db.Column(db.String(150))
  # ------------------------ employees end ------------------------
  verified_email = db.Column(db.Boolean, default=False)
  signup_product = db.Column(db.String(150))
  last_name = db.Column(db.String(150))

  def get_reset_token_function(self, expires_sec=1800):
    serializer_token_obj = Serializer(secret_key_ref, expires_sec)
    return serializer_token_obj.dumps({'dump_load_user_id': self.id}).decode('utf-8')

  @staticmethod
  def verify_reset_token_function(token_to_search_for):
    serializer_token_obj = Serializer(secret_key_ref)
    try:
      dl_user_id_from_token = serializer_token_obj.loads(token_to_search_for)['dump_load_user_id']
    except:
      return None
    return UserObj.query.get(dl_user_id_from_token)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class EmailCollectObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150))
  source = db.Column(db.String(20))
  unsubscribed = db.Column(db.Boolean, default=False)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class EmailDeletedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150), primary_key=True)
  uuid_archive = db.Column(db.String(150), primary_key=True)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ActivityACreatedQuestionsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  status = db.Column(db.Boolean, default=False)
  categories = db.Column(db.String(150))
  title = db.Column(db.String(150))
  question = db.Column(db.String(1000))
  option_a = db.Column(db.String(280))
  option_b = db.Column(db.String(280))
  option_c = db.Column(db.String(280))
  option_d = db.Column(db.String(280))
  option_e = db.Column(db.String(280))
  answer = db.Column(db.String(280))
  aws_image_uuid = db.Column(db.String(150))
  aws_image_url = db.Column(db.String(150))
  submission = db.Column(db.String(20))
  product = db.Column(db.String(50))
  fk_group_id = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ActivityBCreatedQuestionsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  fk_group_id = db.Column(db.String(150))
  question = db.Column(db.String(1000))
  product = db.Column(db.String(50))
  status = db.Column(db.Boolean, default=False)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class StripeCheckoutSessionObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_checkout_session_id = db.Column(db.String(150))
  fk_user_id = db.Column(db.String(150))
  status = db.Column(db.String(20))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class EmailScrapedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150), unique=True)
  unsubscribed = db.Column(db.Boolean, default=False)
# ------------------------ individual model end ------------------------
# ------------------------ all product models end ------------------------

# ------------------------ employees models start ------------------------
# ------------------------ individual model start ------------------------
class GroupObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_company_name = db.Column(db.String(150))
  fk_user_id = db.Column(db.String(150))
  public_group_id = db.Column(db.String(150))
  status = db.Column(db.String(150))
  # ------------------------ products auto on/off start ------------------------
  trivia = db.Column(db.Boolean, default=True)
  picture_quiz = db.Column(db.Boolean, default=False)
  celebrations = db.Column(db.Boolean, default=False)
  icebreakers = db.Column(db.Boolean, default=False)
  surveys = db.Column(db.Boolean, default=False)
  personality_test = db.Column(db.Boolean, default=False)
  this_or_that = db.Column(db.Boolean, default=False)
  most_likely_to = db.Column(db.Boolean, default=False)
  giftcard = db.Column(db.Boolean, default=False)
  # ------------------------ products auto on/off end ------------------------
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ActivityASettingsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_group_id = db.Column(db.String(150))
  fk_user_id = db.Column(db.String(150))
  timezone = db.Column(db.String(150))
  start_day = db.Column(db.String(150))
  start_time = db.Column(db.String(150))
  end_day = db.Column(db.String(150))
  end_time = db.Column(db.String(150))
  cadence = db.Column(db.String(150))
  total_questions = db.Column(db.Integer)
  question_type = db.Column(db.String(150))
  categories = db.Column(db.String(1000))
  product = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ActivityBSettingsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_group_id = db.Column(db.String(150))
  fk_user_id = db.Column(db.String(150))
  timezone = db.Column(db.String(150))
  start_day = db.Column(db.String(150))
  start_time = db.Column(db.String(150))
  end_day = db.Column(db.String(150))
  end_time = db.Column(db.String(150))
  cadence = db.Column(db.String(150))
  product = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ActivityATestObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_group_id = db.Column(db.String(150))
  timezone = db.Column(db.String(150))
  start_day = db.Column(db.String(150))
  start_time = db.Column(db.String(150))
  start_timestamp = db.Column(db.DateTime(timezone=True))
  end_day = db.Column(db.String(150))
  end_time = db.Column(db.String(150))
  end_timestamp = db.Column(db.DateTime(timezone=True))
  cadence = db.Column(db.String(150))
  total_questions = db.Column(db.Integer)
  question_type = db.Column(db.String(150))
  categories = db.Column(db.String(1000))
  question_ids = db.Column(db.String(3000))
  question_types_order = db.Column(db.String(500))
  status = db.Column(db.String(150))
  product = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ActivityBTestObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_group_id = db.Column(db.String(150))
  timezone = db.Column(db.String(150))
  start_day = db.Column(db.String(150))
  start_time = db.Column(db.String(150))
  start_timestamp = db.Column(db.DateTime(timezone=True))
  end_day = db.Column(db.String(150))
  end_time = db.Column(db.String(150))
  end_timestamp = db.Column(db.DateTime(timezone=True))
  cadence = db.Column(db.String(150))
  fk_question_id = db.Column(db.String(150))
  status = db.Column(db.String(150))
  product = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ActivityATestGradedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_group_id = db.Column(db.String(150))
  fk_user_id = db.Column(db.String(150))
  fk_test_id = db.Column(db.String(150))
  total_questions = db.Column(db.Integer)
  correct_count = db.Column(db.Integer)
  final_score = db.Column(db.Float)
  status = db.Column(db.String(20))
  graded_count = db.Column(db.Integer)
  test_obj = db.Column(db.String(180000))
  product = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ActivityBTestGradedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_group_id = db.Column(db.String(150))
  fk_user_id = db.Column(db.String(150))
  fk_test_id = db.Column(db.String(150))
  status = db.Column(db.String(20))
  test_obj = db.Column(db.String(1000))
  product = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ActivityAGroupQuestionsUsedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_group_id = db.Column(db.String(150))
  fk_question_id = db.Column(db.String(150))
  fk_test_id = db.Column(db.String(150))
  product = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ActivityBGroupQuestionsUsedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_group_id = db.Column(db.String(150))
  fk_question_id = db.Column(db.String(150))
  fk_test_id = db.Column(db.String(150))
  product = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class UserDesiredCategoriesObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  user_id_fk = db.Column(db.String(150))
  desired_categories = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class StripePaymentOptionsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  candence = db.Column(db.String(10))
  price = db.Column(db.Float)
  fk_stripe_price_id = db.Column(db.String(150))
  name = db.Column(db.String(20))
  fk_stripe_price_id_testing = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class EmailSentObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  from_user_id_fk = db.Column(db.String(150))
  to_email = db.Column(db.String(150))
  subject = db.Column(db.String(1000))
  body = db.Column(db.String(5000))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class UserFeatureRequestObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  fk_group_id = db.Column(db.String(150))
  feature_requested = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class UserSignupFeedbackObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  fk_email = db.Column(db.String(150))
  question = db.Column(db.String(150))
  response = db.Column(db.String(150))
  fk_group_id = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class UserCelebrateObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  question = db.Column(db.String(150))
  answer = db.Column(db.String(150))
  event = db.Column(db.String(150))
  celebrate_month = db.Column(db.Integer)
  celebrate_day = db.Column(db.Integer)
  celebrate_year = db.Column(db.Integer)
  status = db.Column(db.Boolean, default=False)
  fk_question_id = db.Column(db.String(150))
  fk_test_id = db.Column(db.String(150))
  fk_group_id = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class BlogObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  title = db.Column(db.String(150))
  details = db.Column(db.String(150))
  aws_image_url = db.Column(db.String(150))
# ------------------------ individual model end ------------------------
# ------------------------ employees models end ------------------------
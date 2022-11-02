# ------------------------ imports start ------------------------
from email.policy import default
from website import db
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from website import secret_key_ref
# ------------------------ imports end ------------------------


# ------------------------ models start ------------------------
# ------------------------ individual model start ------------------------
# Note: models vs tables: https://stackoverflow.com/questions/45044926/db-model-vs-db-table-in-flask-sqlalchemy
class CandidatesUserObj(db.Model, UserMixin):   # Only the users object inherits UserMixin, other models do NOT!
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  name = db.Column(db.String(150))
  company_name = db.Column(db.String(150))
  capacity_id_fk = db.Column(db.String(150), default=None)
  fk_stripe_customer_id = db.Column(db.String(150))
  fk_stripe_subscription_id = db.Column(db.String(150))

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
    return CandidatesUserObj.query.get(dl_user_id_from_token)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CandidatesCapacityOptionsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  candence = db.Column(db.String(10))
  price = db.Column(db.Float)
  fk_stripe_price_id = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CandidatesCollectEmailObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CandidatesDesiredLanguagesObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  user_id_fk = db.Column(db.String(150))
  desired_languages = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CandidatesUploadedCandidatesObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  user_id_fk = db.Column(db.String(150))
  candidate_id = db.Column(db.String(150))
  email = db.Column(db.String(150))
  upload_type = db.Column(db.String(15))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CandidatesAssessmentsCreatedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  user_id_fk = db.Column(db.String(150))
  assessment_name = db.Column(db.String(150), unique=True)
  desired_languages_arr = db.Column(db.String(1000))
  total_questions = db.Column(db.Integer)
  delivery_type = db.Column(db.String(150))
  question_ids_arr = db.Column(db.String(1000))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CandidatesRequestLanguageObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  user_id_fk = db.Column(db.String(150))
  desired_languages_str = db.Column(db.String(1000))
  approved_to_view = db.Column(db.Boolean, default=False)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CandidatesScheduleObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  user_id_fk = db.Column(db.String(150))
  assessment_id_fk = db.Column(db.String(150))
  assessment_name = db.Column(db.String(150))
  candidates = db.Column(db.String(150))
  send_date = db.Column(db.String(150))
  send_time = db.Column(db.String(150))
  send_timezone = db.Column(db.String(150))
  candidate_status = db.Column(db.String(150))
  expiring_url = db.Column(db.String(150), unique=True)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CandidatesEmailSentObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  from_user_id_fk = db.Column(db.String(150))
  to_email = db.Column(db.String(150))
  assessment_expiring_url_fk = db.Column(db.String(150))
  subject = db.Column(db.String(1000))
  body = db.Column(db.String(1000))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CandidatesAssessmentGradedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  candidate_email = db.Column(db.String(150))
  assessment_name = db.Column(db.String(150))
  assessment_id_fk = db.Column(db.String(150))
  created_assessment_user_id_fk = db.Column(db.String(150))
  assessment_expiring_url_fk = db.Column(db.String(150), unique=True)
  correct_count = db.Column(db.Integer)
  final_score = db.Column(db.Float)
  assessment_obj = db.Column(db.String(15000))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CandidatesStripeCheckoutSessionObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_checkout_session_id = db.Column(db.String(150))
  fk_user_id = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class CandidatesCreatedQuestionsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  status = db.Column(db.Boolean, default=False)
  categories = db.Column(db.String(150))
  title = db.Column(db.String(150))
  difficulty = db.Column(db.String(20))
  question = db.Column(db.String(1000))
  option_a = db.Column(db.String(280))
  option_b = db.Column(db.String(280))
  option_c = db.Column(db.String(280))
  option_d = db.Column(db.String(280))
  option_e = db.Column(db.String(280))
  answer = db.Column(db.String(10))
  aws_image_uuid = db.Column(db.String(150))
  aws_image_url = db.Column(db.String(150))
# ------------------------ individual model end ------------------------
# ------------------------ models end ------------------------


# ------------------------ tables start ------------------------
# ------------------------ tables end ------------------------
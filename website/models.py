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

  def get_reset_token_function(self, expires_sec=30):
    s = Serializer(secret_key_ref, expires_sec)
    return s.dumps({'dump_load_user_id': self.id}).decode('utf-8')

  @staticmethod
  def verify_reset_token_function(token):
    s = Serializer(secret_key_ref)
    try:
      dl_user_id_from_token = s.loads(token)['dump_load_user_id']
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
# ------------------------ individual model end ------------------------
# ------------------------ models end ------------------------


# ------------------------ tables start ------------------------
# ------------------------ tables start ------------------------
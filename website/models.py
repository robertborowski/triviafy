# ------------------------ imports start ------------------------
from email.policy import default
from website import db
from flask_login import UserMixin
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
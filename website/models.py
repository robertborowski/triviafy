# ------------------------ imports start ------------------------
from website import db
from flask_login import UserMixin
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
# ------------------------ imports end ------------------------


# ------------------------ models start ------------------------
# Note: models vs tables: https://stackoverflow.com/questions/45044926/db-model-vs-db-table-in-flask-sqlalchemy
class CandidatesUserObj(db.Model, UserMixin):   # Only the users object inherits UserMixin, other models do NOT!
  id = db.Column(db.String(150), primary_key=True, default=create_uuid_function('user_'))
  created_timestamp = db.Column(db.DateTime(timezone=True), default=create_timestamp_function())
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  first_name = db.Column(db.String(150))
  last_name = db.Column(db.String(150))
  company_name = db.Column(db.String(150))
  department_name = db.Column(db.String(150))
# ------------------------ models end ------------------------


# ------------------------ tables start ------------------------
# ------------------------ tables start ------------------------
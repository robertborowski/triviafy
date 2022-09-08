# ------------------------ imports start ------------------------
from website import db
from flask_login import UserMixin
# ------------------------ imports end ------------------------


# ------------------------ models start ------------------------
# Note: models vs tables: https://stackoverflow.com/questions/45044926/db-model-vs-db-table-in-flask-sqlalchemy
class CandidatesUserObj(db.Model, UserMixin):   # Only the users object inherits UserMixin, other models do NOT!
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  first_name = db.Column(db.String(150))
  last_name = db.Column(db.String(150))
  company_name = db.Column(db.String(150))
  department_name = db.Column(db.String(150))
# ------------------------ models end ------------------------


# ------------------------ tables start ------------------------
# ------------------------ tables start ------------------------
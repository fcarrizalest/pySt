from flask_wtf.csrf import CsrfProtect
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()
csrf = CsrfProtect()
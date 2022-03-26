from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

app = Flask(__name__)

# configuration
app.config['WTF_CSRF_ENABLED'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'cairocoders-ednalan'

# csrf protection
csrf = CSRFProtect()
csrf.init_app(app)
# create database
db = SQLAlchemy(app)

# database migration
migrate = Migrate(app, db)

from app import views, models

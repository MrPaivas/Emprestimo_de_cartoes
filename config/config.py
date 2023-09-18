from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True

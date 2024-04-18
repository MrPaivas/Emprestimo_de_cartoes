from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()

PASSWORD = os.environ.get('DB_PASS')
PUBLIC_IP_ADDRESS = os.environ.get('PUBLIC_IP_ADDRESS')
DBNAME = os.environ.get('DB_NAME')
PROJECT_ID = os.environ.get('PROJECT_ID')
INSTANCE_NAME = os.environ.get('INSTANCE_NAME')

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True

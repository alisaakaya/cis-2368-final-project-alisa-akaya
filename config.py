import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('exam.c1ok6yy085d2.us-east-2.rds.amazonaws.com')
    
    # Application configuration
    SECRET_KEY = os.environ.get('password')
    
    # CORS configuration
    CORS_HEADERS = 'Content-Type'

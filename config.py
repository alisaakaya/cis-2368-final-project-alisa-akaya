import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('exam.c1ok6yy085d2.us-east-2.rds.amazonaws.com')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-for-development'
    
    # CORS configuration
    CORS_HEADERS = 'Content-Type'

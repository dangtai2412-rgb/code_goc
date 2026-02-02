# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Cấu hình cơ bản
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ban-cuc-ky-bi-mat'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///default.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cấu hình API
    API_PREFIX = '/api'  # <-- Thêm dòng này để quản lý version API dễ hơn
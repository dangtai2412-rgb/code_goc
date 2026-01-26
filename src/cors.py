# src/cors.py
from flask_cors import CORS

def init_cors(app):
    # Thay đổi: origins="*" (chấp nhận mọi nguồn) để tránh bị chặn oan
    CORS(app, resources={
        r"/*": {
            "origins": "*", 
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
        }
    })
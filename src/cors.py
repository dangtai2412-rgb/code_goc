from flask_cors import CORS

def init_cors(app):
    CORS(app, resources={
        r"/*": { # Cho phép tất cả các đường dẫn
            "origins": ["http://localhost:3000"], # Chỉ cho phép trang Web của bạn
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
            "supports_credentials": True
        }
    })
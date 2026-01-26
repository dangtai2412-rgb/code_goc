from flask_cors import CORS

def init_cors(app):
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000"],  # Cho phép cổng 3000 của Frontend
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
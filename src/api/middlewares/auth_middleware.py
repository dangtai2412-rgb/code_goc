# src/api/middlewares/auth_middleware.py
from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Lấy token từ header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token là bắt buộc! (Vui lòng đăng nhập)'}), 401

        try:
            # Giải mã token
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            
            # Gán thông tin user vào request để dùng ở Controller sau này
            request.current_user = data
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token đã hết hạn! Hãy đăng nhập lại.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token không hợp lệ!'}), 401
        except Exception as e:
            return jsonify({'message': f'Lỗi xác thực: {str(e)}'}), 500

        return f(*args, **kwargs)
    return decorated
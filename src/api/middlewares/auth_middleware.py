# src/api/middlewares/auth_middleware.py
from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 1. Lấy SECRET_KEY trực tiếp từ Config để đảm bảo luôn mới nhất
        key = Config.SECRET_KEY 
        
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            # SỬA: Lấy token an toàn, loại bỏ chữ Bearer nếu có
            token = auth_header.replace("Bearer ", "").strip()

        if not token:
            return jsonify({'message': 'Token là bắt buộc! (Vui lòng đăng nhập)'}), 401

        try:
            # 2. Giải mã Token
            data = jwt.decode(token, key, algorithms=["HS256"])
            
            # 3. Gắn dữ liệu vào request object
            request.current_user = data 
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token đã hết hạn! Hãy đăng nhập lại.'}), 401
        except jwt.InvalidTokenError:
            # Chỉ giữ lại một khối xử lý lỗi Token không hợp lệ
            return jsonify({'message': 'Token không hợp lệ!'}), 401
        except Exception as e:
            return jsonify({'message': f'Lỗi xác thực: {str(e)}'}), 401

        return f(*args, **kwargs)

    return decorated
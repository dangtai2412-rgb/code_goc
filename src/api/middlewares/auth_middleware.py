from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

SECRET_KEY = Config.SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 1. Lấy token từ Header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
            else:
                token = auth_header

        if not token:
            return jsonify({'message': 'Token là bắt buộc! (Vui lòng đăng nhập)'}), 401

        try:
            # 2. Giải mã Token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            
            # 3. GẮN VÀO REQUEST THAY VÌ TRUYỀN POSITIONAL ARGUMENT
            # Điều này giúp tránh lỗi "Argument Mismatch" trong Controller
            request.current_user_id = data.get('user_id')
            request.current_role = data.get('role')
            request.current_user = data # Lưu toàn bộ object để dùng nếu cần
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token đã hết hạn! Hãy đăng nhập lại.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token không hợp lệ!'}), 401
        except Exception as e:
            return jsonify({'message': f'Lỗi xác thực: {str(e)}'}), 401

        # FIX: Gọi hàm f mà không truyền 'data' vào đầu để khớp với signature của Controller
        return f(*args, **kwargs)

    return decorated
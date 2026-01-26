# src/api/middlewares/auth_middleware.py
from functools import wraps
from flask import request, jsonify
import jwt
import inspect
from config import Config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 1. QUAN TRỌNG: Nếu là phương thức OPTIONS (trình duyệt kiểm tra) thì cho qua luôn
        if request.method == 'OPTIONS':
            return f(*args, **kwargs)

        key = Config.SECRET_KEY
        token = None
        
        # 2. Lấy token từ header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "").strip()

        # Debug: In ra terminal để xem token đã đến nơi chưa
        if token:
            print(f"✅ SERVER: Đã nhận Token: {token[:10]}...") 
        else:
            print(f"❌ SERVER: Không thấy Token đâu cả!")

        if not token:
            return jsonify({'message': 'Token là bắt buộc! (Vui lòng đăng nhập)'}), 401

        try:
            # Giải mã Token
            data = jwt.decode(token, key, algorithms=["HS256"])
            request.current_user = data
            
            # Tự động truyền user vào hàm xử lý
            sig = inspect.signature(f)
            params = sig.parameters
            
            if 'current_user' in params:
                return f(data, *args, **kwargs)
            if 'current_user_id' in params:
                return f(data.get('user_id'), *args, **kwargs)
                
        except Exception as e:
            print(f"❌ LỖI TOKEN: {str(e)}")
            return jsonify({'message': 'Token không hợp lệ hoặc hết hạn!'}), 401

        return f(*args, **kwargs)
    return decorated
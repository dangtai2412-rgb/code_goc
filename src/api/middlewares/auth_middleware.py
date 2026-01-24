# src/api/middlewares/auth_middleware.py (replacement)
from functools import wraps
from flask import request, jsonify
import jwt
import inspect
from config import Config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = Config.SECRET_KEY
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "").strip()

        if not token:
            return jsonify({'message': 'Token là bắt buộc! (Vui lòng đăng nhập)'}), 401

        try:
            data = jwt.decode(token, key, algorithms=["HS256"])
            request.current_user = data

            sig = inspect.signature(f)
            params = sig.parameters
            if 'current_user' in params:
                return f(data, *args, **kwargs)
            if 'current_user_id' in params:
                return f(data.get('user_id'), *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token đã hết hạn! Hãy đăng nhập lại.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token không hợp lệ!'}), 401
        except Exception as e:
            return jsonify({'message': f'Lỗi xác thực: {str(e)}'}), 401

        return f(*args, **kwargs)
    return decorated
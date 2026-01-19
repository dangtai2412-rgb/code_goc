from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
@inject
def login_system(auth_service: AuthService = Provide[Container.auth_service]):
    """
    Đăng nhập hệ thống (Quét 3 bảng: Admin, Owner, Employee)
    """
    try:
        data = request.get_json()
        # Đổi từ username sang email cho đúng logic mới
        email = data.get('email') or data.get('username') 
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Thiếu email hoặc mật khẩu"}), 400
            
        result = auth_service.login(email, password)
        
        if result:
            return jsonify(result), 200
        
        return jsonify({"error": "Tài khoản hoặc mật khẩu không chính xác"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
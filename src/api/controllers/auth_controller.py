from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.auth_service import AuthService

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
@inject
def login_system(auth_service: AuthService = Provide[Container.auth_service]):
    """
    Đăng nhập vào hệ thống BizFlow
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: admin@bizflow.com
            password:
              type: string
              example: "123456"
    responses:
      200:
        description: Đăng nhập thành công, trả về token JWT
        schema:
          type: object
          properties:
            token:
              type: string
            user:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                role:
                  type: string
      400:
        description: Thiếu dữ liệu đầu vào
      401:
        description: Sai tài khoản hoặc mật khẩu
      500:
        description: Lỗi hệ thống
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Thiếu dữ liệu"}), 400
            
        email = data.get('email')
        password = data.get('password')
        role = data.get('role') # SỬA: Lấy role từ request

        if not email or not password:
            return jsonify({"error": "Vui lòng nhập Email và Mật khẩu"}), 400
            
        # Gọi service kèm theo role
        result = auth_service.login(email, password, role)
        
        if result:
            return jsonify(result), 200
        
        return jsonify({"error": "Sai thông tin đăng nhập hoặc sai vai trò!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
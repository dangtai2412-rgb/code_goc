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
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Thiếu dữ liệu đăng nhập"}), 400

        email = data.get('email') or data.get('username')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Thiếu email hoặc mật khẩu"}), 400

        result = auth_service.login(email, password)

        if result:
            # result is {"token": "...", "user": {...}}
            return jsonify({
                "token": result["token"],
                "user": result["user"]
            }), 200

        return jsonify({"error": "Tài khoản hoặc mật khẩu không chính xác"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
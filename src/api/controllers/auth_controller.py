from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from infrastructure.repositories.access_and_identity_repo.administrator_repository import AdministratorRepository
from infrastructure.repositories.access_and_identity_repo.business_owner_repository import BusinessOwnerRepository
from infrastructure.repositories.access_and_identity_repo.employee_repository import EmployeeRepository
from infrastructure.databases.mssql import session

auth_bp = Blueprint('auth_bp', __name__)

# Khởi tạo các Repo để AuthService quét 3 bảng
admin_repo = AdministratorRepository(session)
owner_repo = BusinessOwnerRepository(session)
emp_repo = EmployeeRepository(session)

auth_service = AuthService(admin_repo, owner_repo, emp_repo)

@auth_bp.route('/login', methods=['POST'])
def login_system(): # Đổi tên hàm thành login_system để tránh trùng với tên endpoint
    """
    Đăng nhập hệ thống (Admin, Owner, Employee)
    ---
    tags: [Auth]
    parameters:
      - in: body
        name: body
        schema:
          required: [username, password]
          properties:
            username: {type: string, example: "admin01"}
            password: {type: string, example: "123456"}
    responses:
      200: {description: "Đăng nhập thành công, trả về JWT Token"}
      401: {description: "Sai tài khoản hoặc mật khẩu"}
    """
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Thiếu username hoặc password"}), 400
            
        result = auth_service.login(data['username'], data['password'])
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401
    except Exception as e:
        return jsonify({"error": "Lỗi hệ thống: " + str(e)}), 500
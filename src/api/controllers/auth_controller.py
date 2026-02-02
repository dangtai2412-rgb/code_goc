from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.auth_service import AuthService
from error_handler import CustomError # Import custom error handler
from api.responses import success_response # Import hàm trả về chuẩn

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
@inject
def login_system(auth_service: AuthService = Provide[Container.auth_service]):
    """
    Đăng nhập vào hệ thống BizFlow
    ---
    tags: [Auth]
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [email, password]
          properties:
            email: {type: string, example: "owner@bizflow.com"}
            password: {type: string, example: "123456"}
            role: {type: string, enum: [BUSINESS_OWNER, EMPLOYEE, ADMINISTRATOR], default: BUSINESS_OWNER}
    responses:
      200:
        description: Đăng nhập thành công
      400:
        description: Thiếu thông tin
      401:
        description: Sai mật khẩu
    """
    # 1. Lấy dữ liệu
    data = request.get_json()
    if not data:
        raise CustomError("Vui lòng gửi dữ liệu JSON", 400)
            
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'BUSINESS_OWNER') # Mặc định là chủ doanh nghiệp

    # 2. Validate thủ công (với Login đơn giản thì không cần Schema quá phức tạp)
    if not email or not password:
        raise CustomError("Email và Mật khẩu là bắt buộc", 400)
        
    # 3. Gọi Service (Không cần try-except)
    result = auth_service.login(email, password, role)
    
    if result:
        return success_response(data=result, message="Đăng nhập thành công")
    
    # Nếu service trả về False/None
    raise CustomError("Sai thông tin đăng nhập hoặc vai trò không đúng", 401)
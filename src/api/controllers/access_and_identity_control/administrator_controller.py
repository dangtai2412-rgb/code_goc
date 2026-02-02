from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

admin_bp = Blueprint('admin_bp', __name__)

# --- ROUTE: CREATE ADMIN ---
@admin_bp.route('/', methods=['POST'])
@token_required  # Kiểm tra token trước
@inject          # Sau đó mới inject service
def create(admin_service: any = Provide[Container.administrator_service]):
    """
    Tạo tài khoản Administrator mới (Super Admin)
    ---
    tags: [Administrator]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [admin_name, email, password]
          properties:
            admin_name: {type: string, example: "Super Admin"}
            email: {type: string, example: "admin@system.com"}
            password: {type: string, example: "admin123"}
    responses:
      201: {description: "Tạo thành công"}
      400: {description: "Lỗi dữ liệu đầu vào"}
      401: {description: "Không có quyền truy cập"}
    """
    try:
        data = request.get_json()
        
        # Kiểm tra dữ liệu đầu vào cơ bản
        if not data or not all(k in data for k in ("admin_name", "email", "password")):
            return jsonify({"error": "Thiếu thông tin bắt buộc"}), 400

        result = admin_service.create_admin(data)
        
        return jsonify({
            "message": "Tạo tài khoản thành công", 
            "id": result.admin_id
        }), 201

    except ValueError as ve: # Catch lỗi logic (ví dụ email đã tồn tại)
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Lỗi hệ thống nội bộ"}), 500


# --- ROUTE: LIST ADMINS ---
@admin_bp.route('/', methods=['GET'])
@token_required
@inject
def list_admins(admin_service: any = Provide[Container.administrator_service]):
    """
    Lấy danh sách admin
    ---
    tags: [Administrator]
    security: [{BearerAuth: []}]
    responses:
      200: 
        description: "Lấy danh sách thành công"
        schema:
          type: array
          items:
            type: object
            properties:
              id: {type: integer}
              name: {type: string}
              email: {type: string}
    """
    try:
        # Lấy ID người gọi từ middleware nếu cần kiểm tra quyền
        # requester_id = getattr(request, 'current_user_id', None)
        
        admins = admin_service.get_all_admins()
        
        # Chuyển đổi list object sang json
        response_data = [
            {
                "id": a.admin_id, 
                "name": a.admin_name, 
                "email": a.email
            } for a in admins
        ]
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({"error": "Không thể lấy danh sách admin"}), 500
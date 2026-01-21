from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/', methods=['POST'])
@token_required 
@inject
# REMOVED: current_user (Access via request.current_user_id instead)
def create(admin_service = Provide[Container.administrator_service]):
    """
    Tạo tài khoản Administrator mới (Super Admin)
    ---
    tags: [Administrator]
    security: [{BearerAuth: []}]  # ADDED: Essential for Swagger to send the token
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
      400: {description: "Lỗi dữ liệu"}
    """
    try:
        data = request.get_json()
        result = admin_service.create_admin(data)
        return jsonify({"message": "Thành công", "id": result.admin_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@admin_bp.route('/', methods=['GET'])
@token_required
@inject
# REMOVED: current_user to maintain consistency and prevent 500 errors
def list_admins(admin_service = Provide[Container.administrator_service]):
    """
    Lấy danh sách admin
    ---
    tags: [Administrator]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Success"}
    """
    try:
        # Example: You can still get the user ID if needed:
        # admin_who_requested = request.current_user_id 
        
        admins = admin_service.get_all_admins()
        return jsonify([{"id": a.admin_id, "name": a.admin_name, "email": a.email} for a in admins]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
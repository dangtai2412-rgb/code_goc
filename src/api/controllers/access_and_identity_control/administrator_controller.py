from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

admin_bp = Blueprint('admin_bp', __name__)

# --- 1. TẠO ADMIN (Đã tối ưu) ---
@admin_bp.route('/', methods=['POST'])
@token_required
@inject
def create(admin_service = Provide[Container.administrator_service]):
    """ Tạo tài khoản Admin mới """
    try:
        data = request.get_json()
        if not data: return jsonify({"error": "No data provided"}), 400
        
        result = admin_service.create_admin(data)
        return jsonify({"message": "Thành công", "id": result.admin_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

# --- 2. LẤY DANH SÁCH + PHÂN TRANG (Pagination) ---
@admin_bp.route('/', methods=['GET'])
@token_required
@inject
def list_admins(admin_service = Provide[Container.administrator_service]):
    """ 
    Lấy danh sách admin có phân trang 
    Query params: ?page=1&limit=10
    """
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        # Giả sử service của bạn hỗ trợ paginate
        admins, total = admin_service.get_paginated_admins(page, limit)
        
        return jsonify({
            "total": total,
            "page": page,
            "limit": limit,
            "data": [{"id": a.admin_id, "name": a.admin_name, "email": a.email} for a in admins]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 3. CẬP NHẬT THÔNG TIN (Update) ---
@admin_bp.route('/<int:admin_id>', methods=['PUT'])
@token_required
@inject
def update_admin(admin_id, admin_service = Provide[Container.administrator_service]):
    """ Cập nhật thông tin admin theo ID """
    try:
        data = request.get_json()
        updated_admin = admin_service.update_admin(admin_id, data)
        if not updated_admin:
            return jsonify({"error": "Admin không tồn tại"}), 404
            
        return jsonify({"message": "Cập nhật thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- 4. XÓA ADMIN (Delete) ---
@admin_bp.route('/<int:admin_id>', methods=['DELETE'])
@token_required
@inject
def delete_admin(admin_id, admin_service = Provide[Container.administrator_service]):
    """ Xóa admin (nên dùng Soft Delete trong thực tế) """
    try:
        # Ngăn chặn việc tự xóa chính mình (nếu cần)
        # if admin_id == request.current_user_id:
        #    return jsonify({"error": "Không thể tự xóa chính mình"}), 400

        success = admin_service.delete_admin(admin_id)
        if not success:
            return jsonify({"error": "Không tìm thấy Admin"}), 404
            
        return jsonify({"message": "Đã xóa Admin thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
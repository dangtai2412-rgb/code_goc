# src/api/controllers/inventory_control/supplier_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

supplier_bp = Blueprint('supplier_bp', __name__)

@supplier_bp.route('/', methods=['POST'])
@token_required
@inject
def add_supplier(supplier_service = Provide[Container.supplier_service]):
    """
    Thêm nhà cung cấp mới
    ---
    tags: [Suppliers]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [supplier_name]
          properties:
            supplier_name: {type: string, example: "Vật liệu Xây dựng Toàn Cầu"}
            phone_number: {type: string, example: "0912345678"}
    responses:
      201:
        description: Tạo thành công
        schema:
          properties:
            id: {type: integer}
      400:
        description: Lỗi dữ liệu hoặc quyền hạn
    """
    try:
        data = request.get_json()
        # SỬA: Lấy từ dictionary current_user
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        if not owner_id:
            return jsonify({"error": "Token thiếu thông tin owner_id"}), 401

        supplier = supplier_service.create_supplier(data, owner_id)
        return jsonify({"id": supplier.supplier_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@supplier_bp.route('/', methods=['GET'])
@token_required
@inject
def get_suppliers(supplier_service = Provide[Container.supplier_service]):
    """
    Lấy danh sách nhà cung cấp
    ---
    tags: [Suppliers]
    security: [{BearerAuth: []}]
    responses:
      200:
        description: Thành công
    """
    # Tương tự, sửa cách lấy owner_id cho hàm GET
    user_info = getattr(request, 'current_user', {})
    owner_id = user_info.get('owner_id') or user_info.get('user_id')
    
    suppliers = supplier_service.get_suppliers_by_owner(owner_id)
    return jsonify([{"id": s.supplier_id, "name": s.supplier_name} for s in suppliers]), 200
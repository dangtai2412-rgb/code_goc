# src/api/controllers/inventory_control/unit_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

unit_bp = Blueprint('unit_bp', __name__)

@unit_bp.route('/', methods=['POST'])
@token_required
@inject
def create_new_unit(unit_service = Provide[Container.unit_service]):
    """
    Tạo đơn vị tính mới (ví dụ: Bao, Viên, Khối)
    ---
    tags: [Inventory]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [unit_name]
          properties:
            unit_name:
              type: string
              example: "Bao"
            description:
              type: string
              example: "Đơn vị tính cho xi măng"
    responses:
      201:
        description: Tạo thành công
      400:
        description: Lỗi dữ liệu đầu vào
    """
    try:
        data = request.get_json()
        
        # Lấy owner_id từ Token
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        # Gọi hàm create_unit (đã sửa tên trong Service)
        result = unit_service.create_unit(data, owner_id)
        
        return jsonify({"message": "Tạo đơn vị thành công", "id": result.unit_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# src/api/controllers/inventory_control/unit_controller.py
@unit_bp.route('/product/<int:product_id>', methods=['GET'])
@token_required
@inject
def list_units_by_product(product_id, unit_service = Provide[Container.unit_service]):
    """
    Lấy danh sách đơn vị tính theo ID sản phẩm
    """
    try:
        # Gọi hàm trong service
        units = unit_service.get_units_by_product(product_id)
        
        return jsonify([
            {
                "id": u.unit_id, 
                "name": u.unit_name,
                "conversion_rate": u.conversion_rate,
                "is_base": u.is_base_unit
            } for u in units
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@unit_bp.route('/', methods=['GET'])
@token_required
@inject
def list_units(unit_service = Provide[Container.unit_service]):
    """Lấy danh sách đơn vị tính của cửa hàng"""
    try:
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        units = unit_service.get_units(owner_id)
        return jsonify([{"id": u.unit_id, "name": u.unit_name} for u in units]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
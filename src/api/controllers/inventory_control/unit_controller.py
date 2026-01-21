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
        result = unit_service.create_unit(data)
        return jsonify({"message": "Tạo đơn vị thành công", "id": result.unit_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@unit_bp.route('/product/<int:product_id>', methods=['GET'])
@token_required
@inject
def list_units_by_product(product_id, unit_service = Provide[Container.unit_service]):
    """
    Lấy danh sách đơn vị tính theo ID sản phẩm
    ---
    tags: [Inventory]
    security: [{BearerAuth: []}]
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: ID của sản phẩm cần lấy đơn vị tính
    responses:
      200:
        description: Danh sách đơn vị tính của sản phẩm
      500:
        description: Lỗi hệ thống
    """
    try:
        units = unit_service.get_units_by_product(product_id)
        return jsonify([{"id": u.unit_id, "name": u.unit_name} for u in units]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
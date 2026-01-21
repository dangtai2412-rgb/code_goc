# src/api/controllers/inventory_control/stock_import_detail_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

stock_import_detail_bp = Blueprint('stock_import_detail_bp', __name__)

@stock_import_detail_bp.route('/', methods=['POST'])
@token_required
@inject
def add_detail(service = Provide[Container.stock_import_detail_service]):
    """
    Thêm chi tiết hàng hóa vào phiếu nhập (Dòng hàng)
    ---
    tags: [Inventory Control]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [import_id, product_id, quantity, unit_price]
          properties:
            import_id: {type: integer, example: 1}
            product_id: {type: integer, example: 10}
            quantity: {type: integer, example: 100}
            unit_price: {type: number, example: 50000}
    responses:
      201: {description: "Thành công"}
      400: {description: "Lỗi dữ liệu"}
    """
    try:
        data = request.get_json()
        detail = service.create_detail(data)
        return jsonify({"id": detail.detail_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@stock_import_detail_bp.route('/import/<int:import_id>', methods=['GET'])
@token_required
@inject
def get_details(import_id, service = Provide[Container.stock_import_detail_service]):
    """
    Lấy danh sách chi tiết các mặt hàng trong một phiếu nhập
    ---
    tags: [Inventory Control]
    security: [{BearerAuth: []}]
    parameters:
      - name: import_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: "Thành công"}
    """
    try:
        details = service.get_details_by_import(import_id)
        return jsonify([{
            "id": d.detail_id,
            "product_id": d.product_id,
            "quantity": d.quantity,
            "unit_price": float(d.unit_price)
        } for d in details]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
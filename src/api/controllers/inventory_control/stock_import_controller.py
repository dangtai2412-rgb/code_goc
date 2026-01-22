# src/api/controllers/inventory_control/stock_import_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

stock_import_bp = Blueprint('stock_import_bp', __name__)

@stock_import_bp.route('/', methods=['POST'])
@token_required
@inject
def import_goods(stock_service = Provide[Container.stock_import_service]):
    """
    Tạo phiếu nhập hàng vào kho (Nhập hàng từ NCC)
    ---
    tags: [Inventory Control]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [supplier_id, items]
          properties:
            supplier_id:
              type: integer
              example: 1
            import_date:
              type: string
              example: "2026-01-21"
            items:
              type: array
              items:
                type: object
                properties:
                  product_id: {type: integer, example: 10}
                  quantity: {type: number, example: 50}
                  import_price: {type: number, example: 150000}
    responses:
      201: {description: "Nhập hàng thành công"}
      500: {description: "Lỗi hệ thống"}
    """
    try:
        data = request.get_json()
        
        # SỬA LỖI TẠI ĐÂY: Lấy từ dictionary current_user giống các phần trước
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        if not owner_id:
            return jsonify({"error": "Token thiếu thông tin owner_id"}), 401
        
        result = stock_service.create_stock_import(data, owner_id)
        return jsonify({"message": "Success", "import_id": result.import_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@stock_import_bp.route('/', methods=['GET'])
@token_required
@inject
def get_import_history(stock_service = Provide[Container.stock_import_service]):
    """
    Lấy danh sách lịch sử nhập hàng của cửa hàng
    ---
    tags: [Inventory Control]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Thành công"}
      401: {description: "Chưa xác thực"}
    """
    try:
        owner_id = getattr(request, 'current_user_id', None)
        # Truy vấn lịch sử nhập hàng theo chủ cửa hàng
        history = stock_service.get_history_by_owner(owner_id)
        return jsonify(history), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
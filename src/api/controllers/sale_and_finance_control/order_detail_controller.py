# src/api/controllers/sale_and_finance_control/order_detail_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.order_detail_service import OrderDetailService

order_detail_bp = Blueprint('order_detail_bp', __name__)

@order_detail_bp.route('/', methods=['POST'])
@token_required
@inject
def add_order_detail(detail_service: OrderDetailService = Provide[Container.order_detail_service]):
    """
    Thêm chi tiết sản phẩm vào đơn hàng
    ---
    tags: [Order Details]
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [order_id, product_id, quantity, unit_price]
          properties:
            order_id: {type: integer, example: 1}
            product_id: {type: integer, example: 1}
            quantity: {type: integer, example: 10}
            unit_price: {type: number, example: 50000}
    responses:
      201:
        description: Thành công
        schema:
          type: object
          properties:
            message: {type: string}
            id: {type: integer}
    """
    try:
        data = request.get_json()
        user_info = getattr(request, 'current_user', {})
        
        # SỬA: Lấy owner_id linh hoạt từ key id/user_id/owner_id
        owner_id = user_info.get('owner_id') or user_info.get('user_id') or user_info.get('id')
        data['owner_id'] = owner_id
        
        result = detail_service.create_detail(data)
        
        return jsonify({
            "message": "Thêm chi tiết đơn hàng thành công", 
            "id": result.order_detail_id # Đảm bảo tên trường id đúng với Model của bạn
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
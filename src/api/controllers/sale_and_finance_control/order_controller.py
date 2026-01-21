# src/api/controllers/sale_and_finance_control/order_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.order_service import OrderService

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/', methods=['POST'])
@token_required
@inject
def post_order(order_service: OrderService = Provide[Container.order_service]):
    """
    Tạo đơn hàng mới
    ---
    tags: [Sales - Order]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          required: [customer_id, details]
          properties:
            customer_id: {type: integer}
            total_amount: {type: number}
            paid_amount: {type: number}
            payment_method: {type: string}
            details:
              type: array
              items:
                properties:
                  product_id: {type: integer}
                  quantity: {type: integer}
                  unit_price: {type: number}
    responses:
      201: {description: Tạo đơn hàng thành công}
    """
    try:
        data = request.get_json()
        
        # Lấy thông tin từ Dictionary 'current_user' được gắn vào request từ middleware
        user_info = getattr(request, 'current_user', {})
        
        # 1. Xác định owner_id (Nếu là chủ thì user_id chính là owner_id)
        token_owner_id = user_info.get('owner_id') or user_info.get('user_id')
        data['owner_id'] = token_owner_id
        
        # 2. Lấy ID người trực tiếp tạo đơn
        user_id = user_info.get('user_id')

        result = order_service.create_order(data, user_id)

        return jsonify({
            "message": "Tạo đơn hàng thành công", 
            "order_id": result.order_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
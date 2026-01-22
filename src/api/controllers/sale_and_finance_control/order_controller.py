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
@order_bp.route('/', methods=['GET'])
@token_required
@inject
def get_order_list(order_service: OrderService = Provide[Container.order_service]):
    """
    Lấy danh sách đơn hàng của shop
    ---
    tags: [Orders]
    security:
      - BearerAuth: []
    responses:
      200:
        description: Danh sách đơn hàng trả về thành công
        schema:
          type: array
          items:
            type: object
            properties:
              order_id: {type: integer, example: 1}
              total_amount: {type: number, example: 500000}
              payment_status: {type: string, example: "PAID"}
              order_date: {type: string, example: "2024-01-22T21:30:00"}
    """
    try:
        # Lấy owner_id từ Token bảo mật
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id') or user_info.get('id')
        
        if not owner_id:
            return jsonify({"error": "Không tìm thấy thông tin chủ cửa hàng"}), 401
            
        orders = order_service.get_orders_by_owner(owner_id)
        
        # Chuyển đổi danh sách Model sang JSON (Đảm bảo OrderModel đã có hàm to_dict)
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
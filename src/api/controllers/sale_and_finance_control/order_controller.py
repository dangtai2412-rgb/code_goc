# src/api/controllers/sale_and_finance_control/order_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.order_service import OrderService
from api.schemas.order import OrderRequestSchema, OrderResponseSchema # Import Schema

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
        required: true
        schema:
          $ref: '#/definitions/OrderRequest' 
    responses:
      201:
        description: Tạo đơn hàng thành công
        schema:
          $ref: '#/definitions/OrderResponse'
    """
    # 1. Nhận và Validate dữ liệu
    json_data = request.get_json()
    schema = OrderRequestSchema()
    # Dòng dưới sẽ tự ném ra lỗi ValidationError nếu dữ liệu sai -> error_handler sẽ bắt
    validated_data = schema.load(json_data) 
    
    # 2. Lấy thông tin User từ Middleware (đã gán vào request.current_user)
    user_info = request.current_user 
    token_owner_id = user_info.get('owner_id') or user_info.get('user_id')
    user_id = user_info.get('user_id')

    # Bổ sung thông tin vào data đã validate
    validated_data['owner_id'] = token_owner_id

    # 3. Gọi Service (Không cần try-except, nếu service lỗi, error_handler sẽ lo)
    result = order_service.create_order(validated_data, user_id)

    return jsonify({
        "message": "Tạo đơn hàng thành công", 
        "order_id": result.order_id
    }), 201

@order_bp.route('/', methods=['GET'])
@token_required
@inject
def get_order_list(order_service: OrderService = Provide[Container.order_service]):
    """
    Lấy danh sách đơn hàng của shop
    ---
    tags: [Sales - Order]
    security: [{BearerAuth: []}]
    responses:
      200:
        description: Danh sách đơn hàng
        schema:
          type: array
          items:
            $ref: '#/definitions/OrderResponse'
    """
    user_info = request.current_user
    owner_id = user_info.get('owner_id') or user_info.get('user_id')
    
    orders = order_service.get_orders_by_owner(owner_id)
    
    # Dùng Schema để serialize danh sách object thành JSON
    response_schema = OrderResponseSchema(many=True)
    return jsonify(response_schema.dump(orders)), 200
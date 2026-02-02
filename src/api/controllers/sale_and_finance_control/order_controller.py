# src/api/controllers/sale_and_finance_control/order_controller.py
from flask import Blueprint, request
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.order_service import OrderService
from api.schemas.order import OrderRequestSchema, OrderResponseSchema
from api.responses import success_response

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/', methods=['POST'])
@token_required
@inject
def create_order(order_service: OrderService = Provide[Container.order_service]):
    """
    Tạo đơn hàng mới (Kèm chi tiết)
    ---
    tags: [Sales - Order]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/OrderRequest'
    """
    # 1. Validate dữ liệu (Tự động check cả nested details)
    schema = OrderRequestSchema()
    validated_data = schema.load(request.get_json())

    # 2. Lấy User ID
    user_info = request.current_user
    owner_id = user_info.get('owner_id') or user_info.get('user_id')
    user_id = user_info.get('user_id')

    # 3. Gọi Service Transaction
    new_order = order_service.create_order(validated_data, owner_id, user_id)

    # 4. Trả về kết quả
    return success_response(
        data=OrderResponseSchema().dump(new_order),
        message="Tạo đơn hàng thành công",
        status_code=201
    )

@order_bp.route('/', methods=['GET'])
@token_required
@inject
def get_orders(order_service: OrderService = Provide[Container.order_service]):
    """
    Lấy danh sách đơn hàng (Có phân trang)
    ---
    tags: [Sales - Order]
    security: [{BearerAuth: []}]
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
        description: Trang số mấy
      - in: query
        name: limit
        type: integer
        default: 20
        description: Số lượng bản ghi mỗi trang
    """
    user_info = request.current_user
    owner_id = user_info.get('owner_id') or user_info.get('user_id')
    
    # Lấy tham số từ URL (VD: /orders?page=2&limit=10)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)

    result = order_service.get_orders_by_owner(owner_id, page, limit)
    
    # Serialize danh sách items bên trong kết quả
    result['items'] = OrderResponseSchema(many=True).dump(result['items'])
    
    return success_response(data=result)
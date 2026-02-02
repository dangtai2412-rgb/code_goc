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
    Tạo đơn hàng mới (Kèm chi tiết sản phẩm)
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
    # 1. Validate dữ liệu đầu vào
    schema = OrderRequestSchema()
    json_data = request.get_json()
    validated_data = schema.load(json_data) # Tự động validate cả nested details

    # 2. Lấy thông tin người tạo
    user_info = request.current_user
    owner_id = user_info.get('owner_id') or user_info.get('user_id')
    user_id = user_info.get('user_id') # Người thực hiện (có thể là nhân viên)

    # 3. Gọi Service (Service sẽ lo Transaction)
    # Truyền cả validated_data (chứa details) vào service
    new_order = order_service.create_order(validated_data, owner_id, user_id)

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
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: limit
        type: integer
        default: 20
    """
    user_info = request.current_user
    owner_id = user_info.get('owner_id') or user_info.get('user_id')
    
    # Lấy tham số phân trang
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)

    # Gọi service hỗ trợ phân trang (Bạn cần sửa service tương ứng)
    orders = order_service.get_orders_by_owner(owner_id, page, limit)
    
    return success_response(data=OrderResponseSchema(many=True).dump(orders))
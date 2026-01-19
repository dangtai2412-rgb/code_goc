from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.order_detail_service import OrderDetailService
order_detail_bp = Blueprint('order_detail_bp', __name__)

@order_detail_bp.route('/', methods=['POST'])
@token_required
@inject
def add_order_detail(current_user, detail_service: OrderDetailService = Provide[Container.order_detail_service]):
    """
    Thêm chi tiết sản phẩm vào đơn hàng
    ---
    tags: [Order Details]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            order_id: {type: integer, example: 1}
            product_id: {type: integer, example: 1}
            quantity: {type: integer, example: 10}
            unit_price: {type: number, example: 50000}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        # Tự động gán owner_id từ user đang đăng nhập
        data['owner_id'] = getattr(current_user, 'owner_id', None)
        
        # Lấy ID người tạo (nhân viên hoặc chủ)
        user_id = getattr(current_user, 'user_id', None) or getattr(current_user, 'owner_id', None)
        
        result = detail_service.create_detail(data)
        return jsonify({
            "message": "Tạo đơn hàng thành công", 
            "order_id": result.order_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
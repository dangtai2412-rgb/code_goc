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
        
        # Lấy thông tin user từ request (do middleware gắn vào)
        user_info = getattr(request, 'current_user', {})
        
        # Tự động gán owner_id từ user đang đăng nhập
        # Dùng .get() vì user_info là một Dictionary
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        data['owner_id'] = owner_id
        
        # Lấy ID người trực tiếp thực hiện
        user_id = user_info.get('user_id')
        
        result = detail_service.create_detail(data)
        
        return jsonify({
            "message": "Thêm chi tiết đơn hàng thành công", 
            "id": result.detail_id # Sửa lại để trả về đúng ID của detail vừa tạo
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
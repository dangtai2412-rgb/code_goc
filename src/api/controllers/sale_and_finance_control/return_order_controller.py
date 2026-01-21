# src/api/controllers/sale_and_finance_control/return_order_controller.py
from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.return_order_service import ReturnOrderService
from api.middlewares.auth_middleware import token_required

return_order_bp = Blueprint('return_order_bp', __name__)

@return_order_bp.route('/', methods=['POST'])
@token_required
@inject
def create_return_order(service: ReturnOrderService = Provide[Container.return_order_service]):
    """
    Tạo phiếu trả hàng và hoàn tồn kho
    ---
    tags: [Sales - Return]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          required: [order_id, details]
          properties:
            order_id: {type: integer, example: 12}
            reason: {type: string, example: "Hàng lỗi nhà sản xuất"}
            refund_amount: {type: number, example: 50000}
            details:
              type: array
              items:
                properties:
                  product_id: {type: integer}
                  quantity: {type: integer}
                  condition: {type: string, enum: [Good, Broken]}
    responses:
      201:
        description: Trả hàng thành công
    """
    try:
        # FIXED: Lấy thông tin user từ Dictionary gắn trong request
        user_info = getattr(request, 'current_user', {})
        
        # Lấy owner_id (Nếu là nhân viên thì lấy owner_id, nếu là chủ thì lấy user_id)
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        data = request.json
        result = service.create_return(data, owner_id)
        
        return jsonify({
            "message": "Trả hàng thành công. Kho đã được cập nhật.",
            "return_id": result.return_id
        }), 201
    except Exception as e:
        print(f"Lỗi trả hàng: {e}")
        return jsonify({"error": str(e)}), 400
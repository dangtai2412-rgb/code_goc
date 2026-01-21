from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.return_order_service import ReturnOrderService
from api.middlewares.auth_middleware import token_required

return_order_bp = Blueprint('return_order_bp', __name__)

@return_order_bp.route('/', methods=['POST'])
@token_required
@inject
def create_return_order(current_user, service: ReturnOrderService = Provide[Container.return_order_service]):
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
        owner_id = getattr(current_user, 'owner_id', None)
        data = request.json
        
        result = service.create_return(data, owner_id)
        
        return jsonify({
            "message": "Trả hàng thành công. Kho đã được cập nhật.",
            "return_id": result.return_id
        }), 201
    except Exception as e:
        print(f"Lỗi trả hàng: {e}")
        return jsonify({"error": str(e)}), 400
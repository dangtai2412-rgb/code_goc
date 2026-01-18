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
    Tạo phiếu trả hàng
    Input:
    {
        "order_id": 12,
        "reason": "Khách đổi ý",
        "refund_amount": 50000,
        "details": [
            {"product_id": 1, "quantity": 2, "condition": "Good"}
        ]
    }
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
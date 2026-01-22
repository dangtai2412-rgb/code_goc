# src/api/controllers/sale_and_finance_control/payment_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.payment_service import PaymentService

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/', methods=['POST'])
@token_required
@inject
def create_payment(payment_service: PaymentService = Provide[Container.payment_service]):
    """
    Tạo phiếu thanh toán (Thu tiền)
    ---
    tags: [Finance & Payment]
    security:
      - BearerAuth: []
    """
    try:
        data = request.get_json()
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id') or user_info.get('id')
        
        # Chỉ cần gọi 1 hàm duy nhất xử lý cả 2 trường hợp
        result = payment_service.process_payment(data, owner_id)
        
        return jsonify({"message": "Thanh toán thành công", "id": result.payment_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


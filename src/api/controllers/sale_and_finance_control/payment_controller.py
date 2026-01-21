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
def process_debt_payment(payment_service: PaymentService = Provide[Container.payment_service]):
    """
    Thanh toán công nợ
    ---
    tags: [Finance & Debt]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          required: [debt_id, amount]
          properties:
            debt_id: {type: integer}
            amount: {type: number}
            payment_method: {type: string}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        
        # Mặc dù logic hiện tại của bạn không dùng đến current_user, 
        # nhưng việc xóa nó khỏi tham số hàm là bắt buộc để tránh lỗi 500.
        
        result = payment_service.process_payment(
            data.get('debt_id'), 
            data.get('amount'), 
            data.get('payment_method')
        )
        return jsonify({
            "message": "Thanh toán thành công", 
            "payment_id": result.payment_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
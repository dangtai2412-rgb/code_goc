from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.payment_service import PaymentService

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/', methods=['POST'])
@token_required
@inject
def process_debt_payment(current_user, payment_service: PaymentService = Provide[Container.payment_service]):
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
    """
    try:
        data = request.get_json()
        result = payment_service.process_payment(
            data.get('debt_id'), 
            data.get('amount'), 
            data.get('payment_method')
        )
        return jsonify({"message": "Thanh toán thành công", "payment_id": result.payment_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
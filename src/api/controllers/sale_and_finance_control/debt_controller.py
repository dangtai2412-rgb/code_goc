# src/api/controllers/sale_and_finance_control/debt_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.debt_service import DebtService # Bạn đã import cái này

debt_bp = Blueprint('debt_bp', __name__)

@debt_bp.route('/', methods=['POST'])
@token_required
@inject
# SỬA TẠI ĐÂY: Thay 'OrderService' bằng 'DebtService'
def create_customer_debt(debt_service: DebtService = Provide[Container.debt_service]):
    """
    Ghi nhận công nợ mới
    ---
    tags: [Finance & Debt]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            order_id: {type: integer, example: 1}
            customer_id: {type: integer, example: 1}
            debt_amount: {type: number, example: 500000}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        
        # 1. Lấy thông tin từ Token để xác định chủ cửa hàng
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id') or user_info.get('id')
        
        if not owner_id:
            return jsonify({"error": "Không tìm thấy thông tin chủ cửa hàng trong token"}), 401

        # 2. Gọi Service với đầy đủ 4 tham số: order_id, customer_id, owner_id, amount
        result = debt_service.create_debt_from_order(
            order_id=data.get('order_id'),
            customer_id=data.get('customer_id'),
            owner_id=owner_id,
            amount=data.get('debt_amount') # Map từ key 'debt_amount' trong JSON sang 'amount' của hàm
        )
        
        return jsonify({
            "message": "Ghi nợ thành công", 
            "id": result.debt_id,
            "remaining_debt": result.remaining_debt
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400
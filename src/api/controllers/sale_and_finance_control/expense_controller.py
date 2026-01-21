# src/api/controllers/sale_and_finance_control/expense_controller.py
from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.expense_service import ExpenseService
from api.middlewares.auth_middleware import token_required

expense_bp = Blueprint('expense_bp', __name__)

@expense_bp.route('/', methods=['POST'])
@token_required
@inject
def create_expense(service: ExpenseService = Provide[Container.expense_service]):
    try:
        data = request.get_json()
        
        # 1. Lấy thông tin user từ request (Middleware đã gắn vào)
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        # 2. Kiểm tra nếu owner_id vẫn None thì báo lỗi ngay
        if not owner_id:
            return jsonify({"error": "Không xác định được chủ cửa hàng. Vui lòng đăng nhập lại."}), 401

        # 3. Đảm bảo lấy đúng trường dữ liệu từ JSON (ví dụ Swagger gửi 'category')
        formatted_data = {
            'expense_category': data.get('category') or data.get('expense_category'),
            'amount': data.get('amount'),
            'description': data.get('description')
        }
        
        new_expense = service.create_expense(formatted_data, owner_id)
        
        return jsonify({"message": "Thành công", "id": new_expense.expense_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@expense_bp.route('/', methods=['GET'])
@token_required
@inject
def list_expenses(service: ExpenseService = Provide[Container.expense_service]):
    """
    Lấy lịch sử các khoản chi
    ---
    tags: [Finance - Expense]
    security: [{BearerAuth: []}]
    responses:
      200:
        description: Danh sách khoản chi
    """
    try:
        # FIXED: Xóa current_user khỏi tham số và lấy từ request dictionary
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        expenses = service.get_history(owner_id)
        
        return jsonify([{
            "id": ex.expense_id,
            "category": ex.expense_category,
            "amount": float(ex.amount),
            "date": ex.expense_date.strftime("%d/%m/%Y %H:%M"),
            "description": ex.description
        } for ex in expenses]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
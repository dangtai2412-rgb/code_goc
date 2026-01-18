from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.expense_service import ExpenseService
from api.middlewares.auth_middleware import token_required

expense_bp = Blueprint('expense_bp', __name__)

@expense_bp.route('/', methods=['POST'])
@token_required
@inject
def create_expense(current_user, service: ExpenseService = Provide[Container.expense_service]):
    try:
        owner_id = getattr(current_user, 'owner_id', None)
        data = request.json
        
        new_expense = service.create_expense(data, owner_id)
        
        return jsonify({
            "message": "Đã lưu khoản chi",
            "id": new_expense.expense_id,
            "amount": new_expense.amount
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@expense_bp.route('/', methods=['GET'])
@token_required
@inject
def list_expenses(current_user, service: ExpenseService = Provide[Container.expense_service]):
    try:
        owner_id = getattr(current_user, 'owner_id', None)
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
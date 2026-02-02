from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.customer_service import CustomerService

customer_bp = Blueprint('customer_bp', __name__)

def get_owner_id():
    user_info = getattr(request, 'current_user', {})
    return user_info.get('owner_id') or user_info.get('user_id') or user_info.get('id')

# --- 1. LẤY CHI TIẾT KÈM CÔNG NỢ ---
@customer_bp.route('/<int:id>/summary', methods=['GET'])
@token_required
@inject
def get_customer_summary(id, customer_service: CustomerService = Provide[Container.customer_service]):
    """ Lấy thông tin chi tiết khách hàng kèm theo tổng nợ hiện tại """
    try:
        owner_id = get_owner_id()
        # Service sẽ tổng hợp dữ liệu từ bảng Customers và Invoices
        summary = customer_service.get_customer_financial_summary(id, owner_id)
        
        return jsonify({
            "success": True,
            "data": summary # Gồm: info, total_bought, total_debt, last_transaction
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# --- 2. LỊCH SỬ GIAO DỊCH ---
@customer_bp.route('/<int:id>/transactions', methods=['GET'])
@token_required
@inject
def get_customer_transactions(id, customer_service: CustomerService = Provide[Container.customer_service]):
    """ Lấy lịch sử mua hàng và trả nợ của khách """
    try:
        owner_id = get_owner_id()
        page = request.args.get('page', 1, type=int)
        
        transactions = customer_service.get_transaction_history(id, owner_id, page)
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 3. TÌM KIẾM NHANH (Phục vụ tại quầy) ---
@customer_bp.route('/search', methods=['GET'])
@token_required
@inject
def search_customers(customer_service: CustomerService = Provide[Container.customer_service]):
    """ Tìm nhanh theo tên hoặc số điện thoại """
    try:
        owner_id = get_owner_id()
        query = request.args.get('q', '').strip()
        
        if len(query) < 2:
            return jsonify([]), 200
            
        results = customer_service.search_customers(owner_id, query)
        return jsonify([{
            "id": c.customer_id,
            "name": c.customer_name,
            "phone": c.phone_number,
            "current_debt": getattr(c, 'total_debt', 0)
        } for c in results]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 4. DANH SÁCH KHÁCH NỢ (Debt Management) ---
@customer_bp.route('/debtors', methods=['GET'])
@token_required
@inject
def get_debtors(customer_service: CustomerService = Provide[Container.customer_service]):
    """ Lấy danh sách những khách hàng đang nợ, sắp xếp theo số nợ giảm dần """
    try:
        owner_id = get_owner_id()
        debtors = customer_service.get_list_debtors(owner_id)
        
        return jsonify({
            "total_receivable": sum(d['debt'] for d in debtors),
            "debtors": debtors
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
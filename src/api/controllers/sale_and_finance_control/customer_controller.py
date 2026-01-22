# src/api/controllers/sale_and_finance_control/customer_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.customer_service import CustomerService

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/', methods=['POST'])
@token_required
@inject
def add_new_customer(customer_service: CustomerService = Provide[Container.customer_service]):
    """
    Tạo khách hàng mới
    ---
    tags: [Customer]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          required: [customer_name, phone_number]
          properties:
            customer_name: {type: string}
            phone_number: {type: string}
            address: {type: string}
            email: {type: string}
    responses:
      201: {description: Thành công}
    """
    try:
        data = request.get_json()
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        if not owner_id:
            return jsonify({"error": "Token thiếu owner_id"}), 401

        # SỬA: Truyền data VÀ owner_id tách biệt
        result = customer_service.create_customer(data, owner_id)
        return jsonify({"message": "Thành công", "id": result.customer_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@customer_bp.route('/', methods=['GET'])
@token_required
@inject
def get_all_customers(customer_service: CustomerService = Provide[Container.customer_service]):
    """
    Lấy danh sách khách hàng
    ---
    tags: [Customer]
    security: [{BearerAuth: []}]
    """
    try:
        # FIXED: Xóa current_user khỏi tham số và lấy từ request
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        customers = customer_service.get_all_customers(owner_id)
        return jsonify([{
            "id": c.customer_id, 
            "name": c.customer_name, 
            "phone": c.phone_number,
            "address": c.address
        } for c in customers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customer_bp.route('/<int:id>', methods=['PUT'])
@token_required
@inject
def update_customer(id, customer_service: CustomerService = Provide[Container.customer_service]):
    """Cập nhật khách hàng"""
    try:
        data = request.get_json()
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        # TRUYỀN THÊM owner_id
        customer_service.update_customer(id, data, owner_id)
        return jsonify({"message": "Cập nhật thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@customer_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@inject
def delete_customer(id, customer_service = Provide[Container.customer_service]):
    """Xóa khách hàng"""
    try:
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        # TRUYỀN THÊM owner_id
        customer_service.delete_customer(id, owner_id)
        return jsonify({"message": "Xóa thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
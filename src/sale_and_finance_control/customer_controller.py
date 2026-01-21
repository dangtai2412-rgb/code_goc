from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.customer_service import CustomerService

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/', methods=['POST'])
@token_required
@inject
def add_new_customer(current_user, customer_service: CustomerService = Provide[Container.customer_service]):
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
        # Lấy owner_id từ token người đang đăng nhập
        owner_id = getattr(current_user, 'owner_id', None)
        data['owner_id'] = owner_id
        
        result = customer_service.create_customer(data)
        return jsonify({"message": "Thành công", "id": result.customer_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@customer_bp.route('/', methods=['GET'])
@token_required
@inject
def get_all_customers(current_user, customer_service: CustomerService = Provide[Container.customer_service]):
    """
    Lấy danh sách khách hàng
    ---
    tags: [Customer]
    security: [{BearerAuth: []}]
    """
    try:
        owner_id = getattr(current_user, 'owner_id', None)
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
def update_customer(current_user, id, customer_service: CustomerService = Provide[Container.customer_service]):
    """Cập nhật khách hàng"""
    try:
        data = request.get_json()
        customer_service.update_customer(id, data)
        return jsonify({"message": "Cập nhật thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@customer_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@inject
def delete_customer(id, customer_service = Provide[Container.customer_service]):
    try:
        customer_service.delete_customer(id)
        return jsonify({"message": "Xóa thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
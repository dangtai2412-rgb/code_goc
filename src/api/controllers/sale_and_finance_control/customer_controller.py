from flask import Blueprint, request
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.sale_and_finance_service.customer_service import CustomerService
from api.schemas.customer import CustomerRequestSchema, CustomerResponseSchema
from api.responses import success_response

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
        required: true
        schema:
          $ref: '#/definitions/CustomerRequest'
    responses:
      201:
        description: Tạo thành công
        schema:
          $ref: '#/definitions/CustomerResponse'
    """
    json_data = request.get_json()
    
    # Lấy Owner ID từ Token
    user_info = request.current_user
    owner_id = user_info.get('owner_id') or user_info.get('user_id') or user_info.get('id')
    
    # Inject owner_id để pass Schema validation
    json_data['owner_id'] = owner_id

    # Validate
    schema = CustomerRequestSchema()
    validated_data = schema.load(json_data)
    
    # Call Service
    result = customer_service.create_customer(validated_data, owner_id)
    
    # Response
    return success_response(
        data=CustomerResponseSchema().dump(result), 
        message="Thêm khách hàng thành công", 
        status_code=201
    )

@customer_bp.route('/', methods=['GET'])
@token_required
@inject
def get_all_customers(customer_service: CustomerService = Provide[Container.customer_service]):
    """
    Lấy danh sách khách hàng
    ---
    tags: [Customer]
    security: [{BearerAuth: []}]
    responses:
      200:
        description: OK
        schema:
          type: array
          items:
            $ref: '#/definitions/CustomerResponse'
    """
    user_info = request.current_user
    owner_id = user_info.get('owner_id') or user_info.get('user_id') or user_info.get('id')
    
    customers = customer_service.get_all_customers(owner_id)
    
    return success_response(data=CustomerResponseSchema(many=True).dump(customers))

@customer_bp.route('/<int:id>', methods=['PUT'])
@token_required
@inject
def update_customer(id, customer_service: CustomerService = Provide[Container.customer_service]):
    """Cập nhật khách hàng"""
    # Lưu ý: Với PUT, có thể dùng schema load(partial=True) nếu chỉ update một vài trường
    json_data = request.get_json()
    
    # Logic update thường service sẽ xử lý
    user_info = request.current_user
    owner_id = user_info.get('owner_id') or user_info.get('user_id')
    
    customer_service.update_customer(id, json_data, owner_id)
    
    return success_response(data=None, message="Cập nhật thành công")

@customer_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@inject
def delete_customer(id, customer_service: CustomerService = Provide[Container.customer_service]):
    """Xóa khách hàng"""
    user_info = request.current_user
    owner_id = user_info.get('owner_id') or user_info.get('user_id')
    
    customer_service.delete_customer(id, owner_id)
    return success_response(data=None, message="Xóa thành công")
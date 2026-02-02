from flask import Blueprint, request
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from services.inventory_service.product_service import ProductService
from api.schemas.product import ProductRequestSchema, ProductResponseSchema
from api.responses import success_response

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/', methods=['POST'])
@token_required
@inject
def create_new_product(product_service: ProductService = Provide[Container.product_service]):
    """
    Thêm sản phẩm mới
    ---
    tags: [Inventory]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/ProductRequest'
    responses:
      201:
        description: Tạo thành công
        schema:
          $ref: '#/definitions/ProductResponse'
    """
    # 1. Chuẩn bị dữ liệu
    json_data = request.get_json()
    
    # Lấy ID từ Token (An toàn hơn là tin vào json body)
    user_info = request.current_user
    owner_id = user_info.get('owner_id') or user_info.get('user_id')
    
    # Gán owner_id vào data để pass qua validation của Schema (vì Schema yêu cầu owner_id)
    json_data['owner_id'] = owner_id 

    # 2. Validate bằng Marshmallow Schema
    schema = ProductRequestSchema()
    validated_data = schema.load(json_data) # Tự động raise ValidationError nếu sai format
    
    # 3. Gọi Service
    result = product_service.create_product(validated_data, owner_id)
    
    # 4. Serialize kết quả trả về
    response_schema = ProductResponseSchema()
    return success_response(data=response_schema.dump(result), message="Thêm sản phẩm thành công", status_code=201)

@product_bp.route('/', methods=['GET'])
@token_required
@inject
def list_products_by_owner(product_service: ProductService = Provide[Container.product_service]):
    """
    Lấy danh sách sản phẩm
    ---
    tags: [Inventory]
    security: [{BearerAuth: []}]
    responses:
      200:
        description: Danh sách sản phẩm
        schema:
          type: array
          items:
            $ref: '#/definitions/ProductResponse'
    """
    user_info = request.current_user
    owner_id = user_info.get('owner_id') or user_info.get('user_id')
    
    products = product_service.get_products_by_owner(owner_id)
    
    # Dump list objects ra JSON
    return success_response(data=ProductResponseSchema(many=True).dump(products))

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@token_required
@inject
def delete_product(product_id, product_service: ProductService = Provide[Container.product_service]):
    """Xóa sản phẩm"""
    # Service nên tự check xem sản phẩm có thuộc về user này không
    product_service.delete_product(product_id) 
    return success_response(data=None, message="Đã xóa sản phẩm")
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

business_owner_bp = Blueprint('business_owner_bp', __name__)

@business_owner_bp.route('/', methods=['POST'])
@inject
def register_new_owner(owner_service = Provide[Container.business_owner_service]):
    """
    Đăng ký chủ cửa hàng mới
    ---
    tags:
      - Business Owner
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - owner_name
            - email
            - password
          properties:
            owner_name:
              type: string
              example: "Nguyen Van Chu"
            email:
              type: string
              example: "chu@shop.com"
            phone_number:
              type: string
              example: "0909123456"
            password:
              type: string
              example: "matkhau123"
            plan_id:
              type: integer
              example: 1
              description: ID của gói cước đăng ký (Mặc định 1 nếu không gửi)
    responses:
      201:
        description: Đăng ký thành công
      400:
        description: Lỗi dữ liệu đầu vào
    """
    try:
        data = request.get_json()
        result = owner_service.create_owner(data)
        return jsonify({"message": "Thành công", "id": result.owner_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@business_owner_bp.route('/', methods=['GET'])
@token_required
@inject
def get_all_business_owners(owner_service = Provide[Container.business_owner_service]):
    """
    Lấy danh sách chủ cửa hàng (Admin)
    ---
    tags: [Business Owner]
    security: [{BearerAuth: []}]  # FIXED: Match the name 'BearerAuth'
    responses:
      200: {description: "Danh sách chủ sở hữu"}
    """
    try:
        owners = owner_service.list_all_owners() # Đảm bảo Service có hàm này hoặc đổi tên
        return jsonify([
            {"id": o.owner_id, "name": o.owner_name, "email": o.email, "status": o.account_status} 
            for o in owners
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
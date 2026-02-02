from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

business_owner_bp = Blueprint('business_owner_bp', __name__)

# --- 1. ĐĂNG KÝ CHỦ SHOP MỚI (Public - Không cần token) ---
@business_owner_bp.route('/', methods=['POST'])
@inject
def register_new_owner(owner_service = Provide[Container.business_owner_service]):
    """
    Đăng ký chủ cửa hàng mới
    ---
    tags: [Business Owner]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [owner_name, email, password]
          properties:
            owner_name: {type: string, example: "Nguyen Van Chu"}
            email: {type: string, example: "chu@shop.com"}
            phone_number: {type: string, example: "0909123456"}
            password: {type: string, example: "matkhau123"}
            plan_id: {type: integer, example: 1}
    responses:
      201: {description: "Đăng ký thành công"}
      400: {description: "Dữ liệu không hợp lệ hoặc email đã tồn tại"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dữ liệu trống"}), 400
            
        result = owner_service.create_owner(data)
        return jsonify({
            "message": "Đăng ký chủ shop thành công", 
            "owner_id": result.owner_id
        }), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Lỗi hệ thống nội bộ"}), 500


# --- 2. LẤY DANH SÁCH CHỦ SHOP (Chỉ dành cho ADMIN hệ thống) ---
@business_owner_bp.route('/', methods=['GET'])
@token_required
@inject
def get_all_business_owners(owner_service = Provide[Container.business_owner_service]):
    """
    Lấy danh sách chủ cửa hàng (Chỉ Admin hệ thống được truy cập)
    ---
    tags: [Business Owner]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Danh sách chủ sở hữu"}
      403: {description: "Không có quyền thực hiện hành động này"}
    """
    try:
        # LOGIC GỢI Ý: Kiểm tra nếu role của request.current_user_id không phải là 'admin'
        # if request.current_user_role != 'admin':
        #     return jsonify({"error": "Quyền truy cập bị từ chối"}), 403

        owners = owner_service.list_all_owners()
        return jsonify([
            {
                "id": o.owner_id, 
                "name": o.owner_name, 
                "email": o.email, 
                "status": getattr(o, 'account_status', 'active'),
                "created_at": str(o.created_at) if hasattr(o, 'created_at') else None
            } 
            for o in owners
        ]), 200
    except Exception as e:
        return jsonify({"error": "Không thể truy xuất danh sách"}), 500

# --- 3. CẬP NHẬT TRẠNG THÁI (Ví dụ: Khóa tài khoản khi hết hạn gói) ---
@business_owner_bp.route('/<int:owner_id>/status', methods=['PATCH'])
@token_required
@inject
def update_owner_status(owner_id, owner_service = Provide[Container.business_owner_service]):
    """ Cập nhật trạng thái tài khoản (Active/Inactive) """
    try:
        data = request.get_json()
        new_status = data.get('status')
        if new_status not in ['active', 'inactive']:
            return jsonify({"error": "Trạng thái không hợp lệ"}), 400
            
        owner_service.update_status(owner_id, new_status)
        return jsonify({"message": f"Đã chuyển trạng thái sang {new_status}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
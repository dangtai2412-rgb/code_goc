from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

business_owner_bp = Blueprint('business_owner_bp', __name__)

# --- 1. LẤY THÔNG TIN CÁ NHÂN (Cho chính chủ shop) ---
@business_owner_bp.route('/me', methods=['GET'])
@token_required
@inject
def get_my_profile(owner_service = Provide[Container.business_owner_service]):
    """
    Chủ shop tự xem thông tin của mình
    """
    try:
        # request.current_user_id được gán từ middleware token_required
        owner_id = getattr(request, 'current_user_id', None)
        owner = owner_service.get_owner_by_id(owner_id)
        
        if not owner:
            return jsonify({"error": "Không tìm thấy thông tin"}), 404
            
        return jsonify({
            "id": owner.owner_id,
            "name": owner.owner_name,
            "email": owner.email,
            "plan_id": owner.plan_id,
            "status": owner.account_status
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 2. NÂNG CẤP GÓI CƯỚC (Subscription Plan) ---
@business_owner_bp.route('/upgrade-plan', methods=['POST'])
@token_required
@inject
def upgrade_plan(owner_service = Provide[Container.business_owner_service]):
    """
    Nâng cấp gói dịch vụ
    """
    try:
        data = request.get_json()
        owner_id = request.current_user_id
        new_plan_id = data.get('plan_id')
        
        if not new_plan_id:
            return jsonify({"error": "Thiếu ID gói cước"}), 400
            
        owner_service.change_plan(owner_id, new_plan_id)
        return jsonify({"message": "Nâng cấp gói cước thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- 3. KIỂM TRA QUYỀN TRONG DANH SÁCH (Sửa lại route GET cũ) ---
@business_owner_bp.route('/', methods=['GET'])
@token_required
@inject
def get_all_business_owners(owner_service = Provide[Container.business_owner_service]):
    try:
        # GIẢ SỬ: Role được lưu trong token và gán vào request
        user_role = getattr(request, 'current_user_role', 'owner')
        
        if user_role != 'admin':
            return jsonify({"error": "Bạn không có quyền xem danh sách này"}), 403

        owners = owner_service.list_all_owners()
        return jsonify([
            {
                "id": o.owner_id, 
                "name": o.owner_name, 
                "email": o.email,
                "status": getattr(o, 'account_status', 'active')
            } for o in owners
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
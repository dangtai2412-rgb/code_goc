from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
from datetime import datetime

subscription_plan_bp = Blueprint('subscription_plan_bp', __name__)

# --- 5. ĐĂNG KÝ/GIA HẠN GÓI (Checkout) ---
@subscription_plan_bp.route('/subscribe', methods=['POST'])
@token_required
@inject
def subscribe_to_plan(plan_service: any = Provide[Container.subscription_plan_service]):
    """
    Chủ shop thực hiện đăng ký hoặc gia hạn một gói cước
    Body: { "plan_id": 1 }
    """
    try:
        current_user = getattr(request, 'current_user', {})
        # Chỉ Owner mới được mua gói
        if current_user.get('role') != 'owner':
            return jsonify({"error": "Chỉ chủ cửa hàng mới có quyền mua gói cước"}), 403

        data = request.get_json()
        plan_id = data.get('plan_id')
        owner_id = current_user.get('id')

        if not plan_id:
            return jsonify({"error": "Vui lòng chọn một gói cước"}), 400

        # Service xử lý: 
        # 1. Lấy duration của plan_id
        # 2. Cập nhật expired_date = datetime.now() + duration
        # 3. Ghi log giao dịch/hóa đơn
        result = plan_service.assign_plan_to_owner(owner_id, plan_id)
        
        return jsonify({
            "message": "Đăng ký gói cước thành công",
            "expired_at": result.expired_at.strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Lỗi quá trình thanh toán"}), 500

# --- 6. KIỂM TRA TRẠNG THÁI GÓI HIỆN TẠI ---
@subscription_plan_bp.route('/my-subscription', methods=['GET'])
@token_required
@inject
def get_my_subscription(plan_service: any = Provide[Container.subscription_plan_service]):
    """ Xem thông tin gói hiện tại và ngày hết hạn """
    try:
        owner_id = getattr(request, 'current_user', {}).get('id')
        sub_info = plan_service.get_owner_subscription(owner_id)
        
        if not sub_info:
            return jsonify({"error": "Bạn chưa đăng ký gói cước nào"}), 404

        # Tính toán số ngày còn lại
        remaining_days = (sub_info.expired_at - datetime.now()).days
        
        return jsonify({
            "plan_name": sub_info.plan.plan_name,
            "expired_at": sub_info.expired_at.strftime("%Y-%m-%d"),
            "remaining_days": max(0, remaining_days),
            "status": "active" if remaining_days > 0 else "expired",
            "limits": {
                "max_employees": sub_info.plan.max_employees,
                "max_products": sub_info.plan.max_products
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 7. NGỪNG KÍCH HOẠT GÓI (Admin) ---
@subscription_plan_bp.route('/<int:plan_id>/deactivate', methods=['PUT'])
@token_required
@inject
def deactivate_plan(plan_id, plan_service: any = Provide[Container.subscription_plan_service]):
    """ Ngừng cung cấp gói cước này cho người dùng mới """
    try:
        if getattr(request, 'current_user', {}).get('role') != 'admin':
            return jsonify({"error": "Quyền bị từ chối"}), 403

        plan_service.toggle_plan_status(plan_id, active=False)
        return jsonify({"message": "Gói cước đã được ẩn khỏi danh sách đăng ký"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

subscription_plan_bp = Blueprint('subscription_plan_bp', __name__)

# --- 1. TẠO GÓI CƯỚC (Chỉ Admin) ---
@subscription_plan_bp.route('/', methods=['POST'])
@token_required
@inject
def create_new_subscription_plan(plan_service: any = Provide[Container.subscription_plan_service]):
    try:
        user_info = getattr(request, 'current_user', {})
        if user_info.get('role') != 'admin':
            return jsonify({"error": "Quyền bị từ chối"}), 403

        data = request.get_json()
        if not data:
            return jsonify({"error": "Dữ liệu không được để trống"}), 400
            
        # Kiểm tra validation cơ bản
        required = ['plan_name', 'price', 'duration']
        if not all(k in data for k in required):
            return jsonify({"error": f"Thiếu trường bắt buộc: {required}"}), 400

        result = plan_service.create_plan(data)
        return jsonify({
            "message": "Thành công", 
            "id": result.plan_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- 2. LẤY DANH SÁCH (Public) ---
@subscription_plan_bp.route('/', methods=['GET'])
@inject
def list_all_plans(plan_service: any = Provide[Container.subscription_plan_service]):
    try:
        plans = plan_service.list_active_plans() 
        
        return jsonify([
            {
                "id": p.plan_id, 
                "name": p.plan_name, 
                "price": float(p.price) if p.price else 0,
                "duration": getattr(p, 'duration_days', getattr(p, 'duration', 30)), # Fix lỗi sai tên trường
                "description": p.description,
                "limits": {
                    "max_employees": getattr(p, 'max_employees', 5),
                    "max_branches": getattr(p, 'max_branches', 1),
                    "max_products": getattr(p, 'max_products', 100)
                }
            } for p in plans
        ]), 200
    except Exception as e:
        return jsonify({"error": "Lỗi tải danh sách gói cước"}), 500

# --- 3. LẤY CHI TIẾT 1 GÓI (Tính năng bổ sung) ---
@subscription_plan_bp.route('/<int:plan_id>', methods=['GET'])
@inject
def get_plan_detail(plan_id, plan_service: any = Provide[Container.subscription_plan_service]):
    try:
        p = plan_service.get_plan_by_id(plan_id)
        if not p:
            return jsonify({"error": "Không tìm thấy gói cước"}), 404
        return jsonify({"id": p.plan_id, "name": p.plan_name, "price": float(p.price)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 4. CẬP NHẬT/ẨN (Chỉ Admin) ---
@subscription_plan_bp.route('/<int:plan_id>', methods=['PATCH'])
@token_required
@inject
def update_plan(plan_id, plan_service: any = Provide[Container.subscription_plan_service]):
    try:
        if getattr(request, 'current_user', {}).get('role') != 'admin':
            return jsonify({"error": "Quyền bị từ chối"}), 403

        data = request.get_json()
        plan_service.update_plan(plan_id, data)
        return jsonify({"message": "Cập nhật thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
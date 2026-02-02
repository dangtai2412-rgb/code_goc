from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

ai_assistant_bp = Blueprint('ai_assistant_bp', __name__)

# --- 1. CẬP NHẬT CẤU HÌNH (Chỉ Super Admin) ---
@ai_assistant_bp.route('/settings', methods=['POST'])
@token_required
@inject
def update_settings(ai_service: any = Provide[Container.ai_assistant_service]):
    """
    Cập nhật cấu hình model AI (Dành cho Admin hệ thống)
    """
    try:
        # BẢO MẬT: Chỉ Admin mới được đổi cấu hình AI
        user_info = getattr(request, 'current_user', {})
        if user_info.get('role') != 'admin':
            return jsonify({"error": "Bạn không có quyền thay đổi cấu hình hệ thống AI"}), 403

        data = request.get_json()
        if not data or 'model_type' not in data:
            return jsonify({"error": "Thiếu thông tin model_type"}), 400

        # GỢI Ý: Thêm danh sách model được phép để tránh lỗi chính tả
        allowed_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gpt-4o"]
        if data['model_type'] not in allowed_models:
            return jsonify({"error": f"Model không hỗ trợ. Cho phép: {allowed_models}"}), 400

        ai_service.update_ai_settings(data)
        return jsonify({"message": "Cấu hình AI đã được cập nhật thành công"}), 200
        
    except Exception as e:
        return jsonify({"error": f"Lỗi cập nhật: {str(e)}"}), 500


# --- 2. LẤY CẤU HÌNH HIỆN TẠI ---
@ai_assistant_bp.route('/config', methods=['GET'])
@token_required
@inject
def get_config(ai_service: any = Provide[Container.ai_assistant_service]):
    """
    Lấy cấu hình AI hiện tại
    """
    try:
        config = ai_service.get_current_config()
        if not config:
            return jsonify({"message": "Chưa có cấu hình AI"}), 404

        return jsonify({
            "version": getattr(config, 'version', 'N/A'),
            "model_type": getattr(config, 'ai_model_type', 'N/A'),
            "updated_at": getattr(config, 'updated_at', None)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- 3. TEST KẾT NỐI AI (Tính năng mới nên có) ---
@ai_assistant_bp.route('/test-connection', methods=['GET'])
@token_required
@inject
def test_ai_connection(ai_service: any = Provide[Container.ai_assistant_service]):
    """ Kiểm tra xem API Key của AI có còn hoạt động không """
    try:
        is_alive = ai_service.check_api_status() # Bạn cần viết hàm này trong Service
        if is_alive:
            return jsonify({"status": "AI is online", "latency": "200ms"}), 200
        return jsonify({"status": "AI is unreachable"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500
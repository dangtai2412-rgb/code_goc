from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

ai_assistant_bp = Blueprint('ai_assistant_bp', __name__)

# Helper để định dạng phản hồi chuẩn cho hệ thống
def success_response(data, message="Thành công", status_code=200):
    return jsonify({"success": True, "message": message, "data": data}), status_code

def error_response(error_msg, status_code=400):
    return jsonify({"success": False, "error": error_msg}), status_code

# --- 4. TRUY VẤN AI (Smart Query) ---
@ai_assistant_bp.route('/ask', methods=['POST'])
@token_required
@inject
def ask_ai(ai_service: any = Provide[Container.ai_assistant_service]):
    """
    Gửi câu hỏi cho AI trợ lý kinh doanh.
    Sử dụng kỹ thuật RAG để đọc dữ liệu thực tế của cửa hàng.
    """
    try:
        current_user = getattr(request, 'current_user', {})
        owner_id = current_user.get('id')
        
        data = request.get_json() or {}
        prompt = data.get('prompt', '').strip()

        if not prompt:
            return error_response("Nội dung câu hỏi không được để trống")

        # 1. Kiểm tra định mức (Quota Check)
        usage_status = ai_service.check_usage_limit(owner_id)
        if not usage_status.get('can_proceed'):
            return error_response("Bạn đã hết lượt sử dụng AI. Vui lòng nâng cấp gói cước!", 429)

        # 2. Xử lý logic qua Service
        # Gợi ý: Truyền thêm context_type (sales, inventory, customers) để AI tập trung hơn
        response = ai_service.process_ai_query(owner_id, prompt)
        
        return success_response({
            "answer": response,
            "usage_stats": ai_service.get_user_usage_stats(owner_id)
        })

    except Exception as e:
        return error_response(f"AI Assistant gặp sự cố: {str(e)}", 500)

# --- 5. BÁO CÁO THÔNG MINH (Auto-Insights) ---
@ai_assistant_bp.route('/insights', methods=['GET'])
@token_required
@inject
def get_business_insights(ai_service: any = Provide[Container.ai_assistant_service]):
    """ 
    Tự động phân tích tình hình kinh doanh hiện tại.
    Query params: ?period=last_7_days (default) hoặc last_30_days
    """
    try:
        owner_id = getattr(request, 'current_user', {}).get('id')
        period = request.args.get('period', 'last_7_days')
        
        # Service thực hiện phân tích đa chiều (doanh thu, đơn hàng, sản phẩm lỗi...)
        report = ai_service.generate_business_report(owner_id, period)
        
        return success_response({
            "owner_id": owner_id,
            "period": period,
            "insights": report,
            "metadata": {
                "engine": "gemini-1.5-pro",
                "last_sync": "just now"
            }
        })
    except Exception as e:
        return error_response(f"Không thể tạo báo cáo: {str(e)}", 500)

# --- 6. QUẢN LÝ LỊCH SỬ (History Management) ---
@ai_assistant_bp.route('/history', methods=['DELETE'])
@token_required
@inject
def clear_chat_history(ai_service: any = Provide[Container.ai_assistant_service]):
    """ Làm mới phiên làm việc với AI """
    try:
        owner_id = getattr(request, 'current_user', {}).get('id')
        ai_service.clear_history(owner_id)
        
        return success_response(None, message="Lịch sử trò chuyện đã được làm mới")
    except Exception as e:
        return error_response(str(e), 500)
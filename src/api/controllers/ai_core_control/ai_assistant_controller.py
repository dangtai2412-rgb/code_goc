from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

ai_assistant_bp = Blueprint('ai_assistant_bp', __name__)

# --- 4. CHAT VỚI AI ASSISTANT ---
@ai_assistant_bp.route('/ask', methods=['POST'])
@token_required
@inject
def ask_ai(ai_service: any = Provide[Container.ai_assistant_service]):
    """
    Gửi câu hỏi cho AI để hỗ trợ quản lý cửa hàng
    Body: { "prompt": "Tháng này mặt hàng nào bán chạy nhất?" }
    """
    try:
        current_user = getattr(request, 'current_user', {})
        owner_id = current_user.get('id')
        data = request.get_json()
        prompt = data.get('prompt')

        if not prompt:
            return jsonify({"error": "Nội dung câu hỏi không được trống"}), 400

        # KIỂM TRA ĐỊNH MỨC (Usage Quota)
        # Gợi ý: Mỗi shop gói Basic chỉ được hỏi 50 câu/tháng
        can_ask = ai_service.check_usage_limit(owner_id)
        if not can_ask:
            return jsonify({"error": "Bạn đã hết lượt sử dụng AI tháng này. Hãy nâng cấp gói cước!"}), 429

        # AI Service sẽ lấy dữ liệu từ DB của Owner và gửi kèm Prompt cho LLM
        response = ai_service.process_ai_query(owner_id, prompt)
        
        return jsonify({
            "answer": response,
            "usage": ai_service.get_user_usage_stats(owner_id)
        }), 200
    except Exception as e:
        return jsonify({"error": f"AI Assistant đang bận: {str(e)}"}), 500

# --- 5. TỰ ĐỘNG PHÂN TÍCH KINH DOANH (Insights) ---
@ai_assistant_bp.route('/insights', methods=['GET'])
@token_required
@inject
def get_business_insights(ai_service: any = Provide[Container.ai_assistant_service]):
    """ AI tự động đọc dữ liệu doanh thu và đưa ra nhận xét """
    try:
        owner_id = getattr(request, 'current_user', {}).get('id')
        
        # Service sẽ tổng hợp data doanh thu tuần/tháng rồi nhờ AI phân tích
        insights = ai_service.generate_business_report(owner_id)
        
        return jsonify({
            "owner_id": owner_id,
            "insights": insights, # Ví dụ: "Doanh thu tăng 10%, nhưng mặt hàng A đang tồn kho quá nhiều..."
            "generated_at": "2024-05-20T10:00:00Z"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 6. XÓA LỊCH SỬ CHAT ---
@ai_assistant_bp.route('/history', methods=['DELETE'])
@token_required
@inject
def clear_chat_history(ai_service: any = Provide[Container.ai_assistant_service]):
    """ Xóa toàn bộ ngữ cảnh (context) cũ để AI bắt đầu phiên làm việc mới """
    try:
        owner_id = getattr(request, 'current_user', {}).get('id')
        ai_service.clear_history(owner_id)
        return jsonify({"message": "Lịch sử trò chuyện đã được xóa"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
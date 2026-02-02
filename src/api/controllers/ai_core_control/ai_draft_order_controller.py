from flask import Blueprint, json, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

ai_draft_order_bp = Blueprint('ai_draft_order_bp', __name__)

def get_auth_ids():
    user_info = getattr(request, 'current_user', {})
    return {
        "user_id": user_info.get('id'),
        "owner_id": user_info.get('owner_id') or user_info.get('id')
    }

# --- 1. GỬI LỆNH THOẠI / VĂN BẢN ---
@ai_draft_order_bp.route('/', methods=['POST'])
@token_required
@inject
def post_voice_command(ai_service = Provide[Container.ai_draft_order_service]):
    try:
        data = request.get_json()
        voice_content = data.get('voice_content', '').strip()
        
        if not voice_content:
            return jsonify({"error": "Vui lòng nhập nội dung lệnh thoại"}), 400
            
        auth = get_auth_ids()
        
        # Service sẽ gọi LLM (Gemini/GPT) để bóc tách thông tin
        result = ai_service.create_draft_from_voice(voice_content, auth['user_id'], auth['owner_id'])
        
        return jsonify({
            "success": True,
            "draft_id": result.draft_id,
            "extracted_data": json.loads(result.extracted_json) if result.extracted_json else {},
            "confidence_score": getattr(result, 'confidence', 1.0) # Độ tin cậy của AI
        }), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 422 # Lỗi dữ liệu AI không hiểu được
    except Exception as e:
        return jsonify({"error": "Hệ thống AI đang bận, vui lòng thử lại"}), 500

# --- 2. CẬP NHẬT ĐƠN NHÁP (Quan trọng: Để sửa sai cho AI) ---
@ai_draft_order_bp.route('/<int:draft_id>', methods=['PATCH'])
@token_required
@inject
def update_draft(draft_id, ai_service = Provide[Container.ai_draft_order_service]):
    """ Nhân viên sửa lại thông tin AI bóc tách sai trước khi lưu thật """
    try:
        data = request.get_json()
        auth = get_auth_ids()
        
        # data thường là JSON của extracted_data đã sửa
        updated_draft = ai_service.update_draft_content(draft_id, data, auth['owner_id'])
        
        return jsonify({"message": "Đã cập nhật bản nháp", "data": updated_draft.extracted_json}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- 3. XÁC NHẬN ĐƠN NHÁP ---
@ai_draft_order_bp.route('/<int:draft_id>/confirm', methods=['POST'])
@token_required
@inject
def confirm_draft(draft_id, ai_service = Provide[Container.ai_draft_order_service]):
    try:
        auth = get_auth_ids()
        
        # Logic: Draft -> Real Order -> Cập nhật kho -> Trừ nợ khách hàng
        order = ai_service.confirm_and_create_order(
            draft_id=draft_id, 
            emp_id=auth['user_id'], 
            owner_id=auth['owner_id']
        )
        
        return jsonify({
            "success": True,
            "order_id": order.order_id,
            "customer": order.customer_name,
            "total_amount": float(order.total_price)
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Không thể tạo hóa đơn: {str(e)}"}), 400

# --- 4. DANH SÁCH & XÓA ---
@ai_draft_order_bp.route('/', methods=['GET'])
@token_required
@inject
def get_drafts(ai_service = Provide[Container.ai_draft_order_service]):
    auth = get_auth_ids()
    drafts = ai_service.get_pending_drafts_by_owner(auth['owner_id'])
    return jsonify([{
        "id": d.draft_id,
        "text": d.raw_text,
        "data": json.loads(d.extracted_json) if d.extracted_json else None,
        "status": d.status
    } for d in drafts]), 200
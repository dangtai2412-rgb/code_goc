from flask import Blueprint, json, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

ai_draft_order_bp = Blueprint('ai_draft_order_bp', __name__)

def get_auth_ids():
    """Helper lấy thông tin định danh từ token"""
    user_info = getattr(request, 'current_user', {})
    # user_id là người thực hiện (NV), owner_id là mã shop
    return {
        "user_id": user_info.get('id'),
        "owner_id": user_info.get('owner_id') or user_info.get('id'),
        "role": user_info.get('role')
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
            return jsonify({"error": "Nội dung không được để trống"}), 400
            
        auth = get_auth_ids()
        
        # AI xử lý trích xuất thực thể (Sản phẩm, Số lượng, Khách hàng)
        result = ai_service.create_draft_from_voice(
            voice_content, 
            auth['user_id'], 
            auth['owner_id']
        )
        
        return jsonify({
            "success": True,
            "draft_id": result.draft_id,
            "extracted_data": json.loads(result.extracted_json) if result.extracted_json else {},
            "message": "Đã tạo đơn nháp từ AI"
        }), 201
    except Exception as e:
        return jsonify({"error": f"Lỗi xử lý AI: {str(e)}"}), 500

# --- 2. LẤY DANH SÁCH ĐƠN NHÁP (Theo Shop) ---
@ai_draft_order_bp.route('/', methods=['GET'])
@token_required
@inject
def get_drafts(ai_service = Provide[Container.ai_draft_order_service]):
    try:
        auth = get_auth_ids()
        # Quan trọng: Chỉ lấy đơn nháp thuộc về shop hiện tại
        drafts = ai_service.get_pending_drafts_by_owner(auth['owner_id'])
        
        return jsonify([{
            "id": d.draft_id,
            "raw_text": d.raw_text,
            "extracted_json": json.loads(d.extracted_json) if d.extracted_json else None,
            "status": d.status,
            "created_by": d.employee_id,
            "created_at": d.created_at.isoformat()
        } for d in drafts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 3. XÁC NHẬN ĐƠN NHÁP ---
@ai_draft_order_bp.route('/<int:draft_id>/confirm', methods=['POST'])
@token_required
@inject
def confirm_draft(draft_id, ai_service = Provide[Container.ai_draft_order_service]):
    """ Xác nhận đơn nháp để trừ kho và ghi công nợ """
    try:
        auth = get_auth_ids()
        
        # Service thực hiện: Trừ kho -> Tạo Invoice -> Ghi nợ -> Đổi trạng thái Draft
        order = ai_service.confirm_and_create_order(
            draft_id=draft_id, 
            emp_id=auth['user_id'], 
            owner_id=auth['owner_id']
        )
        
        return jsonify({
            "success": True,
            "message": "Đã tạo hóa đơn thành công", 
            "order_id": order.order_id
        }), 201
        
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Lỗi xác nhận đơn hàng"}), 500

# --- 4. HỦY ĐƠN NHÁP (Tính năng mới nên có) ---
@ai_draft_order_bp.route('/<int:draft_id>', methods=['DELETE'])
@token_required
@inject
def delete_draft(draft_id, ai_service = Provide[Container.ai_draft_order_service]):
    try:
        auth = get_auth_ids()
        ai_service.cancel_draft(draft_id, auth['owner_id'])
        return jsonify({"message": "Đã xóa bản nháp"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
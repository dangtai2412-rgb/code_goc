# --- 5. GHI NHẬN TRẢ NỢ (Repayment) ---
@customer_bp.route('/<int:id>/repayment', methods=['POST'])
@token_required
@inject
def record_repayment(id, customer_service: CustomerService = Provide[Container.customer_service]):
    """ Ghi nhận khách hàng trả nợ (phiếu thu) """
    try:
        data = request.get_json()
        amount = data.get('amount', 0)
        payment_method = data.get('payment_method', 'cash') # cash, transfer
        
        if amount <= 0:
            return jsonify({"error": "Số tiền trả nợ phải lớn hơn 0"}), 400
            
        owner_id = get_owner_id()
        # Cập nhật số dư nợ trong Database
        repayment_receipt = customer_service.process_repayment(id, owner_id, amount, payment_method)
        
        return jsonify({
            "success": True,
            "message": f"Đã ghi nhận trả nợ {amount}",
            "receipt_id": repayment_receipt.id,
            "remaining_debt": repayment_receipt.new_balance
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- 6. PHÂN NHÓM KHÁCH HÀNG (AI Insights) ---
@customer_bp.route('/segments', methods=['GET'])
@token_required
@inject
def get_customer_segments(customer_service: CustomerService = Provide[Container.customer_service]):
    """ 
    Phân tích hành vi khách hàng bằng AI 
    Nhóm: VIP, Thường xuyên, Nguy cơ rời bỏ, Nợ khó đòi
    """
    try:
        owner_id = get_owner_id()
        segments = customer_service.get_ai_customer_segments(owner_id)
        
        return jsonify({
            "summary": {
                "total_vip": len(segments.get('vip', [])),
                "at_risk": len(segments.get('at_risk', []))
            },
            "segments": segments
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 7. TẠO TIN NHẮN NHẮC NỢ (Automation) ---
@customer_bp.route('/<int:id>/debt-reminder', methods=['GET'])
@token_required
@inject
def get_debt_reminder(id, customer_service: CustomerService = Provide[Container.customer_service]):
    """ Tạo mẫu tin nhắn nhắc nợ cá nhân hóa """
    try:
        owner_id = get_owner_id()
        # Lấy thông tin nợ và tạo nội dung: "Chào anh A, shop BizFlow gửi thông báo số nợ..."
        reminder_content = customer_service.generate_debt_reminder(id, owner_id)
        
        return jsonify({
            "customer_phone": reminder_content['phone'],
            "message": reminder_content['text'],
            "zalo_link": f"https://zalo.me/{reminder_content['phone']}"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
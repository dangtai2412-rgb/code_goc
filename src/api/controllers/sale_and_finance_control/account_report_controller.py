# --- 7. CHẤM ĐIỂM TÍN NHIỆM KHÁCH NỢ (Risk Support) ---
@account_report_bp.route('/customer-risk/<int:customer_id>', methods=['GET'])
@token_required
@inject
def get_customer_risk_profile(customer_id, service: AccountReportService = Provide[Container.account_report_service]):
    """ 
    Phân tích lịch sử trả nợ để cảnh báo mức độ rủi ro 
    Giúp chủ shop quyết định có cho "ghi nợ" tiếp hay không.
    """
    try:
        owner_id = get_owner_id()
        # Tính toán dựa trên: số lần trả chậm, tổng nợ hiện tại, thời gian nợ lâu nhất
        risk_profile = service.analyze_customer_debt_behavior(owner_id, customer_id)
        
        return jsonify({
            "customer_id": customer_id,
            "risk_level": risk_profile['level'], # "Low", "Medium", "High"
            "score": risk_profile['score'],      # 0 - 100
            "advice": risk_profile['advice'],    # "Nên thu tiền mặt đơn này"
            "debt_summary": risk_profile['summary']
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- 8. ĐĂNG KÝ NHẬN BÁO CÁO QUA TELEGRAM/ZALO (Notification Support) ---
@account_report_bp.route('/notifications/subscribe', methods=['POST'])
@token_required
@inject
def subscribe_daily_report(service: AccountReportService = Provide[Container.account_report_service]):
    """ Đăng ký nhận tóm tắt doanh thu mỗi tối qua kênh chat """
    try:
        data = request.get_json()
        owner_id = get_owner_id()
        channel = data.get('channel') # 'telegram', 'zalo', 'push'
        chat_id = data.get('chat_id')
        
        service.register_report_subscription(owner_id, channel, chat_id)
        
        return jsonify({"message": f"Đã đăng ký nhận báo cáo hàng ngày qua {channel}"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- 9. KIỂM TRA SỨC KHỎE TỔN KHO (Inventory Health) ---
@account_report_bp.route('/inventory/health', methods=['GET'])
@token_required
@inject
def get_inventory_health(service: AccountReportService = Provide[Container.account_report_service]):
    """ Cảnh báo hàng tồn lâu ngày (Deadstock) hoặc sắp hết hàng """
    try:
        owner_id = get_owner_id()
        # Tìm các mặt hàng > 60 ngày không có đơn phát sinh
        deadstock = service.get_deadstock_list(owner_id)
        # Tìm các mặt hàng dưới ngưỡng tối thiểu
        low_stock = service.get_low_stock_alerts(owner_id)
        
        return jsonify({
            "deadstock_count": len(deadstock),
            "deadstock_value": sum(item.value for item in deadstock),
            "low_stock_alerts": low_stock,
            "suggestion": "Bạn nên chạy chương trình khuyến mãi cho nhóm hàng tồn lâu để thu hồi vốn."
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
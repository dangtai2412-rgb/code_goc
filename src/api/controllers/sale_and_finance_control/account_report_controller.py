# --- 4. TRỢ LÝ AI NHẬN XÉT BÁO CÁO ---
@account_report_bp.route('/ai-commentary', methods=['GET'])
@token_required
@inject
def get_ai_report_commentary(
    service: AccountReportService = Provide[Container.account_report_service],
    ai_service: any = Provide[Container.ai_assistant_service]
):
    """ AI đọc số liệu báo cáo và đưa ra lời khuyên kinh doanh """
    try:
        owner_id = get_owner_id()
        # 1. Lấy dữ liệu thô từ Service báo cáo
        raw_data = service.get_dashboard_with_growth(owner_id, 'this_month')
        
        # 2. Gửi dữ liệu sang AI Service để "dịch" thành văn bản
        # Ví dụ: "Doanh thu của bạn tăng 10%, nhưng chi phí vận hành đang quá cao..."
        commentary = ai_service.generate_report_insight(raw_data)
        
        return jsonify({
            "success": True,
            "commentary": commentary,
            "suggestions": ["Cần giảm tồn kho mặt hàng A", "Tăng cường thu hồi công nợ nhóm B"]
        }), 200
    except Exception as e:
        return jsonify({"error": "AI đang bận phân tích dữ liệu"}), 500

# --- 5. CẢNH BÁO NGƯỠNG THUẾ (Tax Compliance Support) ---
@account_report_bp.route('/tax-alerts', methods=['GET'])
@token_required
@inject
def get_tax_alerts(service: AccountReportService = Provide[Container.account_report_service]):
    """ Cảnh báo khi doanh thu tiến sát ngưỡng 100 triệu/năm hoặc các mốc thuế quan trọng """
    try:
        owner_id = get_owner_id()
        # Tính tổng doanh thu lũy kế từ đầu năm
        yearly_revenue = service.get_yearly_accumulated_revenue(owner_id)
        
        # Ngưỡng nộp thuế tại VN thường là 100tr/năm
        threshold = 100000000 
        status = "safe"
        if yearly_revenue >= threshold * 0.9:
            status = "warning"
        if yearly_revenue >= threshold:
            status = "taxable"

        return jsonify({
            "current_yearly_revenue": yearly_revenue,
            "threshold": threshold,
            "status": status,
            "message": "Bạn sắp đạt ngưỡng doanh thu phải kê khai thuế GTGT." if status == "warning" else "Ổn định"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 6. DỰ BÁO DÒNG TIỀN (Cash Flow Support) ---
@account_report_bp.route('/cashflow/forecast', methods=['GET'])
@token_required
@inject
def get_cashflow_forecast(service: AccountReportService = Provide[Container.account_report_service]):
    """ Dự báo số tiền sẽ thu được trong 7 ngày tới dựa trên công nợ sắp đến hạn """
    try:
        owner_id = get_owner_id()
        # Lấy danh sách các khoản phải thu từ khách hàng sắp đến ngày hẹn trả
        forecast = service.calculate_incoming_cashflow(owner_id)
        
        return jsonify({
            "expected_incoming": forecast['total'],
            "details": forecast['by_date'], # List: [{"date": "2024-06-01", "amount": 5000000}, ...]
            "recommendation": "Bạn nên đôn đốc khách hàng A trả nợ để đủ tiền nhập hàng vào thứ 4."
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
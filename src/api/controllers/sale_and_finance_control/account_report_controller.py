from flask import Blueprint, request, jsonify, send_file
from api.middlewares.auth_middleware import token_required
from services.sale_and_finance_service.account_report_service import AccountReportService
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
import io

account_report_bp = Blueprint('account_report_bp', __name__)

def get_owner_id():
    user_info = getattr(request, 'current_user', {})
    return user_info.get('owner_id') or user_info.get('id')

# --- 1. BÁO CÁO KẾ TOÁN (TT88) ---
@account_report_bp.route('/tt88/s1', methods=['GET'])
@token_required
@inject
def get_s1_report(service: AccountReportService = Provide[Container.account_report_service]):
    """ 
    Sổ chi tiết doanh thu bán hàng hóa, dịch vụ (Mẫu S1-HKD) 
    Query: ?start_date=...&end_date=...&export=excel
    """
    try:
        owner_id = get_owner_id()
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        export_format = request.args.get('export') # 'excel' hoặc None

        if not start_date or not end_date:
            return jsonify({"error": "Vui lòng chọn khoảng thời gian báo cáo"}), 400

        # Nếu yêu cầu xuất file Excel cho kế toán
        if export_format == 'excel':
            excel_data = service.export_s1_to_excel(owner_id, start_date, end_date)
            return send_file(
                io.BytesIO(excel_data),
                as_attachment=True,
                download_name=f"So_S1_DoanhThu_{start_date}_den_{end_date}.xlsx",
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        report = service.generate_s1_revenue_ledger(owner_id, start_date, end_date)
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": f"Lỗi tạo báo cáo: {str(e)}"}), 500

# --- 2. THỐNG KÊ DASHBOARD (KPIs) ---
@account_report_bp.route('/dashboard', methods=['GET'])
@token_required
@inject
def get_dashboard_stats(service: AccountReportService = Provide[Container.account_report_service]):
    """ Thống kê tổng quan: Doanh thu, Lợi nhuận, Đơn hàng """
    try:
        owner_id = get_owner_id()
        # Cho phép filter theo range (today, this_month, last_30_days)
        period = request.args.get('period', 'this_month')
        
        data = service.get_dashboard_stats(owner_id, period)
        return jsonify({
            "success": True,
            "period": period,
            "summary": data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 3. BIỂU ĐỒ & TOP SẢN PHẨM ---
@account_report_bp.route('/analytics', methods=['GET'])
@token_required
@inject
def get_combined_analytics(service: AccountReportService = Provide[Container.account_report_service]):
    """ Gộp dữ liệu biểu đồ và top sản phẩm để giảm số lần gọi API từ Mobile/Web """
    try:
        owner_id = get_owner_id()
        
        revenue_chart = service.get_revenue_chart(owner_id)
        top_products = service.get_top_products(owner_id)
        
        return jsonify({
            "charts": revenue_chart,
            "top_selling": top_products
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
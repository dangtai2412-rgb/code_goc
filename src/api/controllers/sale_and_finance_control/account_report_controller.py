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

# --- 1. SỔ DOANH THU (S1) & SỔ KHO (S2) ---
@account_report_bp.route('/tt88/<report_type>', methods=['GET'])
@token_required
@inject
def get_accounting_reports(report_type, service: AccountReportService = Provide[Container.account_report_service]):
    """ 
    Hỗ trợ cả S1 (Doanh thu) và S2 (Nhập Xuất Tồn)
    URL: /tt88/s1 hoặc /tt88/s2
    """
    try:
        owner_id = get_owner_id()
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        export = request.args.get('export')

        if not start_date or not end_date:
            return jsonify({"error": "Thiếu khoảng thời gian báo cáo"}), 400

        if report_type not in ['s1', 's2']:
            return jsonify({"error": "Loại báo cáo không hợp lệ"}), 404

        # Xử lý xuất Excel
        if export == 'excel':
            excel_data = service.export_report_to_excel(report_type, owner_id, start_date, end_date)
            return send_file(
                io.BytesIO(excel_data),
                as_attachment=True,
                download_name=f"Bao_cao_{report_type}_{start_date}.xlsx",
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        # Trả về JSON cho Web/App hiển thị
        report_data = service.generate_report_data(report_type, owner_id, start_date, end_date)
        return jsonify(report_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 2. DASHBOARD VỚI TÍNH TOÁN TĂNG TRƯỞNG ---
@account_report_bp.route('/dashboard', methods=['GET'])
@token_required
@inject
def get_dashboard_summary(service: AccountReportService = Provide[Container.account_report_service]):
    """ Thống kê kèm theo % tăng trưởng so với kỳ trước """
    try:
        owner_id = get_owner_id()
        # Mặc định lấy theo tháng hiện tại
        period = request.args.get('period', 'this_month')
        
        # Service sẽ trả về: { "total_revenue": 100M, "growth_rate": 15.5, ... }
        stats = service.get_dashboard_with_growth(owner_id, period)
        
        return jsonify({
            "success": True,
            "data": stats
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 3. PHÂN TÍCH SÂU (BI Analytics) ---
@account_report_bp.route('/analytics/revenue-structure', methods=['GET'])
@token_required
@inject
def get_revenue_structure(service: AccountReportService = Provide[Container.account_report_service]):
    """ Phân tích cơ cấu doanh thu theo danh mục sản phẩm hoặc phương thức thanh toán """
    try:
        owner_id = get_owner_id()
        # Giúp chủ shop biết họ thu tiền mặt nhiều hay chuyển khoản nhiều
        structure = service.get_payment_method_distribution(owner_id)
        return jsonify(structure), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
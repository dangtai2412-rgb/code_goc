from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from services.sale_and_finance_service.account_report_service import AccountReportService
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

account_report_bp = Blueprint('account_report_bp', __name__)

@account_report_bp.route('/tt88', methods=['GET'])
@token_required
@inject
def get_tt88_report(current_user, service: AccountReportService = Provide[Container.account_report_service]):
    """
    Lấy báo cáo Sổ chi tiết doanh thu (Thông tư 88)
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    parameters:
      - name: date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD
    responses:
      200: {description: "Thành công"}
    """
    try:
        owner_id = getattr(current_user, 'owner_id', None) or getattr(current_user, 'user_id', None)
        report_date = request.args.get('date')
        
        if not report_date:
            return jsonify({"error": "Vui lòng chọn ngày báo cáo (?date=...)"}), 400
            
        # FIXED: Use 'service' instead of 'report_service'
        report_data = service.generate_daily_report(owner_id, report_date)
        return jsonify(report_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@account_report_bp.route('/dashboard', methods=['GET'])
@token_required
@inject
def get_dashboard_stats(current_user, service: AccountReportService = Provide[Container.account_report_service]):
    """
    Lấy thống kê Dashboard (Doanh thu, Đơn hàng, Tồn kho)
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Thành công"}
    """
    try:
        owner_id = getattr(current_user, 'owner_id', None) or getattr(current_user, 'user_id', None)
        data = service.get_dashboard_stats(owner_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@account_report_bp.route('/chart', methods=['GET'])
@token_required
@inject
def get_chart_data(current_user, service: AccountReportService = Provide[Container.account_report_service]):
    """
    Lấy dữ liệu biểu đồ doanh thu 7 ngày
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Thành công"}
    """
    try:
        owner_id = getattr(current_user, 'owner_id', None) or getattr(current_user, 'user_id', None)
        data = service.get_revenue_chart(owner_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@account_report_bp.route('/top-products', methods=['GET'])
@token_required
@inject
def get_top_products(current_user, service: AccountReportService = Provide[Container.account_report_service]):
    """
    Lấy Top 5 sản phẩm bán chạy
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Thành công"}
    """
    try:
        owner_id = getattr(current_user, 'owner_id', None) or getattr(current_user, 'user_id', None)
        data = service.get_top_products(owner_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
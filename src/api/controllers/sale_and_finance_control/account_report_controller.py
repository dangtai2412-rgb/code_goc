# src/api/controllers/sale_and_finance_control/account_report_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from services.sale_and_finance_service.account_report_service import AccountReportService
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

account_report_bp = Blueprint('account_report_bp', __name__)

@account_report_bp.route('/tt88', methods=['GET'])
@token_required
@inject
def get_tt88_report(service: AccountReportService = Provide[Container.account_report_service]):
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
        # FIXED: Lấy thông tin từ request object (là Dictionary từ JWT)
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        report_date = request.args.get('date')
        
        if not report_date:
            return jsonify({"error": "Vui lòng chọn ngày báo cáo (?date=...)"}), 400
            
        report_data = service.generate_daily_report(owner_id, report_date)
        return jsonify(report_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@account_report_bp.route('/dashboard', methods=['GET'])
@token_required
@inject
def get_dashboard_stats(service: AccountReportService = Provide[Container.account_report_service]):
    """
    Lấy thống kê Dashboard (Doanh thu, Đơn hàng, Tồn kho)
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Thành công"}
    """
    try:
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        data = service.get_dashboard_stats(owner_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@account_report_bp.route('/chart', methods=['GET'])
@token_required
@inject
def get_chart_data(service: AccountReportService = Provide[Container.account_report_service]):
    """
    Lấy dữ liệu biểu đồ doanh thu 7 ngày
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Thành công"}
    """
    try:
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        data = service.get_revenue_chart(owner_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@account_report_bp.route('/top-products', methods=['GET'])
@token_required
@inject
def get_top_products(service: AccountReportService = Provide[Container.account_report_service]):
    """
    Lấy Top 5 sản phẩm bán chạy
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    responses:
      200: {description: "Thành công"}
    """
    try:
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        data = service.get_top_products(owner_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
@account_report_bp.route('/tt88/s1', methods=['GET'])
@token_required
@inject
def get_s1_report(service: AccountReportService = Provide[Container.account_report_service]):
    """Lấy sổ doanh thu S1-HKD theo Thông tư 88"""
    try:
        user_info = getattr(request, 'current_user', {})
        owner_id = user_info.get('owner_id') or user_info.get('user_id')
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({"error": "Thiếu start_date hoặc end_date (YYYY-MM-DD)"}), 400
            
        report = service.generate_s1_revenue_ledger(owner_id, start_date, end_date)
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
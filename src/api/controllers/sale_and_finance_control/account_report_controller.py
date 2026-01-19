from flask import Blueprint, jsonify
from api.middlewares.auth_middleware import token_required
# Thay vì import từ finance_service chung chung
from services.sale_and_finance_service.account_report_service import AccountReportService
from infrastructure.repositories.sale_and_finance_repo.account_report_repository import AccountReportRepository
from infrastructure.databases.mssql import session
from dependency_injector.wiring import inject, Provide
from dependency_container import Container
account_report_bp = Blueprint('account_report_bp', __name__)

@account_report_bp.route('/', methods=['POST'])
@token_required
@inject
def create_report():
    """
    Tạo báo cáo doanh thu
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            owner_id: {type: integer, example: 1}
            report_type: {type: string, example: "Monthly"}
            report_name: {type: string, example: "Báo cáo tháng 1"}
    responses:
      201: {description: "Thành công"}
    """
# src/api/controllers/sale_and_finance_control/account_report_controller.py
from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from dependency_injector.wiring import inject, Provide
from dependency_container import Container

account_report_bp = Blueprint('account_report_bp', __name__)

@account_report_bp.route('/tt88', methods=['GET'])
@token_required
@inject
def get_tt88_report(current_user, service: AccountReportService = Provide[Container.account_report_service]):
    """
    Lấy báo cáo Sổ chi tiết doanh thu (Thông tư 88)
    Query param: ?date=YYYY-MM-DD
    """
    try:
        owner_id = getattr(request, 'current_user_id', None)
        report_date = request.args.get('date') # FE gửi ngày muốn xem báo cáo
        
        if not report_date:
            return jsonify({"error": "Vui lòng chọn ngày báo cáo (?date=...)"}), 400
            
        report_data = report_service.generate_daily_report(owner_id, report_date)
        return jsonify(report_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@account_report_bp.route('/dashboard', methods=['GET'])
@token_required
@inject
# 👇 SỬA Ở ĐÂY: Dùng Container.account_report_service
def get_dashboard_stats(current_user, service: AccountReportService = Provide[Container.account_report_service]):
    """
    Lấy thống kê Dashboard (Doanh thu, Đơn hàng, Tồn kho)
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    """
    try:
        # Hỗ trợ lấy ID từ cả Owner và Employee
        owner_id = getattr(current_user, 'owner_id', None) or getattr(current_user, 'user_id', None)
        
        data = service.get_dashboard_stats(owner_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@account_report_bp.route('/chart', methods=['GET'])
@token_required
@inject
# 👇 SỬA Ở ĐÂY LUÔN
def get_chart_data(current_user, service: AccountReportService = Provide[Container.account_report_service]):
    """
    Lấy dữ liệu biểu đồ doanh thu 7 ngày
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    """
    try:
        owner_id = getattr(current_user, 'owner_id', None)
        data = service.get_revenue_chart(owner_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@account_report_bp.route('/top-products', methods=['GET'])
@token_required
@inject
# 👇 VÀ CẢ Ở ĐÂY NỮA
def get_top_products(current_user, service: AccountReportService = Provide[Container.account_report_service]):
    """
    Lấy Top 5 sản phẩm bán chạy
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    """
    try:
        owner_id = getattr(current_user, 'owner_id', None)
        data = service.get_top_products(owner_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
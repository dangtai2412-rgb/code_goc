from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel

from infrastructure.models.sale_and_finance.account_report_model import AccountReportModel
from infrastructure.databases.mssql import session
from sqlalchemy import func, Date

from infrastructure.models.inventory.stock_import_detail_model import StockImportDetailModel
from infrastructure.models.inventory.stock_import_model import StockImportModel

class AccountReportRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, report_model):
        try:
            self.session.add(report_model)
            self.session.commit()
            self.session.refresh(report_model)
            return report_model
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_owner(self, owner_id):
        return self.session.query(AccountReportModel).filter_by(owner_id=owner_id).all()
    
    
    def get_revenue_data_tt88(self, owner_id, start_date, end_date):
        """Lấy dữ liệu cho Sổ S1-HKD: Doanh thu chi tiết"""
        return self.session.query(
            OrderModel.order_date,
            OrderModel.order_id,
            OrderDetailModel.product_id,
            OrderDetailModel.quantity, # Giả định tên cột là quantity
            OrderDetailModel.unit_price,
            OrderDetailModel.line_total
        ).join(OrderDetailModel, OrderModel.order_id == OrderDetailModel.order_id)\
         .filter(OrderModel.owner_id == owner_id)\
         .filter(OrderModel.order_date.between(start_date, end_date))\
         .all()

    def get_inventory_data_tt88(self, owner_id, start_date, end_date):
        """Lấy dữ liệu cho Sổ S2-HKD: Nhập - Xuất - Tồn"""
        # 1. Lấy dữ liệu Nhập kho
        imports = self.session.query(
            StockImportModel.import_date.label('date'),
            StockImportDetailModel.product_id,
            StockImportDetailModel.quantity.label('in_qty'),
            func.constant(0).label('out_qty')
        ).join(StockImportDetailModel)\
         .filter(StockImportModel.owner_id == owner_id)\
         .filter(StockImportModel.import_date.between(start_date, end_date)).all()

        # 2. Lấy dữ liệu Xuất kho (từ Đơn hàng)
        exports = self.session.query(
            OrderModel.order_date.label('date'),
            OrderDetailModel.product_id,
            func.constant(0).label('in_qty'),
            OrderDetailModel.quantity.label('out_qty')
        ).join(OrderDetailModel)\
         .filter(OrderModel.owner_id == owner_id)\
         .filter(OrderModel.order_date.between(start_date, end_date)).all()

        return imports + exports
    def get_opening_balance(self, owner_id, product_id, start_date):
        """Tính tồn đầu kỳ = (Tổng Nhập trước start_date) - (Tổng Xuất trước start_date)"""
        
        # 1. Tính tổng nhập
        total_import = self.session.query(func.sum(StockImportDetailModel.quantity))\
            .join(StockImportModel)\
            .filter(StockImportModel.owner_id == owner_id)\
            .filter(StockImportDetailModel.product_id == product_id)\
            .filter(StockImportModel.import_date < start_date).scalar() or 0

        # 2. Tính tổng xuất
        total_export = self.session.query(func.sum(OrderDetailModel.quantity))\
            .join(OrderModel)\
            .filter(OrderModel.owner_id == owner_id)\
            .filter(OrderDetailModel.product_id == product_id)\
            .filter(OrderModel.order_date < start_date).scalar() or 0

        return total_import - total_export
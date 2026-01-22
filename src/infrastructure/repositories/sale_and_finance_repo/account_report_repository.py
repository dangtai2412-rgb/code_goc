from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel

from infrastructure.models.sale_and_finance.account_report_model import AccountReportModel
from infrastructure.databases.mssql import session
from sqlalchemy import func, Date
from datetime import datetime, timedelta
from infrastructure.models.inventory.product_model import ProductModel
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
    
    
    def get_dashboard_summary(self, owner_id):
        """Lấy tổng doanh thu và tổng đơn hàng"""
        stats = self.session.query(
            func.sum(OrderModel.total_amount).label('total_revenue'),
            func.count(OrderModel.order_id).label('total_orders')
        ).filter(OrderModel.owner_id == owner_id).first()
        
        # Lấy số lượng sản phẩm sắp hết hàng (ví dụ < 10)
        low_stock = self.session.query(func.count(ProductModel.product_id))\
            .filter(ProductModel.owner_id == owner_id, ProductModel.stock_quantity < 10).scalar()
            
        return {
            "revenue": float(stats.total_revenue or 0),
            "orders": stats.total_orders or 0,
            "low_stock_count": low_stock or 0
        }

    def get_revenue_last_7_days(self, owner_id):
        """Lấy doanh thu theo từng ngày trong 7 ngày gần nhất"""
        seven_days_ago = datetime.utcnow().date() - timedelta(days=6)
        
        return self.session.query(
            func.cast(OrderModel.order_date, Date).label('date'),
            func.sum(OrderModel.total_amount).label('daily_revenue')
        ).filter(OrderModel.owner_id == owner_id, OrderModel.order_date >= seven_days_ago)\
         .group_by(func.cast(OrderModel.order_date, Date))\
         .order_by(func.cast(OrderModel.order_date, Date)).all()

    def get_top_selling_products(self, owner_id, limit=5):
        """Lấy danh sách sản phẩm bán chạy nhất"""
        return self.session.query(
            ProductModel.product_name,
            func.sum(OrderDetailModel.quantity).label('total_sold')
        ).join(OrderDetailModel, ProductModel.product_id == OrderDetailModel.product_id)\
         .filter(ProductModel.owner_id == owner_id)\
         .group_by(ProductModel.product_name)\
         .order_by(func.sum(OrderDetailModel.quantity).desc())\
         .limit(limit).all()

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
    def get_revenue_data_tt88(self, owner_id, start_date, end_date):
        """Lấy dữ liệu thô để lập Sổ chi tiết doanh thu (S1-HKD) theo TT88"""
        return self.session.query(
            OrderModel.order_date,
            OrderModel.order_id,
            OrderDetailModel.product_id,
            OrderDetailModel.quantity, 
            OrderDetailModel.unit_price,
            OrderDetailModel.line_total
        ).join(OrderDetailModel, OrderModel.order_id == OrderDetailModel.order_id)\
         .filter(OrderModel.owner_id == owner_id)\
         .filter(OrderModel.order_date.between(start_date, end_date))\
         .all()
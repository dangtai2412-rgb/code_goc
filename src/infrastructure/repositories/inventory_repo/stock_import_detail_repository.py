# src/infrastructure/repositories/inventory_repo/stock_import_detail_repository.py
from infrastructure.models.inventory.stock_import_detail_model import StockImportDetailModel
from infrastructure.databases.mssql import session

class StockImportDetailRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, detail_model):
        """Lưu chi tiết dòng hàng vào Database"""
        try:
            self.session.add(detail_model)
            self.session.commit() # FIXED: Added commit
            self.session.refresh(detail_model) # FIXED: Refresh to get the new ID
            return detail_model
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_import_id(self, import_id):
        return self.session.query(StockImportDetailModel).filter_by(import_id=import_id).all()
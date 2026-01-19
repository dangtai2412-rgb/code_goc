from infrastructure.models.inventory.stock_import_detail_model import StockImportDetailModel
from infrastructure.databases.mssql import session

class StockImportDetailRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, detail_model):
        """Chỉ lưu chi tiết dòng hàng"""
        try:
            self.session.add(detail_model)
            return detail_model
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_import_id(self, import_id):
        return self.session.query(StockImportDetailModel).filter_by(import_id=import_id).all()
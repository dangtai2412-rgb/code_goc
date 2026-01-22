from infrastructure.models.inventory.stock_import_model import StockImportModel
from infrastructure.databases.mssql import session

class StockImportRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, import_model):
        """Chỉ lưu thông tin phiếu nhập, không tự ý cập nhật kho tại đây"""
        try:
            self.session.add(import_model)
            self.session.flush()
            # Không gọi commit ở đây để Service có thể quản lý Transaction cho cả chi tiết
            return import_model
        except Exception as e:
            self.session.rollback()
            raise e
    def get_all_by_owner(self, owner_id):
        return self.session.query(StockImportModel).filter_by(owner_id=owner_id).all()
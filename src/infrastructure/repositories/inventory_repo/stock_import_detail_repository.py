from infrastructure.models.inventory.stock_import_detail_model import StockImportDetailModel
from infrastructure.models.inventory.product_model import ProductModel
from infrastructure.databases.mssql import session

class StockImportDetailRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, detail_model):
        try:
            self.session.add(detail_model)
            
            # LOGIC QUAN TRỌNG: Tăng tồn kho khi thêm chi tiết nhập hàng
            product = self.session.query(ProductModel).filter_by(product_id=detail_model.product_id).first()
            if product:
                # Cộng dồn số lượng nhập vào kho
                product.stock_quantity = (product.stock_quantity or 0) + detail_model.quantity
            
            self.session.commit()
            self.session.refresh(detail_model)
            return detail_model
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_import_id(self, import_id):
        return self.session.query(StockImportDetailModel).filter_by(import_id=import_id).all()
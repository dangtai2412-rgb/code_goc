from infrastructure.models.inventory.unit_model import UnitModel
from domain.models.unit import Unit # Import lớp Domain vừa tạo
from infrastructure.databases.mssql import session

class UnitRepository:
    def __init__(self, db_session):
        # Đổi tên thành db_session để đồng bộ
        self.db_session = db_session

    def add(self, unit: Unit):
        # Đảm bảo UnitModel có các trường này
        db_unit = UnitModel(
            unit_name=unit.unit_name, 
            description=unit.description,
            owner_id=unit.owner_id,
            conversion_rate=getattr(unit, 'conversion_rate', 1), 
            is_base_unit=getattr(unit, 'is_base_unit', True)
        )
        try:
            self.db_session.add(db_unit)
            self.db_session.commit()
            self.db_session.refresh(db_unit)
            return db_unit
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_all_by_owner(self, owner_id):
        return self.db_session.query(UnitModel).filter_by(owner_id=owner_id).all()
    
    # src/infrastructure/repositories/inventory_repo/unit_repository.py
    def get_by_product(self, product_id):
        """Lấy tất cả đơn vị tính liên kết với một sản phẩm cụ thể"""
        try:
            return self.db_session.query(UnitModel).filter_by(product_id=product_id).all()
        except Exception as e:
            raise e
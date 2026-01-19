from infrastructure.models.inventory.unit_model import UnitModel
from domain.models.unit import Unit # Import lớp Domain vừa tạo
from infrastructure.databases.mssql import session

class UnitRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, unit: Unit):
        """SỬA: Nhận đối tượng Domain Unit thay vì tham số rời"""
        db_unit = UnitModel(
            product_id=unit.product_id, 
            unit_name=unit.unit_name, 
            conversion_rate=unit.conversion_rate, 
            is_base_unit=unit.is_base_unit
        )
        try:
            self.session.add(db_unit)
            self.session.commit()
            self.session.refresh(db_unit)
            return db_unit
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_product(self, product_id):
        return self.session.query(UnitModel).filter_by(product_id=product_id).all()
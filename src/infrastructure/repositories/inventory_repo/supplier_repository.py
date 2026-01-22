from infrastructure.models.inventory.supplier_model import SupplierModel
from infrastructure.databases.mssql import session

class SupplierRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, sup): # Nhận đối tượng Domain
        try:
            db_supplier = SupplierModel(
                supplier_name=sup.supplier_name,
                phone_number=sup.phone_number, # SỬA: Khớp với Model
                tax_code=sup.tax_code,         # SỬA: Khớp với Model
                owner_id=sup.owner_id
        )
            self.session.add(db_supplier)
            self.session.commit()
            self.session.refresh(db_supplier)
            return db_supplier
        except Exception as e:
            self.session.rollback()
            raise e
    def get_all_by_owner(self, owner_id):
        return self.session.query(SupplierModel).filter_by(owner_id=owner_id).all()
    def get_by_id(self, supplier_id, owner_id):
        return self.session.query(SupplierModel).filter_by(supplier_id=supplier_id, owner_id=owner_id).first()

    def update(self, supplier_model):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, supplier):
        try:
            self.session.delete(supplier)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
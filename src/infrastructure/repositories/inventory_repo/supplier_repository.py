from infrastructure.models.inventory.supplier_model import SupplierModel
from infrastructure.databases.mssql import session

class SupplierRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, supplier_model):
        try:
            self.session.add(supplier_model)
            self.session.commit()
            self.session.refresh(supplier_model)
            return supplier_model
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all_by_owner(self, owner_id):
        return self.session.query(SupplierModel).filter_by(owner_id=owner_id).all()

    def get_by_id(self, supplier_id, owner_id):
        return self.session.query(SupplierModel).filter_by(supplier_id=supplier_id, owner_id=owner_id).first()

    def update(self):
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
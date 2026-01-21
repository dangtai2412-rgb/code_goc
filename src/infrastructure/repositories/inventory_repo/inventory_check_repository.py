from infrastructure.models.inventory.inventory_check_model import InventoryCheckModel
from sqlalchemy.orm import joinedload

class InventoryCheckRepository:
    def __init__(self, db_session):
        self.session = db_session

    def add(self, inventory_check):
        self.session.add(inventory_check)
        # Commit sẽ được gọi ở Service sau khi update xong Product
        return inventory_check

    def commit(self):
        self.session.commit()

    def get_all(self, owner_id):
        return self.session.query(InventoryCheckModel)\
            .options(joinedload(InventoryCheckModel.details))\
            .filter_by(owner_id=owner_id)\
            .order_by(InventoryCheckModel.check_date.desc())\
            .all()

    def get_by_id(self, check_id):
        return self.session.query(InventoryCheckModel)\
            .options(joinedload(InventoryCheckModel.details))\
            .filter_by(check_id=check_id)\
            .first()
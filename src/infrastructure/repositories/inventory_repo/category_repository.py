from infrastructure.models.inventory.category_model import CategoryModel
# Giả sử bạn có lớp Domain Category
# from domain.models.category import Category 

class CategoryRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def add(self, category_name, description, owner_id):
        try:
            new_category = CategoryModel(
                category_name=category_name,
                description=description,
                owner_id=owner_id
            )
            self.db_session.add(new_category)
            self.db_session.commit()
            self.db_session.refresh(new_category)
            return new_category
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_all_by_owner(self, owner_id):
        return self.session.query(CategoryModel).filter_by(owner_id=owner_id).all()
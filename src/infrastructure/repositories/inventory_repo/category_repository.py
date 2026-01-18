from infrastructure.models.inventory.category_model import CategoryModel

class CategoryRepository:
    def __init__(self, session):
        self.session = session

    def add(self, category_name, description, owner_id):
        new_category = CategoryModel(
            category_name=category_name,
            description=description,
            owner_id=owner_id
        )
        self.session.add(new_category)
        self.session.commit()
        return new_category

    def get_all_by_owner(self, owner_id):
        return self.session.query(CategoryModel).filter_by(owner_id=owner_id).all()
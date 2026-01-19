from infrastructure.models.inventory.category_model import CategoryModel
# Giả sử bạn có lớp Domain Category
# from domain.models.category import Category 

class CategoryRepository:
    def __init__(self, session):
        self.session = session

    def add(self, cat): # Nhận đối tượng Domain thay vì tham số rời
        new_category = CategoryModel(
            category_name=cat.category_name,
            description=cat.description,
            owner_id=cat.owner_id
        )
        self.session.add(new_category)
        self.session.commit()
        return new_category
    def get_all_by_owner(self, owner_id):
        return self.session.query(CategoryModel).filter_by(owner_id=owner_id).all()
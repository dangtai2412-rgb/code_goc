class CategoryService:
    def __init__(self, repository):
        self.repo = repository

    def create_category(self, data, owner_id):
        name = data.get('category_name')
        if not name:
            raise ValueError("Tên danh mục không được để trống")
        
        return self.repo.add(
            category_name=name,
            description=data.get('description', ''),
            owner_id=owner_id
        )

    def get_categories(self, owner_id):
        return self.repo.get_all_by_owner(owner_id)
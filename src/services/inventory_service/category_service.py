class CategoryService:
    def __init__(self, repository):
        self.repository = repository

    def create_category(self, data, owner_id):
        # Đảm bảo truyền đúng 'category_name' như định nghĩa trong Repo
        return self.repository.add(
            category_name=data.get('category_name'), 
            description=data.get('description'),
            owner_id=owner_id
        )

    def get_categories(self, owner_id):
        return self.repository.get_all_by_owner(owner_id)
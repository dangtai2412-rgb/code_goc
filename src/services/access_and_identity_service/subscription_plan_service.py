class SubscriptionPlanService:
    def __init__(self, repository):
        self.repository = repository

    def create_plan(self, data):
        # 1. Lấy dữ liệu và kiểm tra logic
        name = data.get('plan_name')
        if not name:
            raise ValueError("Tên gói cước không được để trống")

        duration = data.get('duration')
        if not duration or int(duration) <= 0:
            raise ValueError("Thời hạn gói cước phải lớn hơn 0")

        price = float(data.get('price', 0))
        if price < 0:
            raise ValueError("Giá gói cước không được nhỏ hơn 0")
            
        # 2. Gọi Repository để lưu
        return self.repository.add(
            name=name, 
            duration=int(duration), 
            price=price
        )

    def list_plans(self):
        return self.repository.get_all()
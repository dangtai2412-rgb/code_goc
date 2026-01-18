class OrderDetailService:
    def __init__(self, repository):
        self.repository = repository

    def get_details_by_order_id(self, order_id):
        """Lấy danh sách chi tiết của một hóa đơn cụ thể"""
        return self.repository.get_by_order(order_id)

    def calculate_item_total(self, quantity, unit_price):
        """Logic tính thành tiền cho một dòng sản phẩm"""
        if quantity <= 0:
            raise ValueError("Số lượng phải lớn hơn 0")
        return quantity * unit_price
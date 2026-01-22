
from domain.models.customer import Customer


class CustomerService:
    def __init__(self, repository):
        self.repository = repository

    def create_customer(self, data, owner_id): # Nhận owner_id từ Controller
        if not data.get('customer_name'):
            raise ValueError("Tên khách hàng không được để trống")
        
        # BƯỚC QUAN TRỌNG: Tạo đối tượng Domain trước
        customer_domain = Customer(
            customer_name=data['customer_name'],
            phone_number=data.get('phone_number'),
            address=data.get('address'),
            owner_id=owner_id # Dùng owner_id từ Token
        )
        
        # Truyền CẢ ĐỐI TƯỢNG xuống Repo
        return self.repository.add(customer_domain)

    def list_customers(self):
        return self.repository.get_all()
    def update_customer(self, customer_id, data):
        customer = self.repository.get_by_id(customer_id)
        if not customer: raise ValueError("Khách hàng không tồn tại")
        
        customer.customer_name = data.get('customer_name', customer.customer_name)
        customer.phone_number = data.get('phone_number', customer.phone_number)
        customer.address = data.get('address', customer.address)
        
        return self.repository.update(customer)

    def delete_customer(self, customer_id):
        return self.repository.delete(customer_id)
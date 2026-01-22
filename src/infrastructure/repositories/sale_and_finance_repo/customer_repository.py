from infrastructure.models.sale_and_finance.customer_model import CustomerModel
from infrastructure.databases.mssql import session
from domain.models.customer import Customer
class CustomerRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, customer_domain):
        # Chuyển từ Domain sang Database Model
        db_customer = CustomerModel(
            customer_name=customer_domain.customer_name,
            owner_id=customer_domain.owner_id,
            phone_number=customer_domain.phone_number,
            address=customer_domain.address,
            email=customer_domain.email
        )
        try:
            self.session.add(db_customer)
            self.session.commit()
            self.session.refresh(db_customer)
            return db_customer
        except Exception as e:
            self.session.rollback()
            raise e
        

    def get_all_customers(self):
        return self.session.query(CustomerModel).all()
    def get_by_id(self, customer_id,owner_id):
        return self.session.query(CustomerModel).filter_by(customer_id=customer_id,owner_id=owner_id).first()

    def update(self, customer_model):
        try:
            self.session.commit()
            return customer_model
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, customer_id, owner_id): # Thêm owner_id
        try:
            # Truyền đủ 2 tham số để không bị lỗi TypeError
            customer = self.get_by_id(customer_id, owner_id) 
            if customer:
                self.session.delete(customer)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e
    def get_all_by_owner(self, owner_id):
        # Lọc danh sách khách hàng thuộc về chủ shop đang đăng nhập
        return self.session.query(CustomerModel).filter_by(owner_id=owner_id).all()
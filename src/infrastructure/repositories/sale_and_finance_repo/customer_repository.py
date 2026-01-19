from infrastructure.models.sale_and_finance.customer_model import CustomerModel
from infrastructure.databases.mssql import session
from domain.models.customer import Customer
class CustomerRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, cust: Customer): # NHẬN ĐỐI TƯỢNG DOMAIN
        db_cust = CustomerModel(
            customer_name=cust.customer_name, 
            phone_number=cust.phone_number, 
            address=cust.address,
            owner_id=cust.owner_id
        )
        try:
            self.session.add(db_cust)
            self.session.commit()
            self.session.refresh(db_cust)
            return db_cust
        except Exception as e:
            self.session.rollback()
            raise e
        

    def get_all(self):
        return self.session.query(CustomerModel).all()
    def get_by_id(self, customer_id):
        return self.session.query(CustomerModel).filter_by(customer_id=customer_id).first()

    def update(self, customer_model):
        try:
            self.session.commit()
            return customer_model
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, customer_id):
        try:
            customer = self.get_by_id(customer_id)
            if customer:
                self.session.delete(customer)
                self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e
    def get_all_by_owner(self, owner_id):
        """Lấy toàn bộ khách hàng của một shop cụ thể"""
        return self.session.query(CustomerModel).filter_by(owner_id=owner_id).all()
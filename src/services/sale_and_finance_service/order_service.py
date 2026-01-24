from datetime import datetime
from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel

class OrderService:
    def __init__(self, repository, product_repo, debt_service):
        self.repo = repository
        self.product_repo = product_repo
        self.debt_service = debt_service

    # src/services/sale_and_finance_service/order_service.py (key part)
from infrastructure.databases import session
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel
from datetime import datetime

class OrderService:
    def __init__(self, order_repo, product_repo, debt_service):
        self.repo = order_repo
        self.product_repo = product_repo
        self.debt_service = debt_service

    def create_order(self, data, user_id, owner_id=None):
        """
        data: { customer_id, details:[{product_id, quantity, unit_price}], total_amount, paid_amount, payment_method, ... }
        owner_id should be passed from controller (e.g., from token payload).
        """
        try:
            with session.begin():
                order = OrderModel(
                    owner_id=owner_id or data.get('owner_id'),
                    customer_id=data.get('customer_id'),
                    total_amount=data.get('total_amount', 0),
                    payment_status=data.get('payment_status', 'UNPAID'),
                    payment_method=data.get('payment_method'),
                    created_by=user_id,
                    order_date=datetime.now()
                )
                session.add(order)
                session.flush()  # generate order id

                total = 0
                for item in data.get('details', []):
                    product = self.product_repo.get_by_id(item['product_id'])
                    if not product:
                        raise ValueError(f"Sản phẩm ID {item['product_id']} không tồn tại")
                    if product.stock_quantity < item['quantity']:
                        raise ValueError(f"Sản phẩm {product.product_name} không đủ tồn kho!")
                    product.stock_quantity -= item['quantity']
                    session.add(product)

                    line_total = item['quantity'] * item['unit_price']
                    total += line_total

                    detail = OrderDetailModel(
                        order_id=order.order_id,
                        product_id=item['product_id'],
                        quantity=item['quantity'],
                        unit_price=item['unit_price'],
                        line_total=line_total
                    )
                    session.add(detail)

                # payment/debt handling...
                if data.get('paid_amount', 0) < total and order.customer_id:
                    debt_amount = total - data.get('paid_amount', 0)
                    self.debt_service.create_debt_from_order(order.customer_id, order.order_id, owner_id or order.owner_id, debt_amount)

                # accounting entries e.g. accounting_repo.create_sales_journal(...)
                return order

        except SQLAlchemyError:
            raise
        except Exception:
            raise
    def get_orders_by_owner(self, owner_id):
        # Có thể bổ sung thêm logic nghiệp vụ hoặc phân trang ở đây nếu cần
        return self.repo.get_all_by_owner(owner_id)
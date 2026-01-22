from datetime import datetime
from infrastructure.models.sale_and_finance.payment_model import PaymentModel
from decimal import Decimal

class PaymentService:
    
    
    def __init__(self, payment_repo, debt_repo): # Phải thụt lề vào như thế này
        self.payment_repo = payment_repo
        self.debt_repo = debt_repo
    
    def process_payment(self, data, owner_id):
        amount_val = data.get('amount', 0)
        amount_paid = Decimal(str(amount_val))
        if amount_paid <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")

        # 1. Nếu là thanh toán nợ (có debt_id)
        debt_id = data.get('debt_id')
        if debt_id:
            # Tìm khoản nợ (phải kèm owner_id để bảo mật)
            debt = self.debt_repo.get_by_id(debt_id, owner_id)
            if not debt:
                raise ValueError("Không tìm thấy khoản nợ hợp lệ")
            
            # Cập nhật số nợ còn lại
            debt.remaining_debt -= amount_paid
            if debt.remaining_debt <= 0:
                debt.debt_status = "Paid"
                debt.remaining_debt = 0
            else:
                debt.debt_status = "Partial"

        # 2. Lưu vết thanh toán vào bảng Payments
        return self.payment_repo.add(data, owner_id)

    def get_payment_history(self, debt_id):
        """Lấy lịch sử trả nợ của một khoản nợ cụ thể"""
        return self.payment_repo.get_by_debt(debt_id)
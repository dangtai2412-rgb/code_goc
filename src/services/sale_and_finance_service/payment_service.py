from datetime import datetime
from infrastructure.models.sale_and_finance.payment_model import PaymentModel

class PaymentService:
    def __init__(self, payment_repo, debt_repo):
        """
        Khởi tạo Service với 2 Repository để xử lý liên bảng
        """
        self.payment_repo = payment_repo
        self.debt_repo = debt_repo

    def make_payment(self, data):
        """
        Logic nghiệp vụ: Ghi nhận thanh toán và cập nhật trạng thái nợ
        """
        # 1. Kiểm tra khoản nợ có tồn tại không
        debt_id = data.get('debt_id')
        debt = self.debt_repo.get_by_id(debt_id)
        if not debt:
            raise ValueError("Không tìm thấy khoản công nợ này!")

        # 2. Tạo đối tượng thanh toán mới
        amount_paid = float(data.get('amount', 0))
        new_payment = PaymentModel(
            debt_id=debt_id,
            amount_paid=amount_paid,
            payment_date=datetime.now().date(),
            payment_method=data.get('payment_method', 'Cash')
        )

        # 3. Cập nhật trạng thái khoản nợ [Nghiệp vụ quan trọng]
        # Nếu số tiền trả bằng hoặc lớn hơn số nợ hiện tại -> Đánh dấu đã trả xong
        if amount_paid >= float(debt.debt_amount):
            debt.debt_status = "Paid"
        else:
            debt.debt_status = "Partial" # Trả một phần

        # 4. Lưu cả thanh toán và cập nhật khoản nợ qua Repository
        return self.payment_repo.add(new_payment)

    def get_payment_history(self, debt_id):
        """Lấy lịch sử trả nợ của một khoản nợ cụ thể"""
        return self.payment_repo.get_by_debt(debt_id)
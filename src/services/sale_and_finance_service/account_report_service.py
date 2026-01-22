from datetime import date
from infrastructure.models.sale_and_finance.account_report_model import AccountReportModel

class AccountReportService:
    def __init__(self, repository):
        self.repository = repository

    def create_report(self, data):
        # Logic tạo báo cáo (ví dụ: mặc định lấy ngày hiện tại)
        new_report = AccountReportModel(
            owner_id=data['owner_id'],
            report_type=data.get('report_type', 'Daily'),
            report_name=data.get('report_name', f"Report-{date.today()}"),
            generated_date=date.today()
        )
        return self.repository.add(new_report)

    def get_owner_reports(self, owner_id):
        return self.repository.get_by_owner(owner_id)
    def generate_s1_revenue_ledger(self, owner_id, start_date, end_date):
        """Sổ chi tiết doanh thu bán hàng (Mẫu S1-HKD)"""
        raw_data = self.repository.get_revenue_data_tt88(owner_id, start_date, end_date)
        
        report = {
            "title": "SỔ CHI TIẾT DOANH THU BÁN HÀNG HÓA, DỊCH VỤ",
            "template": "S1-HKD",
            "owner_id": owner_id,
            "period": f"{start_date} - {end_date}",
            "details": []
        }

        total_sum = 0
        for item in raw_data:
            row = {
                "date": item.order_date.strftime("%d/%m/%Y"),
                "voucher": f"HD{item.order_id:05d}", # Số hiệu chứng từ
                "product_id": item.product_id,
                "quantity": float(item.quantity),
                "unit_price": float(item.unit_price),
                "amount": float(item.line_total)
            }
            report["details"].append(row)
            total_sum += float(item.line_total)

        report["total_revenue"] = total_sum
        return report

    # src/services/sale_and_finance_service/account_report_service.py

    def generate_s2_inventory_ledger(self, owner_id, start_date, end_date):
        """Sổ chi tiết vật liệu, dụng cụ, hàng hóa (Mẫu S2-HKD)"""
        
        # Lấy danh sách giao dịch (Nhập/Xuất) đã có trong Repository của bạn
        raw_transactions = self.repository.get_inventory_data_tt88(owner_id, start_date, end_date)
        
        # Sắp xếp giao dịch theo ngày
        raw_transactions.sort(key=lambda x: x.date)

        report = {
            "title": "SỔ CHI TIẾT VẬT LIỆU, DỤNG CỤ, HÀNG HÓA",
            "template": "S2-HKD",
            "products": {}
        }

        # Xử lý theo từng sản phẩm
        for item in raw_transactions:
            p_id = item.product_id
            if p_id not in report["products"]:
                # Tính tồn đầu kỳ cho sản phẩm này
                opening = self.repository.get_opening_balance(owner_id, p_id, start_date)
                report["products"][p_id] = {
                    "opening_stock": opening,
                    "current_balance": opening,
                    "history": []
                }

            # Cập nhật số dư hiện tại sau mỗi giao dịch
            report["products"][p_id]["current_balance"] += (item.in_qty - item.out_qty)
            
            report["products"][p_id]["history"].append({
                "date": item.date.strftime("%d/%m/%Y"),
                "in_qty": float(item.in_qty),
                "out_qty": float(item.out_qty),
                "balance": float(report["products"][p_id]["current_balance"])
            })

        return report
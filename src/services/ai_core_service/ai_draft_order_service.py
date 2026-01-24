import google.generativeai as genai
import json
import re
from config import Config
import time
# src/services/ai_core_service/ai_draft_order_service.py
import google.generativeai as genai
import json
import re
from config import Config

class AIDraftOrderService:
    def __init__(self, draft_repo, order_service, customer_repo, product_repo):
        self.draft_repo = draft_repo
        self.order_service = order_service
        self.customer_repo = customer_repo
        self.product_repo = product_repo
        
        api_key = getattr(Config, 'GEMINI_API_KEY', None)
        if not api_key:
            raise ValueError("Thiếu GEMINI_API_KEY trong file .env")
            
        genai.configure(api_key=api_key)
        # SỬA TÊN MODEL Ở ĐÂY: Sử dụng gemini-2.0-flash từ danh sách của bạn
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def create_draft_from_voice(self, voice_text, employee_id):
        # Prompt được tối ưu để AI trả về JSON chuẩn
        prompt = f"""
        Phân tích câu lệnh sau thành JSON đơn hàng: '{voice_text}'
        Yêu cầu trả về DUY NHẤT một khối JSON theo cấu trúc:
        {{
            "customer_name": "Tên khách hàng hoặc null",
            "items": [
                {{"product_name": "Tên sản phẩm", "quantity": số_lượng}}
            ],
            "payment_method": "Cash" hoặc "Debt"
        }}
        Lưu ý: Nếu không nhắc đến thanh toán, mặc định là "Cash".
        """
        for attempt in range(3):
            try:
                response = self.model.generate_content(prompt)
                
                # Dùng Regex để bóc tách JSON (phòng trường hợp AI trả về text thừa)
                match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if not match:
                    raise ValueError("AI không thể trích xuất thông tin JSON")
                
                ai_json_str = match.group(0)
                ai_data = json.loads(ai_json_str)
                
                # Lưu vào repo (Đảm bảo repo xử lý employee_id và JSON string)
                return self.draft_repo.create_draft(
                raw_text=voice_text,
                extracted_json=ai_data,
                employee_id=employee_id
)
            except Exception as e:
                    if "429" in str(e) and attempt < 2:
                        time.sleep(5) # Chờ 5 giây rồi thử lại
                        continue
                    raise Exception(f"Lỗi AI: {str(e)}")

    def confirm_and_create_order(self, draft_id, employee_id, owner_id=None):
        draft = self.draft_repo.get_by_id(draft_id)
        if not draft:
            raise ValueError("Draft order not found")

        ai_data = json.loads(draft.extracted_json)

        # Tìm khách hàng theo tên trích xuất được
        customer = self.customer_repo.get_by_name(ai_data.get('customer_name'))

        order_payload = {
        "customer_id": customer.customer_id if customer else None,
        "payment_method": ai_data.get('payment_method', 'Cash'),
        "details": []   # <-- use 'details' to match OrderService expectation
    }

        for item in ai_data.get('items', []):
            product = self.product_repo.get_by_name(item.get('product_name'))
            if product:
                order_payload['details'].append({
                    "product_id": product.product_id,
                    "quantity": item.get('quantity', 0),
                    "unit_price": getattr(product, 'base_price', item.get('unit_price', 0)),
                    "unit_id": getattr(product, 'unit_id', None)
                })

        if not order_payload['items']:
            raise ValueError("No valid products found in the AI draft")

        # Chuyển owner_id xuống OrderService để tạo order đúng context
        result = self.order_service.create_order(order_payload, employee_id, owner_id=owner_id)
        if result:
            # cập nhật trạng thái draft nếu order tạo thành công
            self.draft_repo.update_status(draft_id, "Confirmed")
        return result
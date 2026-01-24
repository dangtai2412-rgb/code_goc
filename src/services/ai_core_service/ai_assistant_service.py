from infrastructure.models.ai_core.ai_assistant_model import AIAssistantModel
import json

class AIAssistantService:
    def __init__(self, repository, ai_draft_order_repo):
        # repository: AIAssistantRepository (quản lý cấu hình AI)
        # ai_draft_order_repo: AIDraftOrderRepository (quản lý các đơn hàng nháp)
        self.repository = repository
        self.ai_draft_order_repo = ai_draft_order_repo

    def update_ai_settings(self, data):
        """Cấu hình thông số cho trợ lý AI (Version, Model type)"""
        version = data.get('version', 'v1.0')
        model_type = data.get('model_type', 'GPT-3.5')

        if not version:
            raise ValueError("Phiên bản AI không được để trống")

        return self.repository.update_config(version, model_type)

    def get_current_config(self):
        """Lấy cấu hình AI hiện tại"""
        return self.repository.get_latest_config()
    
    def process_order_command(self, text_input):
        """
        Sử dụng LLM để trích xuất thông tin và LƯU vào bảng đơn hàng nháp
        """
        # 1. Định nghĩa Prompt
        prompt = f"""
        Bạn là trợ lý bán hàng cho hộ kinh doanh vật liệu xây dựng. 
        Hãy trích xuất thông tin đơn hàng từ câu lệnh sau: "{text_input}"
        Trả về kết quả dưới dạng JSON duy nhất với các trường:
        - customer_name: Tên khách (string)
        - items: Danh sách sản phẩm (mỗi item gồm: product_name, quantity)
        - payment_method: "Cash" hoặc "Debt" (mặc định "Cash" nếu không nhắc đến)
        """

        # 2. Giả lập kết quả từ AI (Hoặc gọi Gemini API tương tự file AIDraftOrderService)
        ai_extracted_data = {
            "customer_name": "Khách hàng mới",
            "items": [{"product_name": "Xi măng", "quantity": 1}],
            "payment_method": "Cash"
        }

        # 3. LƯU VÀO DATABASE qua ai_draft_order_repo
        # Đảm bảo tên phương thức khớp với AIDraftOrderRepository
        draft_order = self.ai_draft_order_repo.create_draft(
        raw_text=text_input,
        extracted_json=ai_extracted_data,
        employee_id=None  # hoặc actual employee id
        )

        return draft_order
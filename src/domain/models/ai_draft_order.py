class AIDraftOrder:
    def __init__(self, employee_id, ai_id, customer_id, recognized_content, confirmation_status="Pending", source=None, draft_id=None):
        self.draft_id = draft_id
        self.employee_id = employee_id  
        self.ai_id = ai_id              
        self.customer_id = customer_id  
        self.recognized_content = recognized_content 
        self.confirmation_status = confirmation_status 
        self.source = source            
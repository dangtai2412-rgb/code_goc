class AccountReport:
    def __init__(self, owner_id, report_type, reporting_period, generated_date, report_id=None):
        self.report_id = report_id
        self.owner_id = owner_id  
        self.report_type = report_type  
        self.reporting_period = reporting_period  
        self.generated_date = generated_date  
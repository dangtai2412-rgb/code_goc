from flask import Flask, app
from config import Config
from api.middleware import setup_middleware
from api.routes import register_routes
from infrastructure.databases import init_db
from app_logging import setup_logging
from cors import init_cors
from dependency_container import Container
from flasgger import Swagger

def create_app():
    """
Factory function to create and configure the Flask application.
Returns:
    Flask app instance
"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    container = Container()
    container.wire(modules=[
        "api.controllers.access_and_identity_control.administrator_controller",
        "api.controllers.access_and_identity_control.business_owner_controller",
        "api.controllers.access_and_identity_control.employee_controller",
        "api.controllers.auth_controller",
        "api.controllers.inventory_control.product_controller",
        "api.controllers.inventory_control.unit_controller",
        "api.controllers.inventory_control.supplier_controller",
        "api.controllers.inventory_control.category_controller", # ADDED
        "api.controllers.inventory_control.inventory_check_controller", # ADDED
        "api.controllers.inventory_control.stock_import_detail_controller",
        "api.controllers.inventory_control.stock_import_controller",
        "api.controllers.sale_and_finance_control.customer_controller",
        "api.controllers.sale_and_finance_control.order_controller",
        "api.controllers.sale_and_finance_control.debt_controller",
        "api.controllers.sale_and_finance_control.account_report_controller",
        "api.controllers.sale_and_finance_control.expense_controller", # ADDED
        "api.controllers.sale_and_finance_control.return_order_controller", # ADDED
        "api.controllers.ai_core_control.ai_draft_order_controller",
        "api.controllers.ai_core_control.ai_assistant_controller",
        "api.controllers.access_and_identity_control.subscription_plan_controller"
    ])
    
    # ... rest of your setup code
    init_cors(app)
    setup_logging(app)
    swagger_config = {
        "headers": [],
        "specs": [{"endpoint": 'apispec', "route": '/apispec.json'}],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/", # Đường dẫn vào Swagger của bạn
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey", "name": "Authorization", "in": "header",
                "description": "Nhập theo cú pháp: Bearer <token>"
            }
        }
    }
    Swagger(app, config=swagger_config)
    
    # BƯỚC 4: Đăng ký các Route và Database
    register_routes(app)
    init_db(app)

    return app
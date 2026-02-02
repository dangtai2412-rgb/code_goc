# src/create_app.py
from flask import Flask
from config import Config
from api.middleware import setup_middleware
from api.routes import register_routes
from infrastructure.databases import init_db
from app_logging import setup_logging
from cors import init_cors
from dependency_container import Container
from flasgger import Swagger
from api.swagger import spec # Import spec từ swagger.py
from error_handler import register_error_handlers # Import xử lý lỗi

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 1. Dependency Injection
    container = Container()
    # (Giữ nguyên phần wire modules của bạn, không thay đổi)
    container.wire(modules=[
        "api.controllers.access_and_identity_control.administrator_controller",
        "api.controllers.access_and_identity_control.business_owner_controller",
        "api.controllers.access_and_identity_control.employee_controller",
        "api.controllers.auth_controller",
        "api.controllers.inventory_control.product_controller",
        "api.controllers.inventory_control.unit_controller",
        "api.controllers.inventory_control.supplier_controller",
        "api.controllers.inventory_control.category_controller",
        "api.controllers.inventory_control.inventory_check_controller",
        "api.controllers.inventory_control.stock_import_detail_controller",
        "api.controllers.inventory_control.stock_import_controller",
        "api.controllers.sale_and_finance_control.customer_controller",
        "api.controllers.sale_and_finance_control.order_controller",
        "api.controllers.sale_and_finance_control.debt_controller",
        "api.controllers.sale_and_finance_control.account_report_controller",
        "api.controllers.sale_and_finance_control.expense_controller",
        "api.controllers.sale_and_finance_control.return_order_controller",
        "api.controllers.ai_core_control.ai_draft_order_controller",
        "api.controllers.ai_core_control.ai_assistant_controller",
        "api.controllers.access_and_identity_control.subscription_plan_controller"
    ])
    
    # 2. Setup Middleware & Logging
    init_cors(app)
    setup_logging(app)
    setup_middleware(app) # Gọi middleware đã sửa
    
    # 3. Setup Swagger (BẢN SỬA LỖI)
    # Lấy definitions từ apispec để Flasgger hiểu
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Bizflow API",
            "version": "1.0.0"
        },
        # Nạp definitions từ file swagger.py vào đây
        "definitions": spec.to_dict().get("components", {}).get("schemas", {})
    }

    swagger_config = {
        "headers": [],
        "specs": [{"endpoint": 'apispec', "route": '/apispec.json'}],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey", 
                "name": "Authorization", 
                "in": "header",
                "description": "Nhập: Bearer <token>"
            }
        }
    }
    
    # Khởi tạo Swagger với template đã nối
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # 4. Đăng ký Error Handler & Routes & DB
    register_error_handlers(app) # Đăng ký xử lý lỗi toàn cục
    register_routes(app)
    init_db(app)

    return app
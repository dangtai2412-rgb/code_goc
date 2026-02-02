# src/create_app.py (Chỉ đoạn cần sửa)
# ... các import khác ...
from error_handler import register_error_handlers # Import cái này

def create_app():
    # ... code khởi tạo app ...

    # Đăng ký Error Handlers (Nên đặt trước khi register routes)
    register_error_handlers(app)

    # Đăng ký các Route và Database
    register_routes(app)
    init_db(app)
    
    return app
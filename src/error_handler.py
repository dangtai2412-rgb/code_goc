# src/error_handler.py
from flask import jsonify
from marshmallow import ValidationError

class CustomError(Exception):
    """Lỗi logic nghiệp vụ (Ví dụ: Không đủ hàng tồn kho)"""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {'error': self.message}

def handle_custom_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def handle_validation_error(error):
    """Xử lý lỗi validate dữ liệu đầu vào"""
    response = jsonify({'validation_errors': error.messages})
    response.status_code = 400
    return response

def handle_general_exception(error):
    """Bắt tất cả các lỗi còn lại (Lỗi server 500)"""
    # Ghi log lỗi tại đây (nếu có logger)
    response = jsonify({'message': 'Đã xảy ra lỗi không mong muốn.', 'details': str(error)})
    response.status_code = 500
    return response

def register_error_handlers(app):
    app.register_error_handler(CustomError, handle_custom_error)
    app.register_error_handler(ValidationError, handle_validation_error) # Bắt lỗi từ Schema.validate
    app.register_error_handler(Exception, handle_general_exception)
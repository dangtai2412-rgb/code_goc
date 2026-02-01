from flask import request, jsonify
from werkzeug.exceptions import HTTPException

def log_request_info(app):
    # Sử dụng .get_json(silent=True) để tránh crash nếu body không phải JSON
    body = request.get_json(silent=True) or request.get_data(as_text=True)
    app.logger.debug(f"Method: {request.method} | Path: {request.path}")
    app.logger.debug(f"Headers: {dict(request.headers)}")
    app.logger.debug(f"Body: {body[:500]}...") # Giới hạn log để tránh quá tải

def handle_exception(e):
    """Xử lý lỗi thông minh hơn"""
    # Nếu là lỗi HTTP tiêu chuẩn (404, 405, v.v.)
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }).data
        response.content_type = "application/json"
        return response

    # Nếu là lỗi logic code chưa xác định (500)
    return jsonify({
        "error": "Internal Server Error",
        "message": "Đã có lỗi xảy ra phía máy chủ."
    }), 500

def setup_middleware(app):
    @app.before_request
    def before_request():
        # Bỏ qua logging cho các route tĩnh nếu cần
        if request.endpoint != 'static':
            log_request_info(app)

    @app.after_request
    def after_request(response):
        # Thêm header tùy chỉnh
        response.headers['X-Custom-Header'] = 'Value'
        # Đảm bảo Content-Type luôn là JSON nếu bạn làm API
        return response

    @app.errorhandler(Exception)
    def error_handler(e):
        return handle_exception(e)
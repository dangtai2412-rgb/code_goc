from flask import jsonify

def create_response(success, message, data=None, errors=None, status_code=200):
    """
    Hàm gốc để tạo cấu trúc response đồng nhất.
    """
    response = {
        "success": success,
        "message": message
    }
    if data is not None:
        response["data"] = data
    if errors is not None:
        response["errors"] = errors
        
    return jsonify(response), status_code

def success_response(data=None, message="Success", status_code=200):
    """Trả về khi yêu cầu thành công (200 OK, 201 Created)."""
    return create_response(True, message, data=data, status_code=status_code)

def error_response(message="An error occurred", status_code=400, errors=None):
    """Trả về cho các lỗi Client (400, 401, 403)."""
    return create_response(False, message, errors=errors, status_code=status_code)

def not_found_response(message="Resource not found"):
    """Lỗi 404 đặc thù."""
    return error_response(message, status_code=404)

def validation_error_response(errors):
    """Lỗi xác thực dữ liệu (422 Unprocessable Entity là chuẩn nhất cho validation)."""
    return error_response("Validation failed", status_code=422, errors=errors)

def internal_error_response(message="Internal Server Error"):
    """Lỗi hệ thống (500)."""
    return error_response(message, status_code=500)
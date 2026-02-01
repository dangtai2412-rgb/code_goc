from flask import request, jsonify, abort

def get_request_data():
    """Trích xuất dữ liệu JSON một cách an toàn."""
    data = request.get_json(silent=True)
    if data is None:
        # Thay vì return jsonify, ta dùng abort hoặc raise để ngắt luồng xử lý
        abort(400, description="Dữ liệu không đúng định dạng JSON hoặc rỗng.")
    return data

def validate_request_schema(schema):
    """Xác thực dữ liệu dựa trên schema (giả định dùng Marshmallow)."""
    data = get_request_data()
    errors = schema.validate(data)
    
    if errors:
        # Trả về một dictionary chứa lỗi để controller xử lý hoặc dùng abort
        return None, errors
    return data, None

def handle_post_request(schema):
    """Ví dụ cách sử dụng trong một route."""
    data, errors = validate_request_schema(schema)
    
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400
    
    # Logic xử lý sau khi đã có data sạch
    # db.session.add(NewObject(**data)) ...
    return jsonify({"message": "Tạo thành công", "data": data}), 201

def handle_get_request():
    # Thường GET request lấy data từ request.args (query params)
    query_params = request.args.to_dict()
    return jsonify({"params_received": query_params}), 200